# Copyright (c) 2016 by FEI Company
# All rights reserved. This file includes confidential and proprietary
# information of FEI Company.
import time
import unittest

import numpy as np

from fei.infra.tem_server_access.api import TemService
from fei.infra.tem_server_access.pyom.data.microscope_image import MicroscopeImage
from fei.infra.tem_server_access.models.tests.helpers import change_value_and_restore_test


# Low level integration tests - requires running server! That is, not a unit tests.
# Note that we tests the functionality via the parent class 'TemService', since this is the public
# interface that clients will use.
class TestStemServiceNotUsingOmp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.use_omp = False
        # Create connection to underlying server once, i.e. not for each and every tests.
        cls.tem_service = TemService(use_omp=False, use_tem_access=True)

    def setUp(self):
        self.diagnostics_print = True

    def tearDown(self):
        pass

    def test_available_detectors(self):
        stem = self.tem_service.stem
        detectors = stem.get_available_detectors()
        if self.diagnostics_print:
            print "Available detectors: ", detectors

    def test_detector_selection_no_segments(self):
        stem = self.tem_service.stem
        org_selected = stem.get_selected()
        if self.diagnostics_print:
            print "Original selected detectors: ", org_selected
        detectors = stem.get_available_detectors()
        for detector in detectors:
            stem.select([detector], acquire_segments=False)
            selected = stem.get_selected()
            self.assertEqual(selected[0], detector)

        stem.select(detectors, acquire_segments=False)
        selected = stem.get_selected()
        self.assertItemsEqual(selected, detectors)

    def test_detector_insertion(self):
        stem = self.tem_service.stem
        org_inserted = stem.get_inserted()
        if self.diagnostics_print:
            print "Original inserted detectors: ", org_inserted
        stem.retract(org_inserted)
        inserted = stem.get_inserted()
        if self.diagnostics_print:
            print "Inserted detectors after retracted all: ", inserted
        self.assertEqual(len(inserted), 0, "List of inserted detectors should be empty")
        detectors = stem.get_available_detectors()
        for detector in detectors:
            if self.diagnostics_print:
                print "Inserting: {}".format(detector)
            stem.insert([detector])
            inserted = stem.get_inserted()
            if self.diagnostics_print:
                print "Inserted detectors after {} insert: {}".format(detector, inserted)
            self.assertEqual(inserted[0], detector)
            stem.retract([detector])
            inserted = stem.get_inserted()
            if self.diagnostics_print:
                print "Inserted detectors after retracted {}: ".format(detector, inserted)
            self.assertEqual(len(inserted), 0, "List of inserted detectors should be empty")

        stem.insert(org_inserted)
        inserted = stem.get_inserted()
        self.assertItemsEqual(inserted, org_inserted)

    def test_detector_selection_segments(self):
        stem = self.tem_service.stem
        org_selected = stem.get_selected()
        if self.diagnostics_print:
            print "Original selected detectors: ", org_selected
        detectors = stem.get_available_detectors()
        for detector in detectors:
            stem.select([detector], acquire_segments=True)
            selected = stem.get_selected()
            self.assertEqual(selected[0], detector)

        stem.select(detectors, acquire_segments=False)
        selected = stem.get_selected()
        self.assertItemsEqual(selected, detectors)

    def test_dwell_time(self):
        stem = self.tem_service.stem
        delta_value = 8e-3
        nr_places = 4
        change_value_and_restore_test(self, stem.set_dwell_time, stem.get_dwell_time,
                                      delta_value, nr_places)

    def test_scan_area(self):
        stem = self.tem_service.stem

        org_area = stem.get_scan_area()
        if self.diagnostics_print:
            print "Org scan area: ", org_area

        new_area = (0.5*org_area[0], 0.5*org_area[1], 0.5*org_area[2], 0.5*org_area[3])
        stem.set_scan_area(new_area)
        current_area = stem.get_scan_area()
        if self.diagnostics_print:
            print "new scan area: ", new_area
            print "Current scan area: ", current_area
        self.assertEqual(new_area, current_area)

        stem.set_scan_area(org_area)
        current_area = stem.get_scan_area()
        if self.diagnostics_print:
            print "Original scan area: ", org_area
            print "Current readout area: ", current_area
        self.assertEqual(org_area, current_area)

    def test_resolution(self):
        stem = self.tem_service.stem
        org = stem.get_resolution()
        if self.diagnostics_print:
            print "Org resolution: ", org
        new_resolution = 2*org
        if self.diagnostics_print:
            print "Setting resolution to: ", new_resolution
        stem.set_resolution(new_resolution)
        current = stem.get_resolution()
        if self.diagnostics_print:
            print "Current resolution: ", current
        self.assertAlmostEqual(new_resolution, current, 1)

        if self.diagnostics_print:
            print "Setting resolution to: ", org
        stem.set_resolution(org)
        current = stem.get_resolution()
        if self.diagnostics_print:
            print "Current resolution: ", current
        self.assertAlmostEqual(org, current, 1, "Error restoring x to original resolution")

    def test_mains_lock(self):
        stem = self.tem_service.stem
        org = stem.is_mains_lock_active()
        if self.diagnostics_print:
            print "Is mains lock active: ", org
        if self.diagnostics_print:
            print "Setting mains lock active to: ", (not org)
        stem.activate_mains_lock(not org)
        current = stem.is_mains_lock_active()
        if self.diagnostics_print:
            print "Is mains lock active: ", org
        self.assertEqual(current, not org)

        if self.diagnostics_print:
            print "Setting mains lock active to: ", (not org)
        stem.activate_mains_lock(org)
        current = stem.is_mains_lock_active()
        if self.diagnostics_print:
            print "Is mains lock active: ", org
        self.assertEqual(current, org, "Error restoring to original mains lock setting")

    def test_line_scan_orientation_vertical(self):
        stem = self.tem_service.stem
        org = stem.is_line_scan_orientation_vertical_active()
        if self.diagnostics_print:
            print "Is line_scan_orientation_vertical active: ", org
        if self.diagnostics_print:
            print "Setting line_scan_orientation_vertical active to: ", (not org)
        stem.activate_line_scan_orientation_vertical(not org)
        current = stem.is_line_scan_orientation_vertical_active()
        if self.diagnostics_print:
            print "Is line_scan_orientation_vertical active: ", current
        self.assertEqual(current, not org)

        if self.diagnostics_print:
            print "Setting line_scan_orientation_vertical active to: ", org
        stem.activate_line_scan_orientation_vertical(org)
        current = stem.is_line_scan_orientation_vertical_active()
        if self.diagnostics_print:
            print "Is line_scan_orientation_vertical active: ", current
        self.assertEqual(current, org,
                         "Error restoring to original line_scan_orientation_vertical setting")

    def test_acquire_images_no_segments(self):
        stem = self.tem_service.stem
        detectors = stem.get_available_detectors()
        nr_expected_images = len(detectors)
        if self.diagnostics_print:
            print "Selecting detectors: ", detectors
        stem.select(detectors, acquire_segments=False)
        stem.set_dwell_time(1e-6)
        stem.prepare_acq()
        images, pixel_size = stem.acquire_image(prepare=False, acquire_segments=False)
        nr_images = len(images)
        self.assertEqual(nr_images, nr_expected_images)
        for image in images:
            if self.use_omp:
                from fei.infra.tem_server_access.omp_stem.stem_detector import OmpMicroscopeImage
                self.assertIsInstance(image, OmpMicroscopeImage)
            else:
                self.assertIsInstance(image, MicroscopeImage)
            raw_data = image.raw_data
            self.assertIsInstance(raw_data, np.ndarray)

    def test_acquire_images_using_sw_sync(self):
        stem = self.tem_service.stem
        org_sw_sync = stem.is_sw_sync_active()
        try:
            stem.activate_sw_sync(True)
            detectors = stem.get_available_detectors()
            nr_expected_images = len(detectors)
            if self.diagnostics_print:
                print "Selecting detectors: ", detectors
            stem.select(detectors, acquire_segments=False)
            dwell_time = 0.1e-6
            resolution = 1024
            stem.set_dwell_time(dwell_time)
            stem.set_resolution(resolution)
            stem.prepare_acq()
            print "calculated frametime: {}".format(resolution * resolution * dwell_time)
            for i in range(0, 10, 1):
                start_time = time.time()
                images, pixel_size = stem.acquire_image(prepare=False, acquire_segments=False)
                end_time = time.time()
                print "Acq time: {}".format(end_time-start_time)
                nr_images = len(images)
                self.assertEqual(nr_images, nr_expected_images)
                for image in images:
                    if self.use_omp:
                        from fei.infra.tem_server_access.omp_stem.stem_detector \
                            import OmpMicroscopeImage
                        self.assertIsInstance(image, OmpMicroscopeImage)
                    else:
                        self.assertIsInstance(image, MicroscopeImage)
                    raw_data = image.raw_data
                    self.assertIsInstance(raw_data, np.ndarray)
        finally:
            stem.activate_sw_sync(org_sw_sync)

    def test_acquire_images_segments_not_combined(self):
        stem = self.tem_service.stem
        detectors = stem.get_available_detectors()

        used_detectors = detectors
        nr_expected_images = len(used_detectors)
        if "DF4" in detectors:
            used_detectors = ["DF4"]
            nr_expected_images = 4

        if self.diagnostics_print:
            print "Selecting detectors: ", used_detectors
        stem.select(used_detectors, acquire_segments=True, combined_segments=False)
        stem.set_dwell_time(1e-6)
        stem.prepare_acq()
        images, pixel_size = stem.acquire_image(prepare=False, acquire_segments=True, combined_segments=False)
        nr_images = len(images)
        self.assertEqual(nr_images, nr_expected_images)

        for image in images:
            if self.use_omp:
                from fei.infra.tem_server_access.omp_stem.stem_detector import OmpMicroscopeImage
                self.assertIsInstance(image, OmpMicroscopeImage)
            else:
                self.assertIsInstance(image, MicroscopeImage)
            raw_data = image.raw_data
            self.assertIsInstance(raw_data, np.ndarray)

    def test_acquire_images_segments_combined(self):
        stem = self.tem_service.stem
        detectors = stem.get_available_detectors()
        used_detectors = []
        nr_expected_images = 0
        if "DF4" in detectors:
            used_detectors.append("DF4")
            nr_expected_images += 2
        if "HAADF" in detectors:
            used_detectors.append("HAADF")
            nr_expected_images += 1
        if self.diagnostics_print:
            print "Selecting detectors: ", used_detectors
        stem.select(used_detectors, acquire_segments=True, combined_segments=True)
        stem.set_dwell_time(1e-6)
        stem.prepare_acq()
        images, pixel_size = stem.acquire_image(
            prepare=False, acquire_segments=True, combined_segments=True)
        nr_images = len(images)
        self.assertEqual(nr_images, nr_expected_images)

        for image in images:
            if self.use_omp:
                from fei.infra.tem_server_access.omp_stem.stem_detector import OmpMicroscopeImage
                self.assertIsInstance(image, OmpMicroscopeImage)
            else:
                self.assertIsInstance(image, MicroscopeImage)
            raw_data = image.raw_data
            self.assertIsInstance(raw_data, np.ndarray)

    def test_stem_acquisition_times_haadf(self):
        stem = self.tem_service.stem
        detectors = stem.get_available_detectors()

        if "HAADF" in detectors:
            stem.select(["HAADF"], acquire_segments=False)
            resolutions = [256, 512, 1024]
            for resolution in resolutions:
                stem.set_resolution(resolution)
                stem.set_scan_area((0, 0, 1, 1))
                dwell_times = [0.5e-6, 1.0e-6, 2.0e-6]
                for dwell_time in dwell_times:
                    stem.set_dwell_time(dwell_time)
                    start_time = time.time()
                    loop_time, line_time = stem.prepare_acq()
                    prepare_time = time.time()
                    images, pixel_size = stem.acquire_image(
                        prepare=False, acquire_segments=False,
                        combined_segments=False,show_debug=True)
                    acquisition_time = time.time()
                    print "Dwelltime\tResolution\tLoopTimeCalc\tLoopTimeEst\tPrepDuration\tTotalAcqDurationNoPrep"
                    print "{}\t{}\t{}\t{}\t{}\t{}".format(
                        dwell_time, resolution, dwell_time * resolution * resolution, loop_time,
                        (prepare_time - start_time), (acquisition_time - prepare_time))
                    print


# Low level integration tests - requires running server and OMP! That is, not a unit tests.
# Note that we tests the functionality via the parent class 'TemService', since this is the public
# interface that clients will use.
class TestStemServiceUsingOmpWithTemAccess(TestStemServiceNotUsingOmp):
    @classmethod
    def setUpClass(cls):
        cls.use_omp = True
        # Create connection to underlying server once, i.e. not for each and every tests.
        cls.tem_service = TemService(use_omp=True, use_tem_access=True)


# Low level integration tests - requires running server and OMP! That is, not a unit tests.
# Note that we tests the functionality via the parent class 'TemService', since this is the public
# interface that clients will use.
class TestStemServiceUsingOmpNoTemAccess(TestStemServiceNotUsingOmp):
    @classmethod
    def setUpClass(cls):
        cls.use_omp = True
        # Create connection to underlying server once, i.e. not for each and every tests.
        cls.tem_service = TemService(use_omp=True, use_tem_access=False)


class TestStemPerformance(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.use_omp = False
        # Create connection to underlying server once, i.e. not for each and every test.
        cls.tem_service = TemService(use_omp=False, use_tem_access=True)

    def setUp(self):
        self.diagnostics_print = True

    def tearDown(self):
        pass

    def test_stem_acquisition_times_haadf(self):
        from fei.infra.os.path_helpers import ensure_dir
        results_file = r"c:\temp\acq_times.txt"
        ensure_dir(results_file)
        stem = self.tem_service.stem
        detectors = stem.get_available_detectors()

        debug_output_results = []

        try:
            if "HAADF" in detectors:
                stem.select(["HAADF"], acquire_segments=False)
                resolutions = [512, 1024]
                for resolution in resolutions:
                    stem.set_resolution(resolution)
                    stem.set_scan_area((0, 0, 1, 1))
                    stem.activate_sw_sync(False)
                    dwell_times = [25e-9, 100e-9, 400e-9, 1.6e-6, 6.4e-6, 25.6e-6]
                    for dwell_time in dwell_times:
                        stem.set_dwell_time(dwell_time)
                        start_time = time.time()
                        loop_time, line_time = stem.prepare_acq()
                        prepare_time = time.time()

                        debug_output = {}
                        images, pixel_size = stem.acquire_image(prepare=False,
                                                                acquire_segments=False,
                                                                combined_segments=False,
                                                                show_debug=True,
                                                                debug_output=debug_output)
                        acquisition_time = time.time()
                        print "Dwelltime\tResolution\tLoopTimeCalc\tLoopTimeEst\tPrepDuration\tTotalAcqDurationNoPrep\tOverhead"
                        print "{}\t{}\t{}\t{}\t{}\t{}\t{}".format(
                            dwell_time, resolution, dwell_time * resolution * resolution, loop_time,
                            (prepare_time - start_time), (acquisition_time - prepare_time),
                                                    (acquisition_time - prepare_time) - loop_time)
                        debug_output["LoopTimeCalc"] = dwell_time * resolution * resolution
                        debug_output["LoopTimeEst"] = loop_time
                        debug_output["PrepDuration"] = (prepare_time - start_time)
                        debug_output["TotalAcqDurationNoPrep"] = (acquisition_time - prepare_time)
                        debug_output["OverheadNoPrep"] = (acquisition_time - prepare_time) - loop_time
                        debug_output_results.append(debug_output)
                        print
        finally:
            with open(results_file, "w") as f:
                header_line = "DwellTime\tResolution\tPrepDuration\tStartDuration\tWaitDuration\tImageRetrievalDuration" \
                              "\tTotalAcqDurationNoPrep\tLoopTimeCalc\tLoopTimeEst\tOverheadNoPrep\tOverheadPercentage\n"
                f.write(header_line)
                # write results file
                for debug_output in debug_output_results:
                    data_line = "{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}%\n".format(
                        debug_output["DwellTime"],
                        debug_output["Resolution"],
                        debug_output["PrepDuration"],
                        debug_output["StartDuration"],
                        debug_output["WaitDuration"],
                        debug_output["ImageRetrievalDuration"],
                        debug_output["TotalAcqDurationNoPrep"],
                        debug_output["LoopTimeCalc"],
                        debug_output["LoopTimeEst"],
                        debug_output["OverheadNoPrep"],
                        100.0 * debug_output["OverheadNoPrep"] / debug_output["LoopTimeCalc"])
                    f.write(data_line)
