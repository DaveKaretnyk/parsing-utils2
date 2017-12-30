import unittest

import samples.miscellaneous.sample1

# from samples.miscellaneous.sample1 import *
# from samples.miscellaneous.sample1 import (
#    free_func_1, free_func_2, free_func_3, free_func_4, Silly1)


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
        self.assertEqual(free_func_1(), 4)

    def test_free_func_2(self):
        self.assertEqual(free_func_2(), 1)

    def test_free_func_3(self):
        self.assertEqual(free_func_3(), 1)

    def test_free_func_4(self):
        self.assertEqual(free_func_4(), 3)


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
        silly1 = Silly1()
        self.assertEqual(silly1.class_func_get1(), 'initial value')

    def test_class_func_set(self):
        silly1 = Silly1()
        silly1.class_func_set1('another value')
        self.assertEqual(silly1.class_func_get1(), 'another value')
