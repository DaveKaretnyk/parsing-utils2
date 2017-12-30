

# The 'L' or 'l' postfix is 2.7 only. For 3.0 and later it is not allowed.
# Note also that the variant for specifying octal numbers without the letter 'O' or 'o' is only
# possible in 2.7, not 3.X.
def test_integer_suffix():
    my_int = 1234
    my_int_long = 1234L
    my_int_long2 = 1234l

    print('')
    print('my int:              ', my_int)
    print('my int long:         ', my_int_long)
    print('my int long2:        ', my_int_long2)

    my_hex = 0xABCD
    my_hex_long = 0xABCDL
    my_hex_long2 = 0xABCDl
    my_hex_long3 = 0Xabcdl

    print('')
    print('my hex:              ', my_hex)
    print('my hex long:         ', my_hex_long)
    print('my hex long2:        ', my_hex_long2)
    print('my hex long3:        ', my_hex_long3)

    my_oct = 0O1234
    my_oct_long = 0O1234L
    my_oct_long2 = 0O1234l
    my_oct_long3 = 0o1234l

    print('')
    print('my oct:              ', my_oct)
    print('my oct long:         ', my_oct_long)
    print('my oct long2:        ', my_oct_long2)
    print('my oct long3:        ', my_oct_long3)

    my_oct_no_letter = 01234
    my_oct_no_letter_long = 01234L
    my_oct_no_letter_long2 = 01234l

    print('')
    print('my oct (no letter):          ', my_oct_no_letter)
    print('my oct (no letter) long:     ', my_oct_no_letter_long)
    print('my oct (no letter) long2:    ', my_oct_no_letter_long2)

    my_binary = 0B010101
    my_binary_long = 0B010101L
    my_binary_long2 = 0B010101l
    my_binary_long3 = 0b010101l

    print('')
    print('my binary:           ', my_binary)
    print('my binary long:      ', my_binary_long)
    print('my binary long2:     ', my_binary_long2)
    print('my binary long3:     ', my_binary_long3)
