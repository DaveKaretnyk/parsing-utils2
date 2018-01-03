# Copyright (c) 2012-2016 by FEI Company
# All rights reserved. This file includes confidential and proprietary
# information of FEI Company.
import logging


from fei.tem.omp.api import ApertureMechanismState, ApertureMechanismType
from fei.tem.omp.api import ApertureType
from fei.infra.tem_server_access.models.apertures_service import (
    C1_APERTURE_NAME, C2_APERTURE_NAME, C3_APERTURE_NAME, OBJ_APERTURE_NAME, SA_APERTURE_NAME)


logger = logging.getLogger(__name__)


class AperturesControl(object):
    def __init__(self, omp_worker, column):
        super(AperturesControl, self).__init__()
        self._omp_worker = omp_worker
        self.column = column

        # Dictionary: key is mechanism name. Value will be dictionary with aperture name as key and
        # aperture interface from server as value - these must initialized dynamically of course.
        self.dict_mechanism_to_aperture = {
            C1_APERTURE_NAME: {},
            C2_APERTURE_NAME: {},
            C3_APERTURE_NAME: {},
            OBJ_APERTURE_NAME: {},
            SA_APERTURE_NAME: {}
        }

        # Dictionary of mechanisms with name as key and mechanism interface from server as value.
        self.dict_mechanism_to_interface = {}
        self._initialize_apertures()

    def __del__(self):
        logger.info("OMP AperturesControl destructor")

    def disconnect(self):
        logger.info("OMP AperturesControl disconnect")
        self.omp_worker.execute_on_worker(
            lambda: self._release_objects(),
            "lambda: self._release_objects()")

    def _release_objects(self):
        self.dict_mechanism_to_aperture[C1_APERTURE_NAME] = {}
        self.dict_mechanism_to_aperture[C2_APERTURE_NAME] = {}
        self.dict_mechanism_to_aperture[C3_APERTURE_NAME] = {}
        self.dict_mechanism_to_aperture[OBJ_APERTURE_NAME] = {}
        self.dict_mechanism_to_aperture[SA_APERTURE_NAME] = {}

        self._release_objects()
        self._omp_worker = None

    def get_available_mechanisms(self):
        return self.dict_mechanism_to_interface.keys()

    def enable(self, mechanism_name, enable):
        self._check_mechanism_name(mechanism_name)

        if enable:
            self._omp_worker.execute_on_worker(
                lambda: self.dict_mechanism_to_interface[mechanism_name].enable(),
                "lambda: self.dict_mechanism_to_interface[mechanism_name].enable()")
        else:
            self._omp_worker.execute_on_worker(
                lambda: self.dict_mechanism_to_interface[mechanism_name].disable(),
                "lambda: self.dict_mechanism_to_interface[mechanism_name].disable()")

    def insert(self, mechanism_name, insert):
        self._check_mechanism_name(mechanism_name)

        if insert:
            self._omp_worker.execute_on_worker(
                lambda: self.dict_mechanism_to_interface[mechanism_name].insert(),
                "lambda: self.dict_mechanism_to_interface[mechanism_name].insert()")
        else:
            self._omp_worker.execute_on_worker(
                lambda: self.dict_mechanism_to_interface[mechanism_name].retract(),
                "lambda: self.dict_mechanism_to_interface[mechanism_name].retract()")

    def select(self, mechanism_name, aperture_name):
        self._check_mechanism_name(mechanism_name)
        self._check_aperture_name(mechanism_name, aperture_name)

        mechanism = self.dict_mechanism_to_interface[mechanism_name]

        aperture_collection = self._omp_worker.execute_on_worker(
            lambda: mechanism.get_apertures(),
            "lambda: mechanism.get_apertures()")
        for aperture in aperture_collection:
            aperture_name_in_collection = self._omp_worker.execute_on_worker(
                lambda: aperture.get_name(),
                "lambda: aperture.get_name()")
            if aperture_name_in_collection == aperture_name:
                self._omp_worker.execute_on_worker(
                    lambda: mechanism.select_aperture(aperture),
                    "lambda: mechanism.select_aperture(aperture)")
                return

        raise Exception("Aperture not found!")

    def mechanism_get_info(self, mechanism_name):
        self._check_mechanism_name(mechanism_name)

        return self._get_mechanism_info(self.dict_mechanism_to_interface[mechanism_name])

    def mechanism_is_motorized(self, mechanism_name):
        self._check_mechanism_name(mechanism_name)
        mechanism = self.dict_mechanism_to_interface[mechanism_name]

        return self._omp_worker.execute_on_worker(
            lambda: mechanism.get_type(),
            "lambda: mechanism.get_type()") == ApertureMechanismType.motorized

    def get_selected(self, mechanism_name):
        self._check_mechanism_name(mechanism_name)

        return self._get_aperture_selected(self.dict_mechanism_to_interface[mechanism_name])

    def get_available(self, mechanism_name):
        self._check_mechanism_name(mechanism_name)

        return self.dict_mechanism_to_aperture[mechanism_name].keys()

    def get_info(self, mechanism_name, aperture_name):
        self._check_mechanism_name(mechanism_name)
        self._check_aperture_name(mechanism_name, aperture_name)

        mechanism = self.dict_mechanism_to_interface[mechanism_name]

        aperture_collection = self._omp_worker.execute_on_worker(
            lambda: mechanism.get_apertures(),
            "lambda: mechanism.get_apertures()")
        for aperture in aperture_collection:
            aperture_name_in_collection = self._omp_worker.execute_on_worker(
                lambda: aperture.get_name(),
                "lambda: mechanism.get_name()")
            if aperture_name_in_collection == aperture_name:
                return self._get_info(aperture)

        raise Exception("Aperture not found!")

    # private methods ----------------------------------------------------------------------------

    def _initialize_apertures(self):
        ams = self._omp_worker.execute_on_worker(
            lambda: self.column.get_aperture_mechanism_collection(),
            "lambda: self.column/get_aperture_mechanism_collection()")
        for am in ams:
            name = self._omp_worker.execute_on_worker(lambda: am.get_name(),
                                                      "lambda: am.get_name()")

            apertures = self._omp_worker.execute_on_worker(lambda: am.get_apertures(),
                                                           "lambda: am.get_apertures()")
            if name == C1_APERTURE_NAME:
                self.dict_mechanism_to_interface[C1_APERTURE_NAME] = am
                for aperture in apertures:
                    aperture_name = self._omp_worker.execute_on_worker(
                        lambda: aperture.get_name(),
                        "lambda: aperture.get_name()")
                    self.dict_mechanism_to_aperture[C1_APERTURE_NAME][aperture_name] = aperture
            elif name == C2_APERTURE_NAME:
                self.dict_mechanism_to_interface[C2_APERTURE_NAME] = am
                for aperture in apertures:
                    aperture_name = self._omp_worker.execute_on_worker(
                        lambda: aperture.get_name(),
                        "lambda: aperture.get_name()")
                    self.dict_mechanism_to_aperture[C2_APERTURE_NAME][aperture_name] = aperture
            elif name == C3_APERTURE_NAME:
                self.dict_mechanism_to_interface[C3_APERTURE_NAME] = am
                for aperture in apertures:
                    aperture_name = self._omp_worker.execute_on_worker(
                        lambda: aperture.get_name(),
                        "lambda: aperture.get_name()")
                    self.dict_mechanism_to_aperture[C3_APERTURE_NAME][aperture_name] = aperture
            elif name == OBJ_APERTURE_NAME:
                self.dict_mechanism_to_interface[OBJ_APERTURE_NAME] = am
                for aperture in apertures:
                    aperture_name = self._omp_worker.execute_on_worker(
                        lambda: aperture.get_name(),
                        "lambda: aperture.get_name()")
                    self.dict_mechanism_to_aperture[OBJ_APERTURE_NAME][aperture_name] = aperture
            elif name == SA_APERTURE_NAME:
                self.dict_mechanism_to_interface[SA_APERTURE_NAME] = am
                for aperture in apertures:
                    aperture_name = self._omp_worker.execute_on_worker(
                        lambda: aperture.get_name(),
                        "lambda: aperture.get_name()")
                    self.dict_mechanism_to_aperture[SA_APERTURE_NAME][aperture_name] = aperture

    @staticmethod
    def _get_diameter(self, aperture):
        aperture_type = self._omp_worker.execute_on_worker(lambda: aperture.get_type(),
                                                          "lambda: aperture.get_type()")

        if aperture_type != ApertureType.circular:
            aperture_name = self._omp_worker.execute_on_worker(lambda: aperture.get_name(),
                                                               "lambda: aperture.get_name()")
            logger.warning('query for diameter on {0}, returning None'.format(aperture_name))
            return None
        return self._omp_worker.execute_on_worker(lambda: aperture.get_diameter(),
                                                  "lambda: aperture.get_diameter()")

    def _get_info(self, aperture):
        aperture_name = self._omp_worker.execute_on_worker(lambda: aperture.get_name(),
                                                           "lambda: aperture.get_name()")
        aperture_type = self._omp_worker.execute_on_worker(lambda: aperture.get_type(),
                                                           "lambda: aperture.get_type()")
        aperture_offset_x = self._omp_worker.execute_on_worker(lambda: aperture.get_offset().x,
                                                               "lambda: aperture.get_offset().x")
        aperture_offset_y = self._omp_worker.execute_on_worker(lambda: aperture.get_offset().y,
                                                               "lambda: aperture.get_offset().y")
        aperture_reference_position_x = self._omp_worker.execute_on_worker(
            lambda: aperture.get_reference_position().x,
            "lambda: aperture.get_reference_position().x")
        aperture_reference_position_y = self._omp_worker.execute_on_worker(
            lambda: aperture.get_reference_position().y,
            "lambda: aperture.get_reference_position().y")


        return (aperture_name, aperture_type,
                (aperture_offset_x, aperture_offset_y),
                (aperture_reference_position_x, aperture_reference_position_y),
                self._get_diameter(self, aperture))

    def _get_mechanism_info(self, aperture_mechanism):
        aperture_mechanism_id = self._omp_worker.execute_on_worker(
            lambda: aperture_mechanism.get_id(),
            "lambda: aperture_mechanism.get_id()")
        aperture_mechanism_name = self._omp_worker.execute_on_worker(
            lambda: aperture_mechanism.get_name(),
            "lambda: aperture_mechanism.get_name()")
        aperture_mechanism_state = self._omp_worker.execute_on_worker(
            lambda: aperture_mechanism.get_state(),
            "lambda: aperture_mechanism.get_state()")
        aperture_mechanism_is_retractable = self._omp_worker.execute_on_worker(
            lambda: aperture_mechanism.is_retractable(),
            "lambda: aperture_mechanism.is_retractable()")
        aperture_mechanism_is_blocked = self._omp_worker.execute_on_worker(
            lambda: aperture_mechanism.is_blocked(),
            "lambda: aperture_mechanism.is_blocked()")

        return (aperture_mechanism_id, aperture_mechanism_name, aperture_mechanism_state,
                aperture_mechanism_is_retractable, aperture_mechanism_is_blocked)

    def _get_aperture_selected(self, aperture_mechanism):
        # 'Inserted' state is also what is needed for mechanisms that are 'always inserted'.
        aperture_mechanism_state = self._omp_worker.execute_on_worker(
            lambda: aperture_mechanism.get_state(),
            "lambda: aperture_mechanism.get_state()")

        if aperture_mechanism_state != ApertureMechanismState.inserted:
            return None
        return self._omp_worker.execute_on_worker(
            lambda: aperture_mechanism.get_selected_aperture().get_name(),
            "aperture_mechanism.get_selected_aperture().get_name()")

    def _check_mechanism_name(self, mechanism_name):
        if mechanism_name not in self.dict_mechanism_to_interface:
            message = 'could not find "{0}" mechanism'.format(mechanism_name)
            logger.error(message)
            raise LookupError(message)

    def _check_aperture_name(self, mechanism_name, aperture_name):
        if aperture_name not in self.dict_mechanism_to_aperture[mechanism_name]:
            message = 'could not find aperture "{0}" in mechanism "{1}"'.format(aperture_name,
                                                                                mechanism_name)
            logger.error(message)
            raise LookupError(message)
