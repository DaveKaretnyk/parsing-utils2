# Copyright (c) 2012-2016 by FEI Company
# All rights reserved. This file includes confidential and proprietary
# information of FEI Company.
import time
import logging

from fei.tem.omp.api import StigmatorType, ColumnOperatingMode, MagnificationSubMode


logger = logging.getLogger(__name__)


class OpticsControl(object):
    def __init__(self, omp_worker, column=None, tem_access=None):
        super(OpticsControl, self).__init__()
        self.omp_worker = omp_worker
        self.column = column
        self.optics = self.column.get_optics()
        self._beam_deflector = None
        self._gun_deflector = None
        self._beam_deflector_alignments = None
        self._gun_deflector_alignments = None
        self.tem_access_control = None
        if tem_access is not None:
            self.tem_access_control = tem_access.TemAccessControl

        stigmators = self.omp_worker.execute_on_worker(
            lambda: self.optics.get_stigmators(),
            "lambda: self.optics.get_stigmators()")
        self._lenses = self.omp_worker.execute_on_worker(
            lambda: self.optics.get_lenses(),
            "lambda: self.optics.get_lenses()")
        self._condenser_stigmator = self.omp_worker.execute_on_worker(
            lambda: stigmators.get(StigmatorType.condenser_stigmator),
            "lambda: stigmators.get(StigmatorType.condenser_stigmator)"                                                                      )
        self._condenser_stigmator_3fold = self.omp_worker.execute_on_worker(
            lambda: stigmators.get(StigmatorType.condenser_stigmator_3_fold),
            "lambda: stigmators.get(StigmatorType.condenser_stigmator_3_fold)")
        self._coma_stigmator = self.omp_worker.execute_on_worker(
            lambda: stigmators.get(StigmatorType.coma_stigmator),
            "lambda: stigmators.get(StigmatorType.coma_stigmator)")
            # will use probe_corrector_b2_stigmator or Align_BT

        self._initialize_deflectors()

    def __del__(self):
        logger.info("OMP OpticsControl destructor")
        self.omp_worker = None

    def disconnect(self):
        logger.info("OMP OpticsControl disconnect")
        self.omp_worker.execute_on_worker(
            lambda: self._release_objects(),
            "lambda: self._release_objects()")

    def _release_objects(self):
        self._gun_deflector_alignments = None
        self._gun_deflector = None
        self._beam_deflector_alignments = None
        self._beam_deflector = None
        self._condenser_stigmator_3fold = None
        self._condenser_stigmator = None
        self._coma_stigmator = None
        self.optics = None
        self.column = None

    def _initialize_deflectors(self):
        deflectors = self.omp_worker.execute_on_worker(
            lambda: self.optics.get_deflectors(),
            description="lambda: self.optics.get_deflectors()")
        self._beam_deflector = self.omp_worker.execute_on_worker(
            lambda: deflectors.get_beam_dc_deflector(),
            description="lambda: deflectors.get_beam_dc_deflector()")
        self._beam_deflector_alignments = self.omp_worker.execute_on_worker(
            lambda: self._beam_deflector.get_alignments(),
            description="lambda: self._beam_deflector.get_alignments()")

        # TODO omp gun_deflector = deflectors.Item(iom.enDeflector.enDeflector_GunDcDeflector)
        #self._gun_deflector = gun_deflector.QueryInterface(iom.IGunDcDeflector)
        #self._gun_deflector_alignments = self._gun_deflector.Alignments

    def set_defocus_m(self, defocus_m, stabilisation_delay=0.2):
        self.omp_worker.execute_on_worker(
            lambda: self.optics.set_defocus(defocus_m),
            "lambda: self.optics.set_defocus(defocus_m)")
        time.sleep(stabilisation_delay)

    def get_defocus_m(self):
        return self.omp_worker.execute_on_worker(
            lambda: self.optics.get_defocus(),
            "lambda: self.optics.get_defocus()")

    def set_condenser_stigmator(self, x, y):
        vector_value = self.omp_worker.execute_on_worker(
            lambda: self._condenser_stigmator.get_input_value(),
            "lambda: self._condenser_stigmator.get_input_value()")
        vector_value.x = x
        vector_value.y = y
        self.omp_worker.execute_on_worker(
            lambda: self._condenser_stigmator.set_input_value(vector_value),
            "lambda: self._condenser_stigmator.set_input_value(vector_value)")

    def get_condenser_stigmator(self):
        vector_value = self.omp_worker.execute_on_worker(
            lambda: self._condenser_stigmator.get_input_value(),
            "lambda: self._condenser_stigmator.get_input_value()")
        return vector_value.x, vector_value.y

    def change_condenser_stigmator(self, delta_x, delta_y):
        x, y = self.get_condenser_stigmator()
        x += delta_x
        y += delta_y
        self.set_condenser_stigmator(x, y)

    def set_condenser_stigmator_3fold(self, x, y):
        vector_value = self.omp_worker.execute_on_worker(
            lambda: self._condenser_stigmator_3fold.get_input_value(),
            "lambda: self._condenser_stigmator_3fold.get_input_value()")
        vector_value.x = x
        vector_value.y = y
        self.omp_worker.execute_on_worker(
            lambda: self._condenser_stigmator_3fold.set_input_value(vector_value),
            "lambda: self._condenser_stigmator_3fold.set_input_value(vector_value)")

    def get_condenser_stigmator_3fold(self):
        vector_value = self.omp_worker.execute_on_worker(
            lambda: self._condenser_stigmator_3fold.get_input_value(),
            "lambda: self._condenser_stigmator_3fold.get_input_value()")
        return vector_value.x, vector_value.y

    def change_condenser_stigmator_3fold(self, delta_x, delta_y):
        x, y = self.get_condenser_stigmator_3fold()
        x += delta_x
        y += delta_y
        self.set_condenser_stigmator_3fold(x, y)

    def set_coma_stigmator(self, x, y):
        vector_value = self.omp_worker.execute_on_worker(
            lambda: self._coma_stigmator.get_input_value(),
            "lambda: self._coma_stigmator.get_input_value()")
        vector_value.x = x
        vector_value.y = y
        self.omp_worker.execute_on_worker(
            lambda: self._coma_stigmator.set_input_value(vector_value),
            "lambda: self._coma_stigmator.set_input_value(vector_value)")

    def get_coma_stigmator(self):
        vector_value = self.omp_worker.execute_on_worker(
            lambda: self._coma_stigmator.get_input_value(),
            "lambda: self._coma_stigmator.get_input_value()")
        return vector_value.x, vector_value.y

    def change_coma_stigmator(self, delta_x, delta_y):
        x, y = self.get_coma_stigmator()
        x += delta_x
        y += delta_y
        self.set_coma_stigmator(x, y)

    def get_probe_convergence_semi_angle(self):
        return self.omp_worker.execute_on_worker(
            lambda: self.optics.get_probe_convergence_semi_angle(),
            "lambda: self.optics.get_probe_convergence_semi_angle()")

    def set_probe_convergence_semi_angle(self, angle):
        self.omp_worker.execute_on_worker(
            lambda: self.optics.set_probe_convergence_semi_angle(angle),
            "lambda: self.optics.set_probe_convergence_semi_angle(angle)")

    def get_stem_rotation_in_rad(self):
        return self.omp_worker.execute_on_worker(
            lambda: self.column.get_scan_rotation(),
            "lambda: self.column.get_scan_rotation()")

    def set_stem_rotation(self, angle_in_rad):
        self.omp_worker.execute_on_worker(
            lambda: self.column.set_scan_rotation(angle_in_rad),
            "lambda: self.column.set_scan_rotation(angle_in_rad)")

    def in_stem_mode(self):
        operating_mode = self.omp_worker.execute_on_worker(
            lambda: self.column.get_mode().get_column_operating_mode(),
            "lambda: self.column.get_column_operating_mode()")

        return operating_mode == ColumnOperatingMode.stem

    def get_full_scan_field_of_view(self):
        fov = self.omp_worker.execute_on_worker(
            lambda: self.optics.get_full_scan_field_of_view(),
            "lambda: self.optics.get_full_scan_field_of_view()")
        return fov.x, fov.y

    def set_spot_size_index(self, index):
        self.omp_worker.execute_on_worker(
            lambda: self.optics.set_spot_size_index(index),
            "self.optics.set_spot_size_index(index)")

    def get_spot_size_index(self):
        return self.omp_worker.execute_on_worker(
            lambda: self.optics.get_spot_size_index(),
            "self.optics.get_spot_size_index()")

    def get_intensity(self):
        return self.omp_worker.execute_on_worker(
            lambda: self.optics.get_intensity(),
            "self.optics.get_intensity()")

    def set_intensity(self, intensity):
        self.omp_worker.execute_on_worker(
            lambda: self.optics.set_intensity(intensity),
            "self.optics.set_intensity()")

    def set_align_beam_shift(self, x, y):
        vector_value = self.omp_worker.execute_on_worker(
            lambda: self.optics.get_deflectors()
            .get_beam_dc_deflector().get_alignments().get_shift(),
            "self.optics.get_deflectors()"
            ".get_beam_dc_deflector().get_alignments().get_shift()")
        vector_value.x = x
        vector_value.y = y
        self.omp_worker.execute_on_worker(
            lambda: self.optics.get_deflectors()
            .get_beam_dc_deflector().get_alignments().set_shift(vector_value),
            "self.optics.get_deflectors()"
            ".get_beam_dc_deflector().get_alignments().set_shift(vector_value)")

    def get_align_beam_shift(self):
        vector_value = self.omp_worker.execute_on_worker(
            lambda: self.optics.get_deflectors()
            .get_beam_dc_deflector().get_alignments().get_shift(),
            "self.optics.get_deflectors()"
            ".get_beam_dc_deflector().get_alignments().get_shift()")
        return vector_value.x, vector_value.y

    def set_user_beam_shift(self, x, y):
        vector_value = self.omp_worker.execute_on_worker(
            lambda: self.optics.get_deflectors().get_beam_dc_deflector().get_raw_shift(),
            "self.optics.get_deflectors().get_beam_dc_deflector().get_raw_shift()")
        vector_value.x = x
        vector_value.y = y
        self.omp_worker.execute_on_worker(
            lambda: self.optics.get_deflectors()
            .get_beam_dc_deflector().set_raw_shift(vector_value),
            "self.optics.get_deflectors()"
            ".get_beam_dc_deflector().set_raw_shift(vector_value)")

    def get_user_beam_shift(self):
        vector_value = self.omp_worker.execute_on_worker(
            lambda: self.optics.get_deflectors().get_beam_dc_deflector().get_raw_shift(),
            "self.optics.get_deflectors().get_beam_dc_deflector().get_raw_shift()")
        return vector_value.x, vector_value.y

    def set_calibrated_beam_shift(self, x, y):
        vector_value = self.omp_worker.execute_on_worker(
            lambda: self.optics.get_deflectors().get_beam_dc_deflector().get_shift(),
            "self.optics.get_deflectors().get_beam_dc_deflector().get_shift()")
        vector_value.x = x
        vector_value.y = y
        vector_value = self.omp_worker.execute_on_worker(
            lambda: self.optics.get_deflectors().get_beam_dc_deflector().set_shift(vector_value),
            "self.optics.get_deflectors().get_beam_dc_deflector().set_shift(vector_value)")

    def get_calibrated_beam_shift(self):
        vector_value = self.omp_worker.execute_on_worker(
            lambda: self.optics.get_deflectors().get_beam_dc_deflector().get_shift(),
            "self.optics.get_deflectors().get_beam_dc_deflector().get_shift()")
        return vector_value.x, vector_value.y

    def set_user_gun_shift(self, x, y):
        vector_value = self.omp_worker.execute_on_worker(
            lambda: self.optics.get_deflectors().get_gun_dc_deflector().get_raw_shift(),
            "self.optics.get_deflectors().get_gun_dc_deflector().get_raw_shift()")
        vector_value.x = x
        vector_value.y = y
        self.omp_worker.execute_on_worker(
            lambda: self.optics.get_deflectors().get_gun_dc_deflector().set_raw_shift(vector_value),
            "self.optics.get_deflectors().get_gun_dc_deflector().set_raw_shift(vector_value)")

    def get_user_gun_shift(self):
        vector_value = self.omp_worker.execute_on_worker(
            lambda: self.optics.get_deflectors().get_gun_dc_deflector().get_raw_shift(),
            "self.optics.get_deflectors().get_gun_dc_deflector().get_raw_shift()")
        return vector_value.x, vector_value.y

    def set_align_gun_shift(self, x, y):
        vector_value = self.omp_worker.execute_on_worker(
            lambda: self.optics.get_deflectors()
            .get_gun_dc_deflector().get_alignments().get_shift(),
            "self.optics.get_deflectors()"
            ".get_gun_dc_deflector().get_alignments().get_shift()")
        vector_value.x = x
        vector_value.y = y

        self.omp_worker.execute_on_worker(
            lambda: self.optics.get_deflectors()
            .get_gun_dc_deflector().get_alignments().set_shift(vector_value),
            "self.optics.get_deflectors()"
            ".get_gun_dc_deflector().get_alignments().set_shift(vector_value)")

    def get_align_gun_shift(self):
        vector_value = self.omp_worker.execute_on_worker(
            lambda: self.optics.get_deflectors()
            .get_gun_dc_deflector().get_alignments().get_shift(),
            "self.optics.get_deflectors()"
            ".get_gun_dc_deflector().get_alignments().get_shift()")
        return vector_value.x, vector_value.y

    def set_align_gun_tilt(self, x, y):
        raise Exception("OMP set_align_gun_tilt is not supported")

    def get_align_gun_tilt(self):
        raise Exception("OMP get_align_gun_tilt is not supported")

    def set_user_gun_tilt(self, x, y):
        raise Exception("OMP set_user_gun_tilt is not supported")

    def get_user_gun_tilt(self):
        raise Exception("OMP get_user_gun_tilt is not supported")

    def get_lens_value(self, lens_name):
        if self.tem_access_control:
            return self.tem_access_control.GetLensValue(lens_name)
        raise Exception("OMP get_lens_value is not supported")

    def set_lens_value(self, lens_name, value):
        if self.tem_access_control:
            self.tem_access_control.SetLensValue(lens_name, value)
        else:
            raise Exception("OMP set_lens_value is not supported")

    def get_ofe_x(self, ofe_name):
        if self.tem_access_control:
            return self.tem_access_control.GetOfeValueX(ofe_name)
        raise Exception("OMP get_ofe_x is not supported")

    def get_ofe_y(self, ofe_name):
        if self.tem_access_control:
            return self.tem_access_control.GetOfeValueY(ofe_name)
        raise Exception("OMP get_ofe_y is not supported")

    def set_ofe_x(self, ofe_name, value):
        if self.tem_access_control:
            self.tem_access_control.SetOfeValueX(ofe_name, value)
        else:
            raise Exception("OMP set_ofe_x is not supported")

    def set_ofe_y(self, ofe_name, value):
        if self.tem_access_control:
            self.tem_access_control.SetOfeValueY(ofe_name, value)
        else:
            raise Exception("OMP set_ofe_y is not supported")

    def _get_current_projector_mags(self, column_mode):
        raise Exception("OMP _get_current_projector_mags is not supported")

    def find_magnification_index(self, display_value, mag_dict):
        raise Exception("OMP find_magnification_index is not supported")

    def get_mag_value(self, index):
        raise Exception("OMP get_mag_value is not supported")

    def get_current_mag_value(self):
        raise Exception("OMP get_current_mag_value is not supported")
        # return self.omp_worker.execute_on_worker(
        #       lambda: self.optics.get_current_magnification(),
        #       "self.optics.get_current_magnification()")

    def set_magnification(self, magnification):
        raise Exception("OMP set_magnification is not supported")
        # self.omp_worker.execute_on_worker(lambda: self.optics.set_magnification(magnification),
        #                                  description="self.optics.set_magnification()")

    def is_hm_sub_mode_sa(self):
        hm_sub_mode = self.omp_worker.execute_on_worker(
            lambda: self.optics.get_current_magnification().get_magnification_sub_mode,
            "lambda: self.optics.get_current_magnification().get_magnification_sub_mode")

        return hm_sub_mode == MagnificationSubMode.sa

    def _get_magnification_sub_mode(self, magnification):
        return self.omp_worker.execute_on_worker(
            lambda: self.optics.get_current_magnification().get_magnification_sub_mode,
            "lambda: self.optics.get_current_magnification().get_magnification_sub_mode")

    def set_magnification_index(self, index):
        raise Exception("OMP set_magnification_index is not supported")

    def get_magnification_info(self, magnification):
        raise Exception("OMP get_magnification_info is not supported")

    def get_nominal_value(self, magnification):
        raise Exception("OMP get_nominal_value is not supported")

    def get_display_value(self, magnification):
        raise Exception("OMP get_display_value is not supported")

    def get_available_mags(self):
        raise Exception("OMP get_available_mags is not supported")
        # return self.omp_worker.execute_on_worker(lambda: self.optics.get_magnifications(?),
        #                                          description="self.optics.get_magnifications(?)")

    def is_diffraction(self):
        raise Exception("OMP is_diffraction is not supported")

    def set_diffraction(self, diffraction_active):
        raise Exception("OMP set_diffraction is not supported")

    def is_eftem_mode(self):
        raise Exception("OMP is_eftem_mode is not supported")

    def set_eftem_mode(self, eftem_mode_active):
        raise Exception("OMP set_eftem_mode is not supported")

    def is_nano_probe(self):
        raise Exception("OMP is_nano_probe is not supported")

    def set_nano_probe(self, nano_probe_active):
        raise Exception("OMP set_nano_probe is not supported")

    def is_nano_probe_available(self):
        raise Exception("OMP is_nano_probe_available is not supported")

    def is_nano_probe_allowed(self):
        raise Exception("OMP is_nano_probe_allowed is not supported")

    def is_lorentz(self):
        raise Exception("OMP is_lorentz is not supported")

    def set_lorentz(self, lorentz_active):
        raise Exception("OMP set_lorentz is not supported")

    def is_lorentz_available(self):
        raise Exception("OMP is_lorentz_available is not supported")

    def is_lorentz_allowed(self):
        raise Exception("OMP is_lorentz_allowed is not supported")

    def get_illuminated_area_diameter(self):
        return self.omp_worker.execute_on_worker(
            lambda: self.optics.get_illuminated_area_diameter(),
            "self.optics.get_illuminated_area_diameter()")

    def set_illuminated_area_diameter(self, target):
        self.omp_worker.execute_on_worker(
            lambda: self.optics.set_illuminated_area_diameter(target),
            "self.optics.set_illuminated_area_diameter(target)")

    def is_illumination_free_c3_off(self):
        raise Exception("OMP is_illumination_free_c3_off is not supported")

    def is_illumination_free_c2_off(self):
        raise Exception("OMP is_illumination_free_c2_off is not supported")

    def is_illumination_parallel(self):
        raise Exception("OMP is_illumination_parallel is not supported")

    def is_illumination_probe(self):
        raise Exception("OMP is_illumination_parallel is not supported")

    def is_illumination_probe_normal_angle(self):
        raise Exception("OMP is_illumination_probe_normal_angle is not supported")

    def is_illumination_probe_large_angle(self):
        raise Exception("OMP is_illumination_probe_large_angle is not supported")

    def set_illumination_free_c3_off(self):
        raise Exception("OMP set_illumination_free_c3_off is not supported")

    def set_illumination_free_c2_off(self):
        raise Exception("OMP set_illumination_free_c2_off is not supported")

    def set_illumination_parallel(self):
        raise Exception("OMP set_illumination_parallel is not supported")

    def set_illumination_probe_normal_angle(self):
        raise Exception("OMP set_illumination_probe_normal_angle is not supported")

    def set_illumination_probe_large_angle(self):
        raise Exception("OMP set_illumination_probe_large_angle is not supported")

    def set_basic_monochromator_tuning_mode(self):
        raise Exception("OMP set_basic_monochromator_tuning_mode is not supported")

    def switch_to_stem(self):
        raise Exception("OMP switch_to_stem is not supported")

    def switch_to_tem(self):
        raise Exception("OMP switch_to_tem is not supported")

    def get_current_optics_mode_state(self):
        raise Exception("OMP get_current_optics_mode_state is not supported")

    def restore_optics_mode_state(self, optics_mode_state):
        raise Exception("OMP restore_optics_mode_state is not supported")
