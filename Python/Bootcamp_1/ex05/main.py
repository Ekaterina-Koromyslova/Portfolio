def main():
    string = input().strip()

    if not string:
        print("Incorrect input")
        return
    
    sign = 1
    if string[0] == '-':
        sign = -1
        string = string[1:]
    elif string[0] == '+':
        string = string[1:]

    if not string:
        print("Incorrect input")
        return
    
    if string.count('.') > 1:
        print("Incorrect input")
        return
    
    if '.' in string:
        integer_part, fractional_part = string.split('.')

        if integer_part == "" or fractional_part == "":
            print("Incorrect input")
            return
    else:
        integer_part = string
        fractional_part = ""

    if not integer_part.isdigit():
        print("Incorrect input")
        return
    
    if fractional_part and not fractional_part.isdigit():
        print("Incorrect input")
        return

    integer_value = 0
    for c in integer_part:
        integer_value = integer_value * 10 + (ord(c) - ord('0'))

    fractional_value = 0
    divider = 10
    for c in fractional_part:
        fractional_value += (ord(c) - ord('0')) / divider
        divider *= 10

    value = (integer_value + fractional_value) * sign

    value *= 2

    print(format(value, ".3f"))

if __name__ == "__main__":
    main()

