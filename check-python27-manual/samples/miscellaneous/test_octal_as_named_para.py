

# Construct taken from Standard Library, anydbm.py.
def my_open(file, flag='r', mode=0666):
    _ = file
    _ = flag
    print ''
    print 'mode: ', mode

    return 'OK'


def test_open():
    result = open('some file')
    print 'result:  ', result
