# Copyright (c) 2016 by FEI Company
# All rights reserved. This file includes confidential and proprietary
# information of FEI Company.
import unittest

import numpy as np

from fei.infra.tem_server_access.api import TemService
from fei.infra.tem_server_access.models.tests.helpers import change_value_and_restore_test


SYSTEM_TESTING = True


# Low level integration tests - requires running server! That is, not a unit tests.
# Note that we tests the functionality via the parent class 'TemService', since this is the public
# interface that clients will use.
# These tests require the server to be in STEM mode
class TestOpticsServiceNotUsingOmpInStem(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create connection to underlying server once, i.e. not for each and every tests.
        cls.tem_service = TemService(use_omp=False, use_tem_access=True)
        cls.lorentz_supported = cls.tem_service.optics.is_lorentz_available()
        cls.nano_probe_supported = cls.tem_service.optics.is_nano_probe_available()

    def setUp(self):
        self.diagnostics_print = True

    def tearDown(self):
        pass

    def _change_vector_and_restore_test_using_set_function(self, set_function, get_function,
                                                           delta_value_x, delta_value_y,
                                                           nr_places_x, nr_places_y):
        current_value = get_function()
        if self.diagnostics_print:
            print "Original value: ", current_value
        set_function(current_value[0] + delta_value_x, current_value[1] + delta_value_y)
        new_value = get_function()
        if self.diagnostics_print:
            print "After applying delta_x of {} and delta_y of {} using set function, " \
                  "new value is: {}".format(delta_value_x, delta_value_y, new_value)
        self.assertAlmostEqual(current_value[0]+delta_value_x, new_value[0], nr_places_x,
                               "Resulting change for x is not as expected")
        self.assertAlmostEqual(current_value[1]+delta_value_y, new_value[1], nr_places_y,
                               "Resulting change for y is not as expected")
        if self.diagnostics_print:
            print "Putting back original value: ", current_value
        set_function(current_value[0], current_value[1])
        new_value = get_function()
        if self.diagnostics_print:
            print "Resulting value after restore: ", new_value
        self.assertAlmostEqual(current_value[0], new_value[0], nr_places_x,
                               "Failed to restore to original x value")
        self.assertAlmostEqual(current_value[1], new_value[1], nr_places_y,
                               "Failed to restore to original y value")

    def _change_value_and_restore_test_by_element_name(self, set_function, get_function, name,
                                                       delta_value, nr_places):
        current_value = get_function(name)
        if self.diagnostics_print:
            print "Original value for element {}: {}".format(name, current_value)
        set_function(name, current_value + delta_value)
        new_value = get_function(name)
        if self.diagnostics_print:
            print "After applying delta of {}, new value for element {} is: {}".format(delta_value,
                                                                                       name,
                                                                                       new_value)
        self.assertAlmostEqual(current_value+delta_value, new_value, nr_places,
                               "Resulting change is not as expected")
        if self.diagnostics_print:
            print "Putting back original value: ", current_value
        set_function(name, current_value)
        new_value = get_function(name)
        if self.diagnostics_print:
            print "Resulting value for element {} after restore: {}".format(name, new_value)
        self.assertAlmostEqual(current_value, new_value, nr_places,
                               "Failed to restore to original value")

    def _change_vector_and_restore_test_using_change_function(self,
                                                              change_function,
                                                              get_function,
                                                              set_function,
                                                              delta_value_x,
                                                              delta_value_y,
                                                              nr_places_x,
                                                              nr_places_y):
        current_value = get_function()
        if self.diagnostics_print:
            print "Original value: ", current_value
        change_function(delta_value_x, delta_value_y)
        new_value = get_function()
        if self.diagnostics_print:
            print "After applying delta_x of {} and delta_y of {} using change function, " \
                  "new value is: {}".format(delta_value_x, delta_value_y, new_value)
        self.assertAlmostEqual(current_value[0]+delta_value_x, new_value[0], nr_places_x,
                               "Resulting change for x is not as expected")
        self.assertAlmostEqual(current_value[1]+delta_value_y, new_value[1], nr_places_y,
                               "Resulting change for y is not as expected")
        if self.diagnostics_print:
            print "Putting back original value: ", current_value
        set_function(current_value[0], current_value[1])
        new_value = get_function()
        if self.diagnostics_print:
            print "Resulting value after restore: ", new_value
        self.assertAlmostEqual(current_value[0], new_value[0], nr_places_x,
                               "Failed to restore to original x value")
        self.assertAlmostEqual(current_value[1], new_value[1], nr_places_y,
                               "Failed to restore to original y value")

    def test_defocus(self):
        optics = self.tem_service.optics
        delta_value = 8e-6
        nr_places = 7
        change_value_and_restore_test(self, optics.set_defocus_m, optics.get_defocus_m,
                                      delta_value, nr_places)

    def test_condenser_stigmator(self):
        optics = self.tem_service.optics
        delta_value = 8e-3
        nr_places = 4
        self._change_vector_and_restore_test_using_set_function(
            optics.stigmator_set_condenser,
            optics.stigmator_get_condenser,
            delta_value_x=delta_value,
            delta_value_y=delta_value,
            nr_places_x=nr_places,
            nr_places_y=nr_places)
        self._change_vector_and_restore_test_using_change_function(
            optics.stigmator_change_condenser,
            optics.stigmator_get_condenser,
            optics.stigmator_set_condenser,
            delta_value_x=delta_value,
            delta_value_y=delta_value,
            nr_places_x=nr_places,
            nr_places_y=nr_places)

    def test_condenser_3fold_stigmator(self):
        optics = self.tem_service.optics
        delta_value = 8e-3
        nr_places = 4
        self._change_vector_and_restore_test_using_set_function(
            optics.stigmator_set_condenser_3fold,
            optics.stigmator_get_condenser_3fold,
            delta_value_x=delta_value,
            delta_value_y=delta_value,
            nr_places_x=nr_places,
            nr_places_y=nr_places)
        self._change_vector_and_restore_test_using_change_function(
            optics.stigmator_change_condenser_3fold,
            optics.stigmator_get_condenser_3fold,
            optics.stigmator_set_condenser_3fold,
            delta_value_x=delta_value,
            delta_value_y=delta_value,
            nr_places_x=nr_places,
            nr_places_y=nr_places)

    def test_coma_stigmator(self):
        optics = self.tem_service.optics
        delta_value = 8e-3
        nr_places = 4
        self._change_vector_and_restore_test_using_set_function(optics.stigmator_set_coma,
                                                                optics.stigmator_get_coma,
                                                                delta_value_x=delta_value,
                                                                delta_value_y=delta_value,
                                                                nr_places_x=nr_places,
                                                                nr_places_y=nr_places)
        self._change_vector_and_restore_test_using_change_function(optics.stigmator_change_coma,
                                                                   optics.stigmator_get_coma,
                                                                   optics.stigmator_set_coma,
                                                                   delta_value_x=delta_value,
                                                                   delta_value_y=delta_value,
                                                                   nr_places_x=nr_places,
                                                                   nr_places_y=nr_places)

    def test_probe_convergence_semi_angle(self):
        optics = self.tem_service.optics
        delta_value = -2e-3
        nr_places = 4
        change_value_and_restore_test(self, optics.set_probe_convergence_semi_angle,
                                            optics.get_probe_convergence_semi_angle,
                                            delta_value, nr_places)

    def test_full_scan_field_of_view(self):
        optics = self.tem_service.optics
        current_value = optics.get_full_scan_field_of_view()
        if self.diagnostics_print:
            print "Ful scan field of view: ", current_value

    def test_spot_size_index(self):
        optics = self.tem_service.optics
        delta_value = 1
        nr_places = 0
        change_value_and_restore_test(self, optics.set_spot_size_index,
                                      optics.get_spot_size_index, delta_value, nr_places)

    def test_lens_value(self):
        optics = self.tem_service.optics
        delta_value = 8e-3
        nr_places = 4
        name = "C1"
        self._change_value_and_restore_test_by_element_name(optics.set_lens_value,
                                                            optics.get_lens_value, name,
                                                            delta_value, nr_places)
        name = "C2"
        self._change_value_and_restore_test_by_element_name(optics.set_lens_value,
                                                            optics.get_lens_value, name,
                                                            delta_value, nr_places)
        name = "C3"
        self._change_value_and_restore_test_by_element_name(optics.set_lens_value,
                                                            optics.get_lens_value, name,
                                                            delta_value, nr_places)
        name = "MC"
        self._change_value_and_restore_test_by_element_name(optics.set_lens_value,
                                                            optics.get_lens_value, name,
                                                            delta_value, nr_places)
        name = "ObjLens"
        self._change_value_and_restore_test_by_element_name(optics.set_lens_value,
                                                            optics.get_lens_value, name,
                                                            delta_value, nr_places)
        name = "DiffrLens"
        self._change_value_and_restore_test_by_element_name(optics.set_lens_value,
                                                            optics.get_lens_value, name,
                                                            delta_value, nr_places)
        name = "IL"
        self._change_value_and_restore_test_by_element_name(optics.set_lens_value,
                                                            optics.get_lens_value, name,
                                                            delta_value, nr_places)
        name = "P1"
        self._change_value_and_restore_test_by_element_name(optics.set_lens_value,
                                                            optics.get_lens_value, name,
                                                            delta_value, nr_places)
        name = "P2"
        self._change_value_and_restore_test_by_element_name(optics.set_lens_value,
                                                            optics.get_lens_value, name,
                                                            delta_value, nr_places)

    def test_lens_value_via_ofe_x(self):
        optics = self.tem_service.optics
        delta_value = 8e-3
        nr_places = 4
        name = "C1"
        self._change_value_and_restore_test_by_element_name(optics.set_ofe_x,
                                                            optics.get_ofe_x, name,
                                                            delta_value, nr_places)
        name = "C2"
        self._change_value_and_restore_test_by_element_name(optics.set_ofe_x,
                                                            optics.get_ofe_x, name,
                                                            delta_value, nr_places)
        name = "C3"
        self._change_value_and_restore_test_by_element_name(optics.set_ofe_x,
                                                            optics.get_ofe_x, name,
                                                            delta_value, nr_places)
        name = "MC"
        self._change_value_and_restore_test_by_element_name(optics.set_ofe_x,
                                                            optics.get_ofe_x, name,
                                                            delta_value, nr_places)
        name = "ObjLens"
        self._change_value_and_restore_test_by_element_name(optics.set_ofe_x,
                                                            optics.get_ofe_x, name,
                                                            delta_value, nr_places)
        name = "DiffrLens"
        self._change_value_and_restore_test_by_element_name(optics.set_ofe_x,
                                                            optics.get_ofe_x, name,
                                                            delta_value, nr_places)
        name = "IL"
        self._change_value_and_restore_test_by_element_name(optics.set_ofe_x,
                                                            optics.get_ofe_x, name,
                                                            delta_value, nr_places)
        name = "P1"
        self._change_value_and_restore_test_by_element_name(optics.set_ofe_x,
                                                            optics.get_ofe_x, name,
                                                            delta_value, nr_places)
        name = "P2"
        self._change_value_and_restore_test_by_element_name(optics.set_ofe_x,
                                                            optics.get_ofe_x, name,
                                                            delta_value, nr_places)

    def test_intensity_using_ofe(self):
        optics = self.tem_service.optics
        delta_value = 8e-3
        nr_places = 4
        name = "Intensity"
        self._change_value_and_restore_test_by_element_name(optics.set_ofe_x,
                                                            optics.get_ofe_x,
                                                            name,
                                                            delta_value,
                                                            nr_places)

    def test_intensity(self):
        optics = self.tem_service.optics
        delta_value = 8e-3
        nr_places = 4
        change_value_and_restore_test(self, optics.set_intensity, optics.get_intensity,
                                      delta_value, nr_places)

    def test_intensity_iom(self):
        optics = self.tem_service.optics
        name = "Intensity"
        iom_value = optics.get_intensity()
        ofe_value = optics.get_ofe_x(name)
        if self.diagnostics_print:
            print "Intensity value using IOM: ", iom_value
            print "Intensity value using OFE: ", ofe_value
        self.assertAlmostEqual(iom_value, ofe_value, 4)

    def test_user_gs_using_ofe(self):
        optics = self.tem_service.optics
        delta_value = 8e-3
        nr_places = 4
        name = "User_GS"
        self._change_value_and_restore_test_by_element_name(optics.set_ofe_x, optics.get_ofe_x,
                                                            name, delta_value, nr_places)
        self._change_value_and_restore_test_by_element_name(optics.set_ofe_y, optics.get_ofe_y,
                                                            name, delta_value, nr_places)

    def test_user_gs(self):
        optics = self.tem_service.optics
        delta_value = 8e-3
        nr_places = 4
        self._change_vector_and_restore_test_using_set_function(optics.set_user_gun_shift,
                                                                optics.get_user_gun_shift,
                                                                delta_value_x=delta_value,
                                                                delta_value_y=delta_value,
                                                                nr_places_x=nr_places,
                                                                nr_places_y=nr_places)

    def test_user_gs_explicit(self):
        optics = self.tem_service.optics
        name = "User_GS"
        iom_value = optics.get_user_gun_shift()
        ofe_value = optics.get_ofe_x(name), optics.get_ofe_y(name)
        if self.diagnostics_print:
            print "User GunShift value using Explicit Service Function: ", iom_value
            print "User GunShift value using OFE: ", ofe_value
        self.assertAlmostEqual(iom_value[0], ofe_value[0], 4)
        self.assertAlmostEqual(iom_value[1], ofe_value[1], 4)

    def test_user_gt_using_ofe(self):
        optics = self.tem_service.optics
        delta_value = 8e-3
        nr_places = 4
        name = "User_GT"
        self._change_value_and_restore_test_by_element_name(optics.set_ofe_x, optics.get_ofe_x,
                                                            name, delta_value, nr_places)
        self._change_value_and_restore_test_by_element_name(optics.set_ofe_y, optics.get_ofe_y,
                                                            name, delta_value, nr_places)

    def test_user_gt(self):
        optics = self.tem_service.optics
        delta_value = 8e-3
        nr_places = 4
        self._change_vector_and_restore_test_using_set_function(optics.set_user_gun_tilt,
                                                                optics.get_user_gun_tilt,
                                                                delta_value_x=delta_value,
                                                                delta_value_y=delta_value,
                                                                nr_places_x=nr_places,
                                                                nr_places_y=nr_places)

    def test_user_gt_explicit(self):
        optics = self.tem_service.optics
        name = "User_GT"
        iom_value = optics.get_user_gun_tilt()
        ofe_value = optics.get_ofe_x(name), optics.get_ofe_y(name)
        if self.diagnostics_print:
            print "User GunTilt value using Explicit Service Function: ", iom_value
            print "User GunTilt value using OFE: ", ofe_value
        self.assertAlmostEqual(iom_value[0], ofe_value[0], 4)
        self.assertAlmostEqual(iom_value[1], ofe_value[1], 4)

    def test_align_gs_using_ofe(self):
        optics = self.tem_service.optics
        delta_value = 8e-3
        nr_places = 4
        name = "Align_GS"
        self._change_value_and_restore_test_by_element_name(optics.set_ofe_x, optics.get_ofe_x,
                                                            name, delta_value, nr_places)
        self._change_value_and_restore_test_by_element_name(optics.set_ofe_y, optics.get_ofe_y,
                                                            name, delta_value, nr_places)

    def test_align_gs(self):
        optics = self.tem_service.optics
        delta_value = 8e-3
        nr_places = 4
        self._change_vector_and_restore_test_using_set_function(optics.set_align_gun_shift,
                                                                optics.get_align_gun_shift,
                                                                delta_value_x=delta_value,
                                                                delta_value_y=delta_value,
                                                                nr_places_x=nr_places,
                                                                nr_places_y=nr_places)

    def test_align_gs_iom(self):
        optics = self.tem_service.optics
        name = "Align_GS"
        iom_value = optics.get_align_gun_shift()
        ofe_value = optics.get_ofe_x(name), optics.get_ofe_y(name)
        if self.diagnostics_print:
            print "Align GunShift value using IOM: ", iom_value
            print "Align GunShift value using OFE: ", ofe_value
        self.assertAlmostEqual(iom_value[0], ofe_value[0], 4)
        self.assertAlmostEqual(iom_value[1], ofe_value[1], 4)

    def test_align_gt_using_ofe(self):
        is_blanked = self.tem_service.column_is_beam_blanked()
        if is_blanked:
            if self.diagnostics_print:
                print "Beam is blanked, can not change align gun tilt; skip tests"
            return
        optics = self.tem_service.optics
        delta_value = 8e-3
        nr_places = 4
        name = "Align_GT"
        self._change_value_and_restore_test_by_element_name(optics.set_ofe_x, optics.get_ofe_x,
                                                            name, delta_value, nr_places)
        self._change_value_and_restore_test_by_element_name(optics.set_ofe_y, optics.get_ofe_y,
                                                            name, delta_value, nr_places)

    def test_align_gt(self):
        is_blanked = self.tem_service.column_is_beam_blanked()
        if is_blanked:
            if self.diagnostics_print:
                print "Beam is blanked, can not change align gun tilt; skip tests"
            return

        optics = self.tem_service.optics
        delta_value = 8e-3
        nr_places = 4
        self._change_vector_and_restore_test_using_set_function(optics.set_align_gun_tilt,
                                                                optics.get_align_gun_tilt,
                                                                delta_value_x=delta_value,
                                                                delta_value_y=delta_value,
                                                                nr_places_x=nr_places,
                                                                nr_places_y=nr_places)

    def test_align_gt_iom(self):
        is_blanked = self.tem_service.column_is_beam_blanked()
        if is_blanked:
            if self.diagnostics_print:
                print "Beam is blanked, can not change align gun tilt; skip tests"
            return

        optics = self.tem_service.optics
        name = "Align_GT"
        iom_value = optics.get_align_gun_tilt()
        ofe_value = optics.get_ofe_x(name), optics.get_ofe_y(name)
        if self.diagnostics_print:
            print "Align GunTilt value using IOM: ", iom_value
            print "Align GunTilt value using OFE: ", ofe_value
        self.assertAlmostEqual(iom_value[0], ofe_value[0], 4)
        self.assertAlmostEqual(iom_value[1], ofe_value[1], 4)

    def test_user_bs_using_ofe(self):
        optics = self.tem_service.optics
        delta_value = 8e-3
        nr_places = 4
        name = "User_BS"
        self._change_value_and_restore_test_by_element_name(optics.set_ofe_x, optics.get_ofe_x,
                                                            name, delta_value, nr_places)
        self._change_value_and_restore_test_by_element_name(optics.set_ofe_y, optics.get_ofe_y,
                                                            name, delta_value, nr_places)

    def test_user_bs(self):
        optics = self.tem_service.optics
        delta_value = 8e-3
        nr_places = 4
        self._change_vector_and_restore_test_using_set_function(optics.set_user_beam_shift,
                                                                optics.get_user_beam_shift,
                                                                delta_value_x=delta_value,
                                                                delta_value_y=delta_value,
                                                                nr_places_x=nr_places,
                                                                nr_places_y=nr_places)

    def test_user_bs_iom(self):
        optics = self.tem_service.optics
        name = "User_BS"
        iom_value = optics.get_user_beam_shift()
        ofe_value = optics.get_ofe_x(name), optics.get_ofe_y(name)
        if self.diagnostics_print:
            print "User BeamShift value using IOM: ", iom_value
            print "User BeamShift value using OFE: ", ofe_value
        self.assertAlmostEqual(iom_value[0], ofe_value[0], 4)
        self.assertAlmostEqual(iom_value[1], ofe_value[1], 4)

    def test_calibrated_bs(self):
        optics = self.tem_service.optics
        delta_value = 8e-6
        nr_places = 7
        self._change_vector_and_restore_test_using_set_function(optics.set_calibrated_beam_shift,
                                                                optics.get_calibrated_beam_shift,
                                                                delta_value_x=delta_value,
                                                                delta_value_y=delta_value,
                                                                nr_places_x=nr_places,
                                                                nr_places_y=nr_places)

    def test_align_bs_using_ofe(self):
        optics = self.tem_service.optics
        delta_value = 8e-3
        nr_places = 4
        name = "Align_BS"
        self._change_value_and_restore_test_by_element_name(optics.set_ofe_x, optics.get_ofe_x,
                                                            name, delta_value, nr_places)
        self._change_value_and_restore_test_by_element_name(optics.set_ofe_y, optics.get_ofe_y,
                                                            name, delta_value, nr_places)

    def test_align_bs(self):
        optics = self.tem_service.optics
        delta_value = 8e-3
        nr_places = 4
        self._change_vector_and_restore_test_using_set_function(optics.set_align_beam_shift,
                                                                optics.get_align_beam_shift,
                                                                delta_value_x=delta_value,
                                                                delta_value_y=delta_value,
                                                                nr_places_x=nr_places,
                                                                nr_places_y=nr_places)

    def test_align_bs_iom(self):
        optics = self.tem_service.optics
        name = "Align_BS"
        iom_value = optics.get_align_beam_shift()
        ofe_value = optics.get_ofe_x(name), optics.get_ofe_y(name)
        if self.diagnostics_print:
            print "Align BeamShift value using IOM: ", iom_value
            print "Align BeamShift value using OFE: ", ofe_value
        self.assertAlmostEqual(iom_value[0], ofe_value[0], 4)
        self.assertAlmostEqual(iom_value[1], ofe_value[1], 4)

    def test_stem_rotation(self):
        optics = self.tem_service.optics
        delta_value = 0.4
        nr_places = 2
        change_value_and_restore_test(self, optics.set_stem_rotation,
                                            optics.get_stem_rotation_in_rad,
                                            delta_value, nr_places)

    def test_in_stem_mode(self):
        optics = self.tem_service.optics
        in_stem = optics.in_stem_mode()
        if self.diagnostics_print:
            print "InStem: ", in_stem

    def test_switch_to_stem(self):
        current_state = self.tem_service.optics.get_current_optics_mode_state()
        self.tem_service.optics.switch_to_stem()
        self.assertTrue(self.tem_service.optics.in_stem_mode())
        self.tem_service.optics.restore_optics_mode_state(current_state)

    def test_switch_to_tem(self):
        current_state = self.tem_service.optics.get_current_optics_mode_state()
        self.tem_service.optics.switch_to_tem()
        self.assertFalse(self.tem_service.optics.in_stem_mode())
        self.tem_service.optics.restore_optics_mode_state(current_state)

# Low level integration tests - requires running server! That is, not a unit tests.
# Note that we tests the functionality via the parent class 'TemService', since this is the public
# interface that clients will use.
# These tests require the server to be in TEM mode
class TestOpticsServiceNotUsingOmpInTem(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create connection to underlying server once, i.e. not for each and every tests.
        cls.tem_service = TemService(use_omp=False, use_tem_access=True)
        cls.lorentz_supported = cls.tem_service.optics.is_lorentz_available()
        cls.nano_probe_supported = cls.tem_service.optics.is_nano_probe_available()

    def setUp(self):
        self.diagnostics_print = True

    def tearDown(self):
        pass

    def test_magnification_index(self):
        optics = self.tem_service.optics
        delta_value = 1
        nr_places = 0
        _current_index, _, max_index = optics.get_current_magnification()
        while _current_index + delta_value <= max_index:
            change_value_and_restore_test(self, optics.set_magnification_index,
                                          optics.get_magnification_index,
                                          delta_value, nr_places)
            delta_value += 1
        delta_value = -1
        while _current_index + delta_value >= 0:
            change_value_and_restore_test(self, optics.set_magnification_index,
                                          optics.get_magnification_index,
                                          delta_value, nr_places)
            delta_value -= 1

    def test_is_hm_sub_mode_sa(self):
        optics = self.tem_service.optics
        is_hm_sub_mode_sa = optics.is_hm_sub_mode_sa()
        if self.diagnostics_print:
            print "Is Magnification sub mode SA= ", is_hm_sub_mode_sa

    def test_current_magnification_info(self):
        optics = self.tem_service.optics
        _index, _in_imaging, _max_index, display, nominal, is_calibrated, \
        calibrated_value, rotation, sub_mode = optics.get_current_magnification_info()
        if self.diagnostics_print:
            print "Index= {}".format(_index)
            print "InImaging= {}".format(_in_imaging)
            print "MaxIndex= {}".format(_max_index)
            print "DisplayValue= {} ".format(display)
            print "NominalValue= {} ".format(nominal)
            print "IsCalibrated= {} ".format(is_calibrated)
            print "CalibratedValue= {}".format(calibrated_value)
            print "Rotation= {}".format(rotation)
            print "SubMode= {}".format(sub_mode)

    def test_available_mags(self):
        optics = self.tem_service.optics
        available_mags = optics.get_available_mags()
        for mag in available_mags:
            if self.diagnostics_print:
                print "Index = {}, Value= {}".format(mag[0], mag[1])
            index, is_imaging, _max_index, display, nominal, \
            is_calibrated, calibrated_value, rotation, sub_mode = \
                optics.get_magnification_info(mag[0])
            if self.diagnostics_print:
                print "  Index= {}".format(index)
                print "  InImaging= {}".format(is_imaging)
                print "  MaxIndex= {}".format(_max_index)
                print "  DisplayValue= {} ".format(display)
                print "  NominalValue= {} ".format(nominal)
                print "  IsCalibrated= {} ".format(is_calibrated)
                print "  CalibratedValue= {}".format(calibrated_value)
                print "  Rotation= {}".format(rotation)
                print "  SubMode= {}".format(sub_mode)

    def test_is_diffraction(self):
        optics = self.tem_service.optics
        is_diffraction = optics.is_diffraction()
        if self.diagnostics_print:
            print "IsDiffraction: ", is_diffraction

    def test_diffraction(self):
        optics = self.tem_service.optics
        org_is_diffraction = optics.is_diffraction()
        if self.diagnostics_print:
            print "Original IsDiffraction: ", org_is_diffraction
        try:
            optics.set_diffraction(diffraction_active=not org_is_diffraction)
            is_diffraction = optics.is_diffraction()
            if self.diagnostics_print:
                print "IsDiffraction: ", is_diffraction
            self.assertEqual(is_diffraction, not org_is_diffraction)
        finally:
            optics.set_diffraction(diffraction_active=org_is_diffraction)
            is_diffraction = optics.is_diffraction()
            if self.diagnostics_print:
                print "IsDiffraction: ", is_diffraction
            self.assertEqual(is_diffraction, org_is_diffraction)

    @unittest.skipIf(SYSTEM_TESTING, "will not restore, for manual testing only")
    def test_to_diffraction(self):
        optics = self.tem_service.optics
        optics.set_diffraction(diffraction_active=True)
        is_diffraction = optics.is_diffraction()
        if self.diagnostics_print:
            print "IsDiffraction: ", is_diffraction
        self.assertEqual(is_diffraction, True)

    @unittest.skipIf(SYSTEM_TESTING, "will not restore, for manual testing only")
    def test_to_imaging(self):
        optics = self.tem_service.optics
        optics.set_diffraction(diffraction_active=False)
        is_diffraction = optics.is_diffraction()
        if self.diagnostics_print:
            print "IsDiffraction: ", is_diffraction
        self.assertEqual(is_diffraction, False)

    def test_is_eftem(self):
        optics = self.tem_service.optics
        is_eftem = optics.is_eftem_mode()
        if self.diagnostics_print:
            print "IsEftem: ", is_eftem

    def test_eftem(self):
        optics = self.tem_service.optics
        org_is_eftem = optics.is_eftem_mode()
        if self.diagnostics_print:
            print "Original IsEftem: ", org_is_eftem
        try:
            optics.set_eftem_mode(eftem_mode_active=not org_is_eftem)
            is_eftem = optics.is_eftem_mode()
            if self.diagnostics_print:
                print "IsEftem: ", is_eftem
            self.assertEqual(is_eftem, not org_is_eftem)
        finally:
            optics.set_eftem_mode(eftem_mode_active=org_is_eftem)
            is_eftem = optics.is_eftem_mode()
            if self.diagnostics_print:
                print "IsEftem: ", is_eftem
            self.assertEqual(is_eftem, org_is_eftem)

    @unittest.skipIf(SYSTEM_TESTING, "will not restore, for manual testing only")
    def test_to_eftem_serie(self):
        optics = self.tem_service.optics
        optics.set_eftem_mode(eftem_mode_active=True)
        is_eftem = optics.is_eftem_mode()
        if self.diagnostics_print:
            print "IsEftem: ", is_eftem
        self.assertEqual(is_eftem, True)

    @unittest.skipIf(SYSTEM_TESTING, "will not restore, for manual testing only")
    def test_to_regular_serie(self):
        optics = self.tem_service.optics
        optics.set_eftem_mode(eftem_mode_active=False)
        is_eftem = optics.is_eftem_mode()
        if self.diagnostics_print:
            print "IsEftem: ", is_eftem
        self.assertEqual(is_eftem, False)

    def test_is_nano_probe(self):
        if not self.nano_probe_supported: self.skipTest("Nano probe is not supported")
        optics = self.tem_service.optics
        is_nano_probe = optics.is_nano_probe()
        if self.diagnostics_print:
            print "IsNanoProbe: ", is_nano_probe

    def test_is_nano_probe_available(self):
        optics = self.tem_service.optics
        is_nano_probe = optics.is_nano_probe_available()
        if self.diagnostics_print:
            print "IsNanoProbe available: ", is_nano_probe

    def test_is_nano_probe_allowed(self):
        if not self.nano_probe_supported: self.skipTest("Nano probe is not supported")
        optics = self.tem_service.optics
        is_nano_probe = optics.is_nano_probe_allowed()
        if self.diagnostics_print:
            print "IsNanoProbe allowed: ", is_nano_probe

    def test_nano_probe(self):
        if not self.nano_probe_supported: self.skipTest("Nano probe is not supported")
        optics = self.tem_service.optics
        org_is_nano_probe = optics.is_nano_probe()
        if self.diagnostics_print:
            print "Original IsNanoProbe: ", org_is_nano_probe
        if optics.is_nano_probe_allowed():
            try:
                optics.set_nano_probe(nano_probe_active=not org_is_nano_probe)
                is_nano_probe = optics.is_nano_probe()
                if self.diagnostics_print:
                    print "IsNanoProbe: ", is_nano_probe
                self.assertEqual(is_nano_probe, not org_is_nano_probe)
            finally:
                optics.set_nano_probe(nano_probe_active=org_is_nano_probe)
                is_nano_probe = optics.is_nano_probe()
                if self.diagnostics_print:
                    print "IsNanoProbe: ", is_nano_probe
                self.assertEqual(is_nano_probe, org_is_nano_probe)

    @unittest.skipIf(SYSTEM_TESTING, "will not restore, for manual testing only")
    def test_to_nano_probe(self):
        optics = self.tem_service.optics
        optics.set_nano_probe(nano_probe_active=True)
        is_nano_probe = optics.is_nano_probe()
        if self.diagnostics_print:
            print "IsNanoProbe: ", is_nano_probe
        self.assertEqual(is_nano_probe, True)

    @unittest.skipIf(SYSTEM_TESTING, "will not restore, for manual testing only")
    def test_to_micro_probe(self):
        optics = self.tem_service.optics
        optics.set_nano_probe(nano_probe_active=False)
        is_nano_probe = optics.is_nano_probe()
        if self.diagnostics_print:
            print "IsNanoProbe: ", is_nano_probe
        self.assertEqual(is_nano_probe, False)

    def test_is_lorentz(self):
        if not self.lorentz_supported: self.skipTest("Lorentz is not supported")
        optics = self.tem_service.optics
        is_lorentz = optics.is_lorentz()
        if self.diagnostics_print:
            print "IsLorentz: ", is_lorentz

    def test_is_lorentz_available(self):
        optics = self.tem_service.optics
        is_lorentz = optics.is_lorentz_available()
        if self.diagnostics_print:
            print "IsLorentz available: ", is_lorentz

    def test_is_lorentz_allowed(self):
        if not self.lorentz_supported: self.skipTest("Lorentz is not supported")
        optics = self.tem_service.optics
        is_lorentz = optics.is_lorentz_allowed()
        if self.diagnostics_print:
            print "IsLorentz allowed: ", is_lorentz

    def test_lorentz(self):
        if not self.lorentz_supported: self.skipTest("Lorentz is not supported")
        optics = self.tem_service.optics
        org_is_lorentz = optics.is_lorentz()
        if self.diagnostics_print:
            print "Original IsLorentz: ", org_is_lorentz
        if optics.is_lorentz_allowed():
            try:
                optics.set_lorentz(lorentz_active=not org_is_lorentz)
                is_lorentz = optics.is_lorentz()
                if self.diagnostics_print:
                    print "IsLorentz: ", is_lorentz
                self.assertEqual(is_lorentz, not org_is_lorentz)
            finally:
                optics.set_lorentz(lorentz_active=org_is_lorentz)
                is_lorentz = optics.is_lorentz()
                if self.diagnostics_print:
                    print "IsLorentz: ", is_lorentz
                self.assertEqual(is_lorentz, org_is_lorentz)

    @unittest.skipIf(SYSTEM_TESTING, "will not restore, for manual testing only")
    def test_lorentz_on(self):
        optics = self.tem_service.optics
        optics.set_lorentz(lorentz_active=True)
        is_lorentz = optics.is_lorentz()
        if self.diagnostics_print:
            print "IsLorentz: ", is_lorentz
        self.assertEqual(is_lorentz, True)

    @unittest.skipIf(SYSTEM_TESTING, "will not restore, for manual testing only")
    def test_lorentz_off(self):
        optics = self.tem_service.optics
        optics.set_lorentz(lorentz_active=False)
        is_lorentz = optics.is_lorentz()
        if self.diagnostics_print:
            print "IsLorentz: ", is_lorentz
        self.assertEqual(is_lorentz, False)

    def test_illuminated_area_diameter(self):
        original_illuminated_area = self.tem_service.optics.get_illuminated_area_diameter()
        if self.diagnostics_print:
            print 'original illuminated area: ', original_illuminated_area
        self.assertIsInstance(original_illuminated_area, float)

        # Try to change the value.
        target_illuminated_area = original_illuminated_area / 2
        self.tem_service.optics.set_illuminated_area_diameter(target_illuminated_area)
        returned_illuminated_area = self.tem_service.optics.get_illuminated_area_diameter()
        if self.diagnostics_print:
            print 'target illuminated area:   ', target_illuminated_area
            print 'returned illuminated area: ', returned_illuminated_area
        self.assertTrue(np.allclose([returned_illuminated_area], [target_illuminated_area]))

        # Restore the value.
        self.tem_service.optics.set_illuminated_area_diameter(original_illuminated_area)
        returned_illuminated_area = self.tem_service.optics.get_illuminated_area_diameter()
        if self.diagnostics_print:
            print 'restored illuminated area: ', returned_illuminated_area

    def test_is_illumination_mode_probe(self):
        _is_illumination_mode_probe = self.tem_service.optics.is_illumination_probe()
        if self.diagnostics_print:
            print "Is illumination mode probe= ", _is_illumination_mode_probe

    def test_illumination_mode(self):
        org_c3_off = self.tem_service.optics.is_illumination_free_c3_off()
        org_c2_off = self.tem_service.optics.is_illumination_free_c2_off()
        org_parallel = self.tem_service.optics.is_illumination_parallel()
        org_probe_normal_angle = self.tem_service.optics.is_illumination_probe_normal_angle()
        org_probe_large_angle = self.tem_service.optics.is_illumination_probe_large_angle()
        if self.diagnostics_print:
            print 'is_illumination_free_c3_off: ', org_c3_off
            print 'is_illumination_free_c2_off: ', org_c2_off
            print 'is_illumination_parallel: ', org_parallel
            print 'is_illumination_probe_normal_angle: ', org_probe_normal_angle
            print 'is_illumination_probe_large_angle: ', org_probe_large_angle

        self.tem_service.optics.set_illumination_parallel()
        self.assertTrue(self.tem_service.optics.is_illumination_parallel())

        self.tem_service.optics.set_illumination_free_c3_off()
        self.assertTrue(self.tem_service.optics.is_illumination_free_c3_off())

        self.tem_service.optics.set_illumination_probe_normal_angle()
        self.assertTrue(self.tem_service.optics.is_illumination_probe_normal_angle())

        self.tem_service.optics.set_illumination_free_c2_off()
        self.assertTrue(self.tem_service.optics.is_illumination_free_c2_off())

        self.tem_service.optics.set_illumination_probe_large_angle()
        self.assertTrue(self.tem_service.optics.is_illumination_probe_large_angle())

        if org_c3_off:
            self.tem_service.optics.set_illumination_free_c3_off()
        elif org_c2_off:
            self.tem_service.optics.set_illumination_free_c2_off()
        elif org_parallel:
            self.tem_service.optics.set_illumination_parallel()
        elif org_probe_normal_angle:
            self.tem_service.optics.set_illumination_probe_normal_angle()
        elif org_probe_large_angle:
            self.tem_service.optics.set_illumination_probe_large_angle()

    def test_get_current_optics_mode_state(self):
        current_state = self.tem_service.optics.get_current_optics_mode_state()

    def test_restore_optics_mode_state(self):
        current_state = self.tem_service.optics.get_current_optics_mode_state()
        self.tem_service.optics.restore_optics_mode_state(current_state)

    def test_set_basic_monochromator_tuning_mode(self):
        current_state = self.tem_service.optics.get_current_optics_mode_state()
        self.tem_service.optics.set_basic_monochromator_tuning_mode()
        self.tem_service.optics.restore_optics_mode_state(current_state)

# Low level integration tests - requires running server and OMP! That is, not a unit tests.
# Note that we tests the functionality via the parent class 'TemService', since this is the public
# interface that clients will use.
# These tests require the server to be in STEM mode
class TestOpticsServiceUsingOmpWithTemAccessInStem(TestOpticsServiceNotUsingOmpInStem):
    @classmethod
    def setUpClass(cls):
        # Create connection to underlying server once, i.e. not for each and every tests.
        cls.tem_service = TemService(use_omp=True, use_tem_access=True)
        cls.lorentz_supported =  False # cls.tem_service.optics.is_lorentz_available()
        cls.nano_probe_supported = False # cls.tem_service.optics.is_nano_probe_available()

# Low level integration tests - requires running server and OMP! That is, not a unit tests.
# Note that we tests the functionality via the parent class 'TemService', since this is the public
# interface that clients will use.
# These tests require the server to be in TEM mode
class TestOpticsServiceUsingOmpWithTemAccessInTem(TestOpticsServiceNotUsingOmpInTem):
        @classmethod
        def setUpClass(cls):
            # Create connection to underlying server once, i.e. not for each and every tests.
            cls.tem_service = TemService(use_omp=True, use_tem_access=True)
            cls.lorentz_supported = False  # cls.tem_service.optics.is_lorentz_available()
            cls.nano_probe_supported = False  # cls.tem_service.optics.is_nano_probe_available()

# Low level integration tests - requires running server and OMP! That is, not a unit tests.
# Note that we tests the functionality via the parent class 'TemService', since this is the public
# interface that clients will use.
# These tests require the server to be in STEM mode
class TestOpticsServiceUsingOmpNoTemAccessInStem(TestOpticsServiceNotUsingOmpInStem):
    @classmethod
    def setUpClass(cls):
        # Create connection to underlying server once, i.e. not for each and every tests.
        cls.tem_service = TemService(use_omp=True, use_tem_access=False)
        cls.lorentz_supported = False #cls.tem_service.optics.is_lorentz_available()
        cls.nano_probe_supported = False #cls.tem_service.optics.is_nano_probe_available()

# Low level integration tests - requires running server and OMP! That is, not a unit tests.
# Note that we tests the functionality via the parent class 'TemService', since this is the public
# interface that clients will use.
# These tests require the server to be in TEM mode
class TestOpticsServiceUsingOmpNoTemAccessInTem(TestOpticsServiceNotUsingOmpInTem):
            @classmethod
            def setUpClass(cls):
                # Create connection to underlying server once, i.e. not for each and every tests.
                cls.tem_service = TemService(use_omp=True, use_tem_access=False)
                cls.lorentz_supported = False  # cls.tem_service.optics.is_lorentz_available()
                cls.nano_probe_supported = False  # cls.tem_service.optics.is_nano_probe_available()