# Copyright (c) 2012-2015 by FEI Company
# All rights reserved. This file includes confidential and proprietary
# information of FEI Company.

# PIL comes from Pillow package: import before PySide is imported, else can lead to problems
# with matplotlib backend selection of UI toolkit. ???TODO - figure out precise details...
from PIL import Image
from fei.infra.pillow.image_qt import ImageQt  # solves issue with Pillow version

import subprocess
from constants import HELP_FILE
import PySide
from PySide.QtGui import *
from PySide.QtCore import *
from functools import partial
from types import *

from fei.autostar.applications.sherpa.infra.autostar_styles import (TASK_ACTIVE_STYLE,
                                                                      TASK_INACTIVE_STYLE) # noqa
from fei.autostar.applications.sherpa.ui.about_dialog import AboutDialog
from fei.autostar.tasks.infra.task import TaskStatus  # noqa
from fei.autostar.applications.sherpa.ui.gen import (MainWindowGUI,
                                                       GeneralSettingsGUI)  # noqa, made with Qt designer, converted to *.py with pyside-uic.exe
from fei.autostar.applications.sherpa.ui.define_ui_model import (create_tree_control_items,
                                                                   qtask_id_to_executor)  # noqa
from fei.autostar.applications.sherpa.ui.category_model import CategoryAdministration  # noqa
from fei.autostar.applications.sherpa.ui.system_state import *  # noqa
from fei.autostar.applications.sherpa.ui.qtask_model import QTaskModel  # noqa
from fei.autostar.applications.sherpa.ui.image_label import ResizingImage
from fei.autostar.applications.sherpa.mono.dialog_handler import *  # noqa
from fei.autostar.applications.sherpa.infra.base_dialog_handler import reset_settings_pane
from fei.autostar.applications.sherpa.mono.ui_helpers import np2d_almost_to_qimage  # noqa
from fei.autostar.applications.sherpa.ui.display_conditions import *  # noqa
from fei.autostar.applications.sherpa.ui.constants import privileged_users
from fei.infra.licensing.constants import *  # noqa
from fei.autostar.applications.sherpa.ui.Slider import SliderEventFilter


logger = logging.getLogger(__name__)


class MainWindow(QMainWindow, MainWindowGUI.Ui_mainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.uiSettings = QSettings()
        self.setupUi(self)
        self.init_dialog()


    def init_dialog(self):
        """ Initialize the presentation layer
        """
        self._init_category_admin()

        # Store the pyside-uic generated values at initial startup
        # Overwrite each startup to accommodate new release
        self._storeWindowArrangement("Defaults")
        self._restoreWindowArrangement("Customization")

        self._create_category_pane()
        self._init_panes()
        self._init_progressindicators()
        self._init_general_settings_ui()

        # Hide docks until they are explicitly enabled
        for child in self.children():
            if isinstance(child, QDockWidget):
                if child.features() & QDockWidget.DockWidgetClosable:
                    child.setVisible(False)

        self._init_input_validation()
        self._init_ui_signalhandlers()
        self._init_category_selection()

        self._set_expert_mode(False)

        self.actionUndo.triggered.connect(self.undo_dlg_handler)
        self.actionRedo.triggered.connect(self.redo_dlg_handler)
        self.actionStop.triggered.connect(self.stop_dlg_handler)

        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint)

    def _init_mono_controls(self):
        """ Hook up Mono specific Controls.
            No problem to connect up signals/slots even if button will not be enabled.
        """
        # Acquire
        self.monoControls.pushAcquireFlucam.clicked.connect(self.acquire_flu_cam_dlg_handler)
        self.monoControls.pushAcquireGifCamera.clicked.connect(self.acquire_gif_cam_dlg_handler)
        self.monoControls.pushCenterOnGif.clicked.connect(self.center_on_gif_dlg_handler)

        # Pre-conditions
        self.monoControls.pushPresets.clicked.connect(self.presets_dlg_handler)
        self.monoControls.pushFindBeam.clicked.connect(self.find_beam_dlg_handler)

        # Setup beam
        self.monoControls.pushCenterOnFlucam.clicked.connect(self.center_on_flucam_dlg_handler)
        self.monoControls.pushFocusAtSlit.clicked.connect(self.focus_at_slit_dlg_handler)

        # Excitation
        self.monoControls.pushSetExcitation.clicked.connect(self.rampauto_tune_dlg_handler)

        # Tune
        self.monoControls.pushAutoTune.clicked.connect(self.auto_tune_dlg_handler)
        self.monoControls.pushCalibrateDeflections.clicked.connect(
            self.calibrate_deflections_dlg_handler)
        self.monoControls.pushCalibrateFocus.clicked.connect(self.calibrate_focus_dlg_handler)
        self.monoControls.pushTuneStigmators.clicked.connect(self.tune_coarse_dlg_handler)
        self.monoControls.pushFineTuneMStigX.clicked.connect(self.tune_stig_x_dlg_handler)
        self.monoControls.pushFineTuneMStigY.clicked.connect(self.tune_stig_y_dlg_handler)
        self.monoControls.pushTuneGifFocusX.clicked.connect(self.tune_gif_focus_x_dlg_handler)
        self.monoControls.pushTuneGifFocusY.clicked.connect(self.tune_gif_focus_y_dlg_handler)

        self.monoCalibrationControls.pushCalibrate.clicked.connect(self.calibrate_dlg_handler)
        self.monoCalibrationControls.pushTestCalibrate.clicked.connect(
            self.test_calibrate_dlg_handler)

        if not self.settings.flucam_or_service_cam_present:
            self.monoControls.pushAcquireFlucam.setEnabled(False)
            self.monoControls.groupBox_CalibrateMonochromator.setEnabled(False)
            self.monoControls.pushCenterOnFlucam.setEnabled(False)
            self.monoControls.pushCenterOnGif.setEnabled(False)
            self.monoControls.pushTuneGifFocusX.setEnabled(False)
            self.monoControls.pushTuneGifFocusY.setEnabled(False)
            self.monoControls.pushAutoTune.setEnabled(False)
            self.monoControls.pushTuneStigmators.setEnabled(False)
            self.monoControls.pushFineTuneMStigX.setEnabled(False)
            self.monoControls.pushFineTuneMStigY.setEnabled(False)
            self.monoCalibrationControls.pushCalibrate.setEnabled(False)
            self.monoCalibrationControls.pushTestCalibrate.setEnabled(False)
            self.monoControls.pushFocusAtSlit.setEnabled(False)

        if not self.settings.energy_filter_present:
            self.monoControls.pushAcquireGifCamera.setEnabled(False)
            self.monoControls.pushTuneGifFocusX.setEnabled(False)
            self.monoControls.pushTuneGifFocusY.setEnabled(False)
            self.monoControls.pushFineTuneMStigX.setEnabled(False)
            self.monoControls.pushCenterOnGif.setEnabled(False)
            self.monoControls.pushAutoTune.setEnabled(False)

        if not self.settings.monochromator:
            self.monoControls.pushFineTuneMStigX.setEnabled(False)
            self.monoControls.pushFineTuneMStigY.setEnabled(False)
            self.monoControls.pushAutoTune.setEnabled(False)
            self.monoControls.pushCenterOnFlucam.setEnabled(False)
            self.monoControls.pushCenterOnGif.setEnabled(False)
            self.monoControls.pushFindBeam.setEnabled(False)
            self.monoControls.pushTuneStigmators.setEnabled(False)
            self.monoControls.pushTuneGifFocusX.setEnabled(False)
            self.monoControls.pushTuneGifFocusY.setEnabled(False)
            self.monoCalibrationControls.pushCalibrate.setEnabled(False)
            self.monoCalibrationControls.pushTestCalibrate.setEnabled(False)
            self.monoControls.pushFocusAtSlit.setEnabled(False)
            self.monoControls.groupBox_Excitation.setEnabled(False)

    def _init_optistem_controls(self):
        self.optiStemCalibrationControls.pushCalibrateC1.clicked.connect(self.optistem_calibrate_c1_dlg_handler)
        self.optiStemCalibrationControls.pushCalibrateA1.clicked.connect(self.optistem_calibrate_a1_dlg_handler)
        self.optiStemCalibrationControls.pushCalibrateAll.clicked.connect(self.optistem_calibrate_all_dlg_handler)
        self.optiStemCalibrationControls.pushTrainA1C1.clicked.connect(self.optistem_train_a1c1_dlg_handler)
        self.optiStemCalibrationControls.pushTrainA2.clicked.connect(self.optistem_train_a2_dlg_handler)
        self.optiStemCalibrationControls.pushTrainB2.clicked.connect(self.optistem_train_b2_dlg_handler)
        self.optiStemCalibrationControls.pushOutputCalibrationAndTrainingData.clicked.connect(
            self.optistem_output_calibration_and_training_data_handler)
        self.optiStemCalibrationControls.pushWienA2r.clicked.connect(
            lambda: self.optistem_acquire_wien_dlg_handler("a2r"))
        self.optiStemCalibrationControls.pushWienA2i.clicked.connect(
            lambda: self.optistem_acquire_wien_dlg_handler("a2i"))
        self.optiStemCalibrationControls.pushWienB2r.clicked.connect(
            lambda: self.optistem_acquire_wien_dlg_handler("b2r"))
        self.optiStemCalibrationControls.pushWienB2i.clicked.connect(
            lambda: self.optistem_acquire_wien_dlg_handler("b2i"))
        self.optiStemCalibrationControls.bar_wiener_constant.valueChanged.connect(
            lambda: self._on_slider_position_change(
                self.optiStemCalibrationControls.bar_wiener_constant,
                                                    self.optiStemCalibrationControls.Edit_wiener_constant))
        self.optiStemCalibrationControls.bar_wiener_constant.sliderReleased.connect(
            self.optistem_update_wien_dlg_handler)
        self.optiStemCalibrationControls.bar_wiener_constant.installEventFilter(SliderEventFilter(self))
        self.optiStemCalibrationControls.bar_wiener_constant.actionTriggered.connect(
            lambda action: self._on_slider_action(
                action, self.optiStemCalibrationControls.bar_wiener_constant,
                self.optiStemCalibrationControls.Edit_wiener_constant))
        self.optiStemCalibrationControls.Edit_wiener_constant.editingFinished.connect(
            lambda: self._on_slider_value_change(
                self.optiStemCalibrationControls.bar_wiener_constant,
                self.optiStemCalibrationControls.Edit_wiener_constant))
        self.optiStemControls.pushTuneA1C1.clicked.connect(self.optistem_tune_a1c1_dlg_handler)
        self.optiStemControls.pushTuneAll.clicked.connect(self.optistem_tune_all_dlg_handler)

    def _on_slider_action(self, action, slider, value):
        if action in [QAbstractSlider.SliderSingleStepAdd, QAbstractSlider.SliderSingleStepSub,
                      QAbstractSlider.SliderPageStepAdd, QAbstractSlider.SliderPageStepSub]:
            self._on_slider_position_change(slider, value)
            self.optistem_update_wien_dlg_handler()

    def _on_slider_value_change(self, slider, value):
        # Update the slider position based on the manual value entered
        # (which is restricted to the slider range via a validator).
        # Not called when the text is changed programmatically (via the slider),
        # so the signals will not keep going back and forth.
        slider.setValue(int(float(value.text())))
        self.optistem_update_wien_dlg_handler()

    def _on_slider_position_change(self, slider, value):
        # Update the slider value text while the slider is being dragged.
        # It will be effectuated when the slider is released.
        value.setText(str(slider.sliderPosition()))

    def _init_panes(self):
        """ Ensure the tasks Pane ends up on the left side and the results pane on the right side.
            Set the controls on top of the settings.
            Aligning Tasks to the top of the tasks Pane.
        """
        self.splitDockWidget(self.tasksDock, self.controlsDock, Qt.Horizontal)
        self.splitDockWidget(self.controlsDock, self.settingsDock, Qt.Vertical)

        # Qt-bug: Don't use setFixedWidth or the vertical separator between docks will disappear (i.s.o. the horizontal one)
        self.controlsDock.setMinimumWidth(374)
        self.settingsDock.setMinimumWidth(374)
        self.controlsDock.setMaximumWidth(375)
        self.settingsDock.setMaximumWidth(375)

        # Tasks
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.taskBarLayout.addItem(spacer)
        self.tasksDock.setFixedWidth(2 * self._getMaxTaskWidth())
        self.tasksDock.setMinimumHeight(2 * self._getMaxTaskHeight())

        # Warning: We cannot use a fixed size central widget (e.g. for the taskbar) as a resize of the mainwindow will
        #          always result in a resize of the central widget. SetFixedWidth, resize, setgeometry etc. will
        #          not work (QTBUG - 7631)

    def reset_settings_pane(self, pane):
        reset_settings_pane(pane)

    def update_ht(self):
        # TODO: Decouple
        update_ht_handler(self)

    def initialize(self):
        """ Initialize the logic layer
        """
        init_app_logic(self)  # Initialize the dialog_handler

        self._init_mono_controls()
        self._init_optistem_controls()

        # Create the model that will drive the UI tree control, it is built based on configuration
        # information in Settings object.
        procedure = create_tree_control_items(self.settings)
        self._model = QTaskModel(procedure)
        self.treeView.setModel(self._model)
        self.treeView.setSelectionMode(QAbstractItemView.SingleSelection)
        self.treeView.expandAll()

        self.treeView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.treeView.customContextMenuRequested.connect(self._on_open_context_menu)

    def close_dialog(self):
        close_dialog(self)

    def finalize(self):
        finalize(self)

    def add_img_to_report(self, image, location):
        add_img_to_report(self, image, location)

    def add_text_to_report(self, info, level=0):
        add_text_to_report(self, info, level=0)

    def _initiate_task(self, callable_handler, qtask=None):
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        callable_handler(qtask, self)
        QApplication.restoreOverrideCursor()

    def acquire_flu_cam_dlg_handler(self):
        self._initiate_task(
            acquire_flu_cam_dlg_handler)  # self._model.root_task.get_from_name(NAME_TASK_ACQUIRE_ON_FLUCAM)

    def acquire_gif_cam_dlg_handler(self):
        self._initiate_task(
            acquire_gif_cam_dlg_handler)  # self._model.root_task.get_from_name(NAME_TASK_ACQUIRE_ON_GIF_CCD)

    def center_on_gif_dlg_handler(self):
        self._initiate_task(center_beam_dlg_handler)  # self._model.root_task.get_from_name(NAME_TASK_CENTER_BEAM)

    def presets_dlg_handler(self):
        self._initiate_task(presets_dlg_handler, self._model.root_task.get_from_name(NAME_TASK_PRESETS))

    def find_beam_dlg_handler(self):
        self._initiate_task(find_beam_full_dlg_handler, self._model.root_task.get_from_name(NAME_TASK_FIND_BEAM_FULL))

    def center_on_flucam_dlg_handler(self):
        self._initiate_task(coarse_center_on_flucam_dlg_handler,
                            self._model.root_task.get_from_name(NAME_TASK_CENTER_ON_FLUCAM))

    def focus_at_slit_dlg_handler(self):
        self._initiate_task(
            step_1_3_focus_at_slit_dlg_handler)  # self._model.root_task.get_from_name(NAME_TASK_FOCUS_AT_SLIT)

    def rampauto_tune_dlg_handler(self):
        self._initiate_task(ramp_to_excitation_dlg_handler,
                            self._model.root_task.get_from_name(NAME_TASK_RAMP_TO_EXCITATION))

    def auto_tune_dlg_handler(self):
        self._initiate_task(auto_tune_flu_cam_and_gif_dlg_handler,
                            self._model.root_task.get_from_name(NAME_TASK_TUNE_MONO))

    def calibrate_deflections_dlg_handler(self):
        self._initiate_task(
            step_3_1_calibrate_monochromator_dlg_handler)  # self._model.root_task.get_from_name(NAME_TASK_CALIBRATE_MONOCHROMATOR)

    def calibrate_focus_dlg_handler(self):
        self._initiate_task(
            step_3_4_calibrate_gunlens_vs_MonoStigX_dlg_handler)  # self._model.root_task.get_from_name(NAME_TASK_CALIBRATE_GUNLENS_V_MONOSTIGX)

    def tune_coarse_dlg_handler(self):
        self._initiate_task(tune_coarse_dlg_handler, self._model.root_task.get_from_name(NAME_TASK_TUNE_COARSE))

    def tune_stig_x_dlg_handler(self):
        self._initiate_task(tune_stig_x_dlg_handler, self._model.root_task.get_from_name(NAME_TASK_TUNE_MONO_STIG_X))

    def tune_stig_y_dlg_handler(self):
        self._initiate_task(tune_stig_y_dlg_handler, self._model.root_task.get_from_name(NAME_TASK_TUNE_MONO_STIG_Y))

    def tune_gif_focus_x_dlg_handler(self):
        self._initiate_task(tune_gif_focus_x_dlg_handler,
                            self._model.root_task.get_from_name(NAME_TASK_TUNE_GIF_FOCUS_X))

    def tune_gif_focus_y_dlg_handler(self):
        self._initiate_task(tune_gif_focus_y_dlg_handler,
                            self._model.root_task.get_from_name(NAME_TASK_TUNE_GIF_FOCUS_Y))

    def calibrate_dlg_handler(self):
        self._initiate_task(
            calibrate_dlg_handler)  # self._model.root_task.get_from_name(NAME_TASK_CALIBRATE_MONO_EFFECTS)

    def test_calibrate_dlg_handler(self):
        self._initiate_task(test_calibrate_dlg_handler)  # self._model.root_task.get_from_name(NAME_TASK_TEST_CALIBRATE)

    def undo_dlg_handler(self):
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        undo_dlg_handler(self)
        QApplication.restoreOverrideCursor()

    def redo_dlg_handler(self):
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        redo_dlg_handler(self)
        QApplication.restoreOverrideCursor()

    def stop_dlg_handler(self):
        stop_dlg_handler(self)

    def optistem_calibrate_c1_dlg_handler(self):
        self._initiate_task(optistem_calibrate_c1_dlg_handler)

    def optistem_calibrate_a1_dlg_handler(self):
        self._initiate_task(optistem_calibrate_a1_dlg_handler)

    def optistem_calibrate_all_dlg_handler(self):
        self._initiate_task(optistem_calibrate_all_dlg_handler)

    def optistem_train_a1c1_dlg_handler(self):
        self._initiate_task(optistem_train_a1c1_dlg_handler)

    def optistem_train_a2_dlg_handler(self):
        self._initiate_task(optistem_train_a2_dlg_handler)

    def optistem_train_b2_dlg_handler(self):
        self._initiate_task(optistem_train_b2_dlg_handler)

    def optistem_tune_a1c1_dlg_handler(self):
        self._initiate_task(optistem_tune_a1c1_dlg_handler)

    def optistem_tune_all_dlg_handler(self):
        self._initiate_task(optistem_tune_all_dlg_handler)

    def optistem_output_calibration_and_training_data_handler(self):
        self._initiate_task(optistem_output_calibration_and_training_data_handler)

    def optistem_acquire_wien_dlg_handler(self, coeff):
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        qtask = None
        optistem_acquire_wien_dlg_handler(qtask, self, coeff)
        QApplication.restoreOverrideCursor()

    def optistem_update_wien_dlg_handler(self):
        self._initiate_task(optistem_update_wien_dlg_handler)

    def enable_dlg(self, enable):
        self.topDock.setEnabled(enable)
        self.tasksDock.setEnabled(enable)
        self.controlsDock.setEnabled(enable)
        self.settingsDock.setEnabled(enable)

        if hasattr(self, 'actionUndo'):
            self.actionUndo.setEnabled(enable and (len(self.undo_stack) > 0))
        if hasattr(self, 'actionRedo'):
            self.actionRedo.setEnabled(enable and (len(self.redo_stack) > 0))

    def _on_task_state_change(self, task_id, new_state_int):
        """ Task state change -> update UI.

        :param task_id: int, unique task ID.
        :param new_state_int: new state of task (as int).
        """
        new_state = TaskStatus.to_enum(new_state_int)
        logger.info('task state change signal received, id (%s), state change -> %s',
                    task_id, new_state)

        self.refresh_tree_view(task_id)

        # If finalizing after failure takes too long (like abort) this is the place to
        # perform early detection.
        # if new_state_int == TaskStatus.Failed:
        #    self._set_systemstatus(SystemStatus.Failed)

    def _on_open_context_menu(self, position):
        """ Handle request for context menu -> configure and display it.

        Show a context menu providing 'run selected', 'clear_history', and 'run_all actions' that
        can then be selected by the user.
        :param position: ???TODO?
        """
        # Get QModelIndex of selection on UI, this allows access to underlying model data.
        indexes = self.treeView.selectedIndexes()
        if len(indexes) != 1 or not indexes[0].isValid():
            return

        qtask = indexes[0].internalPointer()  # access the actual QTask

        menu = QMenu()

        action_run_selected = QAction('Run Selected', self)
        action_run_selected.triggered.connect(lambda: self._on_run_selected(qtask))

        action_clear_history = QAction('Clear History', self)
        action_clear_history.triggered.connect(self._on_clear_history)

        menu.addAction(action_run_selected)
        menu.addSeparator()
        menu.addAction(action_clear_history)

        if self._model.is_qtask_running:
            # Most tasks do not support cancel, these do.
            # TODO??? not a robust solution! cancel can be called from either - incorrect!
            if qtask.name in [NAME_TASK_CENTER_BEAM_SCREEN_CURRENT, NAME_TASK_FIND_BEAM_2]:
                action_run_selected.setText("Cancel")
            else:
                action_run_selected.setEnabled(False)
            action_clear_history.setEnabled(False)

        if not qtask.checked:
            action_run_selected.setEnabled(False)
            action_clear_history.setEnabled(False)

        logger.info('display context menu for task (%s)', qtask.id)
        menu.exec_(self.treeView.viewport().mapToGlobal(position))

    def _on_run_selected(self, qtask=None):
        """ Run the selected task. If None then get from current UI selection.

        :param qtask: the QTask to be executed.
        """
        if qtask is None:
            indexes = self.treeView.selectedIndexes()
            if len(indexes) != 1:
                logger.error('invalid selection in tree control: %s',
                             len(indexes))
                return

            qtask = indexes[0].internalPointer()  # access the actual QTask

        logger.info('execute task (%s)', qtask.id)
        qtask_id_to_executor[qtask.id](qtask, self)

    def _on_clear_history(self):
        """ Reset model (and hence the user interface view/s).
        """
        logger.info('reset UI model')
        self._model.reset()
        self.treeView.expandAll()  # by default the view is not expanded

    def _on_about(self):
        """ Open the about dialog
        """
        aboutDialog = AboutDialog(self)
        aboutDialog.exec_()

    def _on_user_manual(self):
        try:
            subprocess.Popen(HELP_FILE, shell=True)
        except OSError, e:
            # TODO: Debug only?
            pass

    def _init_general_settings_ui(self):
        self.settingsDialog = QDialog(self)
        self.settingsUi = GeneralSettingsGUI.Ui_GeneralSettings()
        self.settingsUi.setupUi(self.settingsDialog)
        self.settingsDialog.accepted.connect(lambda: update_settings_from_ui(self))
        self.settingsDialog.rejected.connect(lambda: update_settings_to_ui(self))

    def _on_general_settings(self):
        assert self.settingsDialog is not None
        self.settingsDialog.show()

    def _on_expert_mode_changed(self):
        self._set_expert_mode(self.actionExpertMode.isChecked())

    # TODO: Reapply filter
    def _on_warning_filter_changed(self):
        if self.warningCounter.isChecked():
            self.loggingStack.setCurrentWidget(self.filteredLoggingContent)
            self.warningCounter.setStyleSheet(BUTTON_ACTIVE_STYLE)
        else:
            self.loggingStack.setCurrentWidget(self.loggingContent)
            self.warningCounter.setStyleSheet(BUTTON_DEFAULT_STYLE)

    def _on_error_filter_changed(self):
        if self.errorCounter.isChecked():
            self.loggingStack.setCurrentWidget(self.filteredLoggingContent)
            self.errorCounter.setStyleSheet(BUTTON_ACTIVE_STYLE)
        else:
            self.loggingStack.setCurrentWidget(self.loggingContent)
            self.errorCounter.setStyleSheet(BUTTON_DEFAULT_STYLE)

    def _set_expert_mode(self, enabled=True):
        button = self.toolBar.widgetForAction(self.actionExpertMode)
        logger.info("{0} {1}".format("Expert Mode", "enabled" if enabled else "disabled"))
        button.setStyleSheet(BUTTON_ACTIVE_STYLE if enabled else BUTTON_DEFAULT_STYLE)
        if enabled:
            self.loggingStack.setCurrentWidget(self.loggingContent)
            self.categoryAdmin.reset_layout()
        else:
            self.loggingStack.setCurrentWidget(self.filteredLoggingContent)
            self.resultsStack.setCurrentWidget(self.finalResultContent)

    def _init_progressindicators(self):
        errorIcon = QIcon()
        errorIcon.addPixmap(QPixmap(":/Error"), QIcon.Normal, QIcon.Off)
        self.errorCounter = QToolButton()
        self.errorCounter.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.errorCounter.setIcon(errorIcon)
        self.errorCounter.setText("0")
        self.errorCounter.setCheckable(True)
        self.errorCounter.setVisible(False)
        self.errorCounter.setFixedHeight(24)
        self.statusBar.addPermanentWidget(self.errorCounter)

        warningIcon = QIcon()
        warningIcon.addPixmap(QPixmap(":/Warning"), QIcon.Normal, QIcon.Off)
        self.warningCounter = QToolButton()
        self.warningCounter.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.warningCounter.setIcon(warningIcon)
        self.warningCounter.setText("0")
        self.warningCounter.setCheckable(True)
        self.warningCounter.setVisible(False)
        self.errorCounter.setFixedHeight(24)
        self.statusBar.addPermanentWidget(self.warningCounter)

        self.progressBar = QProgressBar()
        self.progressBar.setProperty("value", 0)
        self.progressBar.setTextVisible(True)
        self.progressBar.setMaximumWidth(200)
        # Ensure the user experiences some form of initial progress
        # Reset must be used to show 'no progress'
        self.progressBar.setRange(5, 100)
        self.progressBar.setObjectName("progressBar")
        self.statusBar.addPermanentWidget(self.progressBar)

        self._set_systemstatus(SystemStatus.Idle)

    def _on_warning(self):
        self.warningCounter.setVisible(True)
        self.warningCounter.setText(str(int(self.errorCounter.text()) + 1))

    def _on_error(self):
        self.errorCounter.setVisible(True)
        self.errorCounter.setText(str(int(self.errorCounter.text()) + 1))

    def _set_systemstatus(self, status):
        # TODO: Store state (in model)
        self.progressBar.setStyleSheet(get_systemstate_style(status))
        self.progressBar.setFormat(status.name)

    def _on_start_run(self, isrevertable=True):
        self.statusBar.clearMessage()
        self.progressBar.reset()
        self.actionStop.setEnabled(True)
        self._set_systemstatus(SystemStatus.Running)
        self.enable_dlg(False)
        self._reset_pane_results(self.resultsStack)
        self._reset_pane_results(self.finalResult)
        self.warningCounter.setText("0")
        self.errorCounter.setText("0")
        self.warningCounter.setVisible(False)
        self.errorCounter.setVisible(False)

        # Regular tasks are revertable, undo and redo functions are not (undo cannot be undone, only via redo).
        if isrevertable:
            self.redo_stack = []

    def _reset_pane_results(self, pane):
        for child in pane.children():
            if isinstance(child, ResizingImage):
                child.resetPixmap()
            else:
                self._reset_pane_results(child)

    def _on_failure(self):
        self.actionStop.setEnabled(False)
        self._set_systemstatus(SystemStatus.Failed)
        self.progressBar.setValue(100)
        self.enable_dlg(True)
        QApplication.alert(self)
        self.statusBar.clearMessage()

    def _on_success(self):
        self.actionStop.setEnabled(False)
        self._set_systemstatus(SystemStatus.Passed)
        self.progressBar.setValue(100)
        self.enable_dlg(True)
        self.statusBar.clearMessage()

    def _set_input_validator_by_group(self, group, validator_type):
        for item in group.children():
            if isinstance(item, QLineEdit):
                if validator_type is IntType:
                    item.setValidator(QIntValidator())
                elif validator_type is FloatType:
                    item.setValidator(QDoubleValidator())
                else:
                    # No need for QRegExpValidator yet
                    raise Exception("Invalid input validator type")
            else:
                self._set_input_validator_by_group(item, validator_type)

    def _init_input_validation(self):
        self.settingsUi.Edit_log_level.setValidator(QIntValidator())

        # OptiMono
        self._set_input_validator_by_group(self.monoSettings.groupBox_flucam_settings, IntType)
        self._set_input_validator_by_group(self.monoSettings.groupBox_gifccd_settings, IntType)
        self.monoControls.Edit_TargetExcitation.setValidator(QDoubleValidator())

        # OptiSTEM
        self._set_input_validator_by_group(self.optiStemCalibrationControls, IntType)
        self._set_input_validator_by_group(self.optiStemCalibrationSettings, FloatType)
        self.optiStemCalibrationControls.Edit_wiener_constant.setValidator(
            QDoubleValidator(self.optiStemCalibrationControls.bar_wiener_constant.minimum(),
                             self.optiStemCalibrationControls.bar_wiener_constant.maximum(), 1))

    def _init_ui_signalhandlers(self):
        self.actionAbout.triggered.connect(self._on_about)
        self.actionUser_Manual.triggered.connect(self._on_user_manual)
        # self.actionConfig.triggered.connect(self._on_general_settings)
        self.actionExpertMode.triggered.connect(self._on_expert_mode_changed)
        self.warningCounter.clicked.connect(self._on_warning_filter_changed)
        self.errorCounter.clicked.connect(self._on_error_filter_changed)

        # Detect view menu selection changes
        self.actionToggleSettingsPane.triggered.connect(
            lambda: self._togglePane(self.actionToggleSettingsPane, self.settingsDock))
        self.actionToggleLogPane.triggered.connect(lambda: self._togglePane(
            self.actionToggleLogPane, self.logDock))
        self.actionResetLayout.triggered.connect(lambda: self._restoreWindowArrangement(
            "Defaults"))

        # Detect closing of view docks
        self.settingsDock.visibilityChanged.connect(
            lambda: self._togglePaneMenu(self.actionToggleSettingsPane, self.settingsDock))
        self.logDock.visibilityChanged.connect(lambda: self._togglePaneMenu(
            self.actionToggleLogPane, self.logDock))

        # Align menu and docks
        self._togglePaneMenu(self.actionToggleSettingsPane, self.settingsDock)
        self._togglePaneMenu(self.actionToggleLogPane, self.logDock)

        # Detect category selection
        self.categoryTabs.currentChanged.connect(self._on_category_selection)

        # Logging
        self.copyLoggingButton.clicked.connect(self._on_copy_logging)
        self.clearLoggingButton.clicked.connect(self._on_clear_logging)

    def _on_clear_logging(self):
        self.loggingText.clear()
        self.filteredLoggingText.clear()
        self.warningCounter.setText("0")
        self.errorCounter.setText("0")
        # TODO: Subclass QToolButton to change visibility based on setText.
        self.warningCounter.setVisible(False)
        self.errorCounter.setVisible(False)
        if self.progressBar.text() in [str(SystemStatus.Passed), str(SystemStatus.Failed)]:
            self.progressBar.reset()
            self._set_systemstatus(SystemStatus.Idle)

    def _on_copy_logging(self):
        if self.actionExpertMode.isChecked():
            logging_text = self.loggingText
        else:
            logging_text = self.filteredLoggingText
        logging_text.selectAll()
        logging_text.copy()
        logging_text.textCursor().clearSelection()

    def highlight_errors(self):
        selections = []
        selection = QTextEdit.ExtraSelection
        selection.cursor = QTextCursor(self.loggingText.document())
        selection.cursor.setPosition(0)
        selection.cursor.setPosition(10, QTextCursor.KeepAnchor)

        highlightFormat = QTextCharFormat()
        highlightFormat.setForeground(Qt.darkMagenta)
        highlightFormat.setFontWeight(QFont.Bold)
        highlightFormat.setBackground(QBrush(Qt.yellow))
        selection.format = highlightFormat
        selections.append(selection)
        self.loggingText.setExtraSelections(selections)

    # TODO: Move to factory
    def _init_category_admin(self):
        self.categoryAdmin = CategoryAdministration()

        # Categories, Tasks and the allowed panes
        autofunctions_tasks = []

        ts = TemService(use_omp=False, use_tem_access=True)  # we can not use self.ts yet, because initialize is not yet called

        if ts.configuration.is_monochromator():
            if is_licensed(ts, LICENSE_CODE_MONO_AUTOTUNE_FEATURE):
                autofunctions_tasks.append('OptiMono')
            else:
                logger.info('OptiMono not licensed')

        if is_licensed(ts, LICENSE_CODE_STEM_AFS_FEATURE) or \
                is_licensed(ts, LICENSE_CODE_STEM_2ND_ORDER_CORR_FEATURE):
            autofunctions_tasks.append('OptiSTEM')
        else:
            logger.info('AFS not licensed')

        if not is_licensed(ts, LICENSE_CODE_STEM_2ND_ORDER_CORR_FEATURE):
            logger.info('OptiSTEM A2/B2 not licensed')
            self.optiStemControls.pushTuneAll.hide()

        if len(autofunctions_tasks) > 0:
            self.categoryAdmin.add_category('Auto Functions', autofunctions_tasks,
                                            [self.settingsDock, self.controlsDock, self.logDock])

            # Task pane content (layouts)
            if 'OptiMono' in autofunctions_tasks:
                for container, layout in [(self.settingsStack, self.monoSettingsContent),
                                          (self.controlsStack, self.monoControlsContent),
                                          (self.resultsStack, self.monoResultsContent)]:
                    self.categoryAdmin.set_layout('Auto Functions', 'OptiMono', container, layout)

            if 'OptiSTEM' in autofunctions_tasks:
                for container, layout in [(self.settingsStack, self.optiStemSettingsContent),
                                          (self.controlsStack, self.optiStemControlsContent),
                                          (self.resultsStack, self.optiStemResultsContent)]:
                    self.categoryAdmin.set_layout('Auto Functions', 'OptiSTEM', container, layout)

        if is_user_in_group(privileged_users):
            if ts.configuration.is_monochromator():
                self.categoryAdmin.add_category('Service/Factory', ['OptiMono', 'OptiSTEM'],
                                                [self.settingsDock, self.controlsDock, self.logDock])
            else:
                self.categoryAdmin.add_category('Service/Factory', ['OptiSTEM'],
                                                [self.settingsDock, self.controlsDock, self.logDock])
            if ts.configuration.is_monochromator():
                for container, layout in [(self.settingsStack, self.TBDSettingsContent),
                                          (self.controlsStack, self.monoCalibrationControlsContent),
                                          (self.resultsStack, self.monoResultsContent)]:
                    self.categoryAdmin.set_layout('Service/Factory', 'OptiMono', container, layout)

            for container, layout in [(self.settingsStack, self.optiStemCalibrationSettingsContent),
                                      (self.controlsStack, self.optiStemCalibrationControlsContent),
                                      (self.resultsStack, self.optiStemCalibrationResultsContent)]:
                self.categoryAdmin.set_layout('Service/Factory', 'OptiSTEM', container, layout)

    def _create_category_pane(self):
        # Remove the title of the dock
        self.topDock.setTitleBarWidget(QWidget())

        for categoryName, _ in self.categoryAdmin.iteritems():
            tab = QWidget()
            tab.setObjectName("categoryTab_{0}".format(categoryName))
            self.categoryTabs.addTab(tab, "")
            self.categoryTabs.setTabText(self.categoryTabs.indexOf(tab),
                                         QApplication.translate("mainWindow", categoryName, None,
                                                                QApplication.UnicodeUTF8))

    def _init_category_selection(self):
        """ Explicitly activate the first Category.
            This is the default (and therefore _on_category_selection is not triggered), but don't rely on defaults.
            Traverse all Categories to ensure defaults initialisation.
        """
        for i in reversed(range(self.categoryTabs.count())):
            self.categoryTabs.setCurrentIndex(i)
        self._on_category_selection()

    def _create_categorytaskbutton(self, name):
        taskButton = QPushButton(self.taskDockContents)
        taskButton.setObjectName(
            "taskButton_{0}".format(self._to_qt_friendly_objectname(name)))  # objectName: no spaces allowed
        taskButton.setText(QApplication.translate("mainWindow", name, None, QApplication.UnicodeUTF8))
        return taskButton

    def _getMaxTaskWidth(self):
        return QFontMetrics(QPushButton().font()).width(self.categoryAdmin.longest_task_name())

    def _getMaxTaskHeight(self):
        return QFontMetrics(QPushButton().font()).height() * self.categoryAdmin.max_nof_tasks()

    def _to_qt_friendly_objectname(self, name):
        return ''.join(character for character in name if character.isalnum())

    def _on_category_selection(self):
        """ Handle user Category selection.
            Instead of monitoring many change events, this defined moment in time is used
            to store any changes in the active Category, before effectuating the new selection.

            Triggers:
            1) Application launch
            2) Category selection by user

            Actions:
            1) Save dock customizations of the previous category
            2) Load the Category specific docks (taking into account user customization)
            3) Load the Category specific Tasks.
            4) Restore any previous Task selection
        """
        self.categoryAdmin.set_window_state(self.saveState())
        self._clear_task_dock()

        selectedCategory = self.categoryTabs.tabText(self.categoryTabs.currentIndex())
        self.categoryAdmin.set_active_category(selectedCategory)

        # Refill the taskDock based on the category selection.
        # Tasks are inserted at the front such that no involvement with the Spacer is needed.
        persistentTaskButton = None
        for taskName in reversed(self.categoryAdmin.active_category_tasks()):
            newTaskButton = self._create_categorytaskbutton(taskName)
            self.taskBarLayout.insertWidget(0, newTaskButton)
            # Note: lambda always sends the last task used. Therefore using partial.
            newTaskButton.clicked.connect(partial(self._on_task_selection, taskName))
            if taskName is self.categoryAdmin.active_task():
                persistentTaskButton = newTaskButton
        # Align to the top. The spacer ensures that count is never 0.
        self.taskBarLayout.setStretch(self.taskBarLayout.count() - 1, 1)

        # Restore the last task selection in this category.
        # If there is no persistent Task nothing was or will be selected.
        if persistentTaskButton is None:
            self._reset_layouts()
        else:
            self._on_task_selection(self.categoryAdmin.active_task())
        windowState = self.categoryAdmin.window_state()
        if windowState is not None:
            self.restoreState(windowState)

    def _restore_docks(self):
        activeCategory = self.categoryAdmin.active_category()
        if activeCategory is not None:
            for dock in activeCategory.allowedDocks:
                dock.setVisible(True)

    def _clear_task_dock(self):
        # isEmpty is not counting spacers, so using count
        while self.taskBarLayout.count() > 1:
            oldTaskButton = self.taskBarLayout.takeAt(0)
            if isinstance(oldTaskButton, QWidgetItem):
                oldTaskButton.widget().deleteLater()
                # else: Not removing the Spacer

    # Events:
    # 1) User Category selection (restore previous task selection)
    # 2) User Task selection
    # Actions:
    # 1) Load the Task specific layouts (dock content)
    # 2) Store the selected Task
    def _on_task_selection(self, taskName):
        # Reset stylesheet of previous selection
        # TODO: Category-specific strategy. Multiple Tasks can be selected in the Workflows Category,
        #       so multiple items will stay highlighted.
        taskButtons = (self.taskBarLayout.itemAt(i) for i in range(self.taskBarLayout.count()))
        for taskButton in taskButtons:
            if taskButton.widget():
                if taskButton.widget().text() == taskName:
                    taskButton.widget().setStyleSheet(TASK_ACTIVE_STYLE)
                else:
                    taskButton.widget().setStyleSheet(TASK_INACTIVE_STYLE)

        self.categoryAdmin.set_active_task(taskName)
        if not self.actionExpertMode.isChecked():
            self.resultsStack.setCurrentWidget(self.finalResultContent)

    def _reset_layouts(self):
        self.settingsStack.setCurrentWidget(self.TBDSettingsContent)
        self.controlsStack.setCurrentWidget(self.TBDControlsContent)
        self.resultsStack.setCurrentWidget(self.TBDResultsContent)
        # TODO: The tree view (no need for a stack)

    # TODO: The dimensions of a pane are not correctly restored when the pane is disabled during application close.
    def _storeWindowArrangement(self, arrangementName):
        """ Write persistent data, being:
            1) The overall application geometry
            2) The window state per category (includes geometry of dockwidgets and taskbars)
            3) Dock state
            Note that saveState on MainWindow level only saves and restores the Active Category.
            Therefore the CategoryAdmin is used.

            @precondition: self.categoryAdmin is not None

            @postcondition: -
        """
        # MainWindow
        settingName = arrangementName + "/mainView/geometry"
        self.uiSettings.setValue(settingName, self.saveGeometry())

        # Categories
        for categoryName, category in self.categoryAdmin.iteritems():
            settingName = "{name}/{category}/saveState".format(name=arrangementName,
                                                               category=self._to_qt_friendly_objectname(categoryName))
            self.uiSettings.setValue(settingName, self.categoryAdmin.window_state(categoryName))

        # Docks
        # TODO: To be moved to Persistency mechanism
        for child in self.children():
            if isinstance(child, QDockWidget):
                for categoryName, category in self.categoryAdmin.iteritems():
                    if self.categoryAdmin.pane_allowed(categoryName, child.windowTitle()):
                        settingsBaseName = "{name}/{category}/{dock}/".format(name=arrangementName,
                                                                              category=self._to_qt_friendly_objectname(
                                                                                  categoryName),
                                                                              dock=child.windowTitle())
                        # settingName = settingsBaseName + "geometry"
                        # self.uiSettings.setValue(settingName, self.categoryAdmin.pane_geometry(categoryName, child.windowTitle()))
                        settingName = settingsBaseName + "enabled"
                        self.uiSettings.setValue(settingName, str(
                            self.categoryAdmin.pane_visible(categoryName, child.windowTitle())))

        self.uiSettings.sync()

    def _restoreWindowArrangement(self, arrangementName):
        """ Load persistent data.

            @precondition: self.categoryAdmin is not None

            @postcondition: -

        """
        # MainWindow
        # Note: saveState contains the state of taskbars and docks.
        #       Therefore this must be restored before the dock customization.
        settingName = arrangementName + "/mainView/geometry"
        if self.uiSettings.contains(settingName):
            self.restoreGeometry(self.uiSettings.value(settingName))

        # Categories
        for categoryName, category in self.categoryAdmin.iteritems():
            settingName = "{name}/{category}/saveState".format(name=arrangementName,
                                                               category=self._to_qt_friendly_objectname(categoryName))
            if self.uiSettings.contains(settingName):
                self.categoryAdmin.set_window_state(self.uiSettings.value(settingName), categoryName)

        # Docks
        # TODO: To be moved to the Persistency mechanism.
        for child in self.children():
            if isinstance(child, QDockWidget):
                for categoryName, category in self.categoryAdmin.iteritems():
                    if self.categoryAdmin.pane_allowed(categoryName, child.windowTitle()):
                        settingsBaseName = "{name}/{category}/{dock}/".format(name=arrangementName,
                                                                              category=self._to_qt_friendly_objectname(
                                                                                  categoryName),
                                                                              dock=child.windowTitle())
                        settingName = settingsBaseName + "enabled"
                        if self.uiSettings.contains(settingName):
                            # Note: False was not detected by usage of QVariant bool. Therefore converting to string.
                            self.categoryAdmin.set_pane_visible(categoryName, child.windowTitle(),
                                                                self.uiSettings.value(settingName) == str(True))

    # Update view visibility based on menu selection
    def _togglePane(self, viewMenu, dockWidget):
        dockWidget.setVisible(viewMenu.isChecked())

    # Update menu selection when a view is being closed
    def _togglePaneMenu(self, viewMenu, dockWidget):
        viewMenu.setChecked(dockWidget.isVisible())

    def closeEvent(self, event):
        close_dlg_handler(self, event)

    def show_warning(self, message):
        """ Show an application level warning for non-fatal events for which the logging pane is insufficient
            (e.g. because the user is able to close it).
        """
        msgBox = QMessageBox(flags=Qt.Dialog | Qt.MSWindowsFixedSizeDialogHint | Qt.WindowStaysOnTopHint)
        msgBox.warning(self, "Sherpa warning", message)

    def store_window_customization(self):
        self.categoryAdmin.set_window_state(self.saveState())
        self.categoryAdmin.sync()
        self._storeWindowArrangement("Customization")

    def mousePressEvent(self, _):
        # Kludge to allow de-selection from tree view -> need to click on main window (i.e. not
        # in tree view or group box).
        self.treeView.clearSelection()

    def refresh_tree_view(self, task_id):
        """ Update the part of the tree view associated with the supplied
        task.

        Public for client code that runs on the UI thread -> no need for
        signal/slot mechanism.
        :param task_id: int
        """
        root_index = self._model.index(0, 0, None)
        # Get the QModelIndex of the supplied task, get first match and search at all levels.
        # See 'QTaskModel' method 'data' for use of 'UserRole'.
        indices = self._model.match(root_index, Qt.UserRole, task_id, 1, Qt.MatchRecursive)

        if len(indices) == 1:
            # Signal updating of the appropriate part of the UI model.
            self._model.dataChanged.emit(indices[0], indices[0])
        else:
            logger.error('unexpected number of task indices, ignore and continue')
