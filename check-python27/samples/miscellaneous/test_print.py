
def some_function(x=3):
    print "hello "
    print
    print "goodbye"

    # print with brackets is possible in Python 2.7.X, mandatory in 3.X
    print("Python 3.x hello")
    print "Python 2.x hello, with arg", 4
    print("Python 3.x hello, with arg", 4)
    print("Python 3.x hello, with formatted arg {0}".format(4))
    print "Python 2.x hello, with formatted arg {0}".format(4)
    return x+1


def test_some_function():
    assert some_function(3) == 4
