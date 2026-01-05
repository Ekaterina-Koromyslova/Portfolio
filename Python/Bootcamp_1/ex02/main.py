n = int(input())

if n < 0:
    print(False)
else:
    reversed_number = 0
    temp = n

    while temp > 0:
        digit = temp % 10
        reversed_number = reversed_number * 10 + digit
        temp = temp // 10

    print(n == reversed_number)