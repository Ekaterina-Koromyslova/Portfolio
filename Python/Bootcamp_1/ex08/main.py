n = int(input())
unique_numbers = set()

for _ in range(n):
    number = int(input())
    unique_numbers.add(number)

print(len(unique_numbers))