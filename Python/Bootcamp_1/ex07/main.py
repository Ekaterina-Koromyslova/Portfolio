def main():

    number_of_rows, number_of_columns = map(int, input().split())

    coin_field = []
    for _ in range(number_of_rows):
        row_values = list(map(int, input().split()))
        coin_field.append(row_values)

    best_path_sum = [[0] * number_of_columns for _ in range(number_of_rows)]

    best_path_sum[0][0] = coin_field[0][0]

    for column_index in range(1, number_of_columns):
        best_path_sum[0][column_index] = best_path_sum[0][column_index - 1] + coin_field[0][column_index]

    for row_index in range(1, number_of_rows):
        best_path_sum[row_index][0] = best_path_sum[row_index - 1][0] + coin_field[row_index][0]

    for row_index in range(1, number_of_rows):
        for column_index in range(1, number_of_columns):
            best_from_top = best_path_sum[row_index - 1][column_index]
            best_from_left = best_path_sum[row_index][column_index - 1]

            best_path_sum[row_index][column_index] = coin_field[row_index][column_index] + max(best_from_top, best_from_left)

    print(best_path_sum[number_of_rows - 1][number_of_columns - 1])


if __name__ == "__main__":
    main()
