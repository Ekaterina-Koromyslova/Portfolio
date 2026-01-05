def main():
    user_input = input().strip()

    if not user_input.isdigit() or int(user_input) < 1:
        print("Natural number was expected")
        return

    n = int(user_input)
    
    previous_row = [1]
    print_row(previous_row)

    for _ in range(1, n):
        next_row = []
        next_row.append(1)

        for i in range(len(previous_row) - 1):
            inner_value = previous_row[i] + previous_row[i + 1]
            next_row.append(inner_value)

        next_row.append(1)
        print_row(next_row)
        previous_row = next_row

def print_row(row):
    print(" ".join(map(str, row)))

if __name__ == "__main__":
    main()
