
def free_func_1(x=3):
    print "hello "
#    print
    print "goodbye"
    print("Python 3.x hello")
    print "Python 2.x hello, with arg", 4
    print("Python 3.x hello, with arg", 4)
    print("Python 3.x hello, with formatted arg {0}".format(4))
    print "Python 2.x hello, with formatted arg {0}".format(4)
    return x+1


def free_func_2():
    return 1


def free_func_3():
    def my_local_func():
        return 0

    return my_local_func() + 1


def free_func_4():
    def my_local_func():
        def another_local_func():
            return 0

        return another_local_func() + 0

    return my_local_func() + 1


class Silly1(object):
    def __init__(self):
        self._something = 'initial value'

    def class_func_get1(self):
        return self._something

    def class_func_set1(self, new_value):
        self._something = new_value


class Silly2(object):
    def __init__(self):
        self._something = 'initial value'

    class InternalClass(object):
        def __init__(self):
            pass

        class InternalClass2(object):
            def __init__(self):
                pass

            def internal_class_method(self):
                pass

            def another_internal_method(self):
                pass

        def internal_class_method(self):
            pass

        def another_internal_method(self):
            pass

    def class_func_get2(self):
        return self._something

    def class_func_set2(self, new_value):
        self._something = new_value

    def class_func_another(self):
        pass

    def class_func_another2(self):
        pass


class Silly3(object):
    def __init__(self):
        self._something = 'initial value'

    def class_func_get1(self):

        def class_func_internal():
            pass

        class_func_internal()
        return self._something

    def class_func_set1(self, new_value):
        self._something = new_value

    def _class_func_xxx(self):

        def class_func_internal_xxx():
            pass

        class_func_internal_xxx()
        self._something = self._something


if __name__ == "__main__":
    print('Python 3.X print...')  # Python 3 print...
    print 'Python 2.X print...'   # Python 2 print...

    free_func_1(2)
    free_func_2()
    free_func_3()
    free_func_4()

    silly1 = Silly1()
    silly1.class_func_set1("blah")
    get_current = silly1.class_func_get1()
    print 'silly1 returned: ', get_current

    silly2 = Silly2()
    silly2.class_func_set2("haha")
    get_current = silly2.class_func_get2()
    print 'silly2 returned: ', get_current

    silly3 = Silly3()
    silly3.class_func_set1('hoho')
    get_current = silly3.class_func_get1()
    print 'silly3 returned: ', get_current

    x = 0
    try:
        _ = 100 / x

    # More usual way to write the except clause.
    except Exception as e:
        print "exception caught: ", e.message

    x = 0
    try:
        _ = 100 / x

    # Python 2.7.X - this is acceptable. For Python 3.X apparently not.
    except Exception, e:
        print "exception caught: ", e.message
