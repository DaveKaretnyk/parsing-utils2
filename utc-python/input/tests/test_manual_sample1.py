# Copyright (c) 2017 by FEI Company
# All rights reserved. This file includes confidential and proprietary
# information of FEI Company.
import unittest

from input.sample1 import (
    free_func_1, free_func_2, free_func_3, free_func_4)


class Test_sample1(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.diagnostics_print = False

    def tearDown(self):
        pass

    def test_free_func_1(self):
        self.assertTrue(False)

    def test_free_func_2(self):
        self.assertTrue(False)

    def test_free_func_3(self):
        self.assertTrue(False)

    def test_free_func_4(self):
        self.assertTrue(False)


class TestSilly1(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.diagnostics_print = False

    def tearDown(self):
        pass

    def test_class_func_get(self):
        self.assertTrue(False)

    def test_class_func_set(self):
        self.assertTrue(False)
