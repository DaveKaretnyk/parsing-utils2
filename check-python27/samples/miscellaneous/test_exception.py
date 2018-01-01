
def method_throws_exception_2_7(diagnostics):
    x = 0
    try:
        _ = 100 / x

    # Python 2.7.X - this is acceptable. For Python 3.X apparently not.
    except Exception, e:
        if diagnostics:
            print "exception caught: ", e.message


def method_throws_exception(diagnostics):
    x = 0
    try:
        _ = 100 / x

    # More usual way to write the except clause.
    except Exception as e:
        if diagnostics:
            print "exception caught: ", e.message


class TestExceptions(object):
    @staticmethod
    def display_diagnostics():
        return False

    def test_method_throws_exception_2_7(self):
        method_throws_exception_2_7(self.display_diagnostics())

    def test_method_throws_exception(self):
        method_throws_exception(self.display_diagnostics())
