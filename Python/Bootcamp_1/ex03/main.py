from collections import deque

def read_from_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    matrix = []
    for line in lines:
        row = list(map(int, line.strip().split()))
        matrix.append(row)
    return matrix

def get_matrix_size(matrix):
    rows = len(matrix)
    if rows == 0:
        cols = 0
    else:
        cols = len(matrix[0])
    return rows, cols

def create_visited(rows, cols):
    visited = []
    for r in range(rows):
        row = []
        for c in range(cols):
            row.append(False)
        visited.append(row)
    return visited

def bfs(matrix, start_row, start_col, visited, total_rows, total_cols):
    queue = deque()
    queue.append((start_row,start_col))

    visited[start_row][start_col] = True

    figure_cells = [(start_row, start_col)]

    directions = [
        (-1, 0), # вверх
        (1, 0), # вниз
        (0, -1), # влево
        (0, 1) # вправо
    ]

    while queue:
        current_row, current_col = queue.popleft()

        for delta_row, delta_col in directions:
            neighbor_row = current_row + delta_row
            neighbor_col = current_col + delta_col

            if 0 <= neighbor_row < total_rows and 0 <= neighbor_col < total_cols:
                if matrix[neighbor_row][neighbor_col] == 1 and not visited[neighbor_row][neighbor_col]:
                    visited[neighbor_row][neighbor_col] = True
                    queue.append((neighbor_row, neighbor_col))
                    figure_cells.append((neighbor_row, neighbor_col))

    return figure_cells

def get_bounding_box(figure_cells):
    min_row = min(cell[0] for cell in figure_cells)
    max_row = max(cell [0] for cell in figure_cells)
    min_col = min(cell[1] for cell in figure_cells)
    max_col = max(cell[1] for cell in figure_cells)

    return min_row, max_row, min_col, max_col

def is_fully_filled(matrix, min_row, max_row, min_col, max_col):
    for row in range(min_row, max_row + 1):
        for col in range(min_col, max_col + 1):
            if matrix[row][col] != 1:
                return False
    return True

def get_figure_type(matrix, figure_cells):
    min_row, max_row, min_col, max_col = get_bounding_box(figure_cells)

    if is_fully_filled(matrix, min_row, max_row, min_col, max_col):
        return "square"
    else:
        return "circle"
    
def find_figures(matrix):
    rows, cols = get_matrix_size(matrix)
    visited = create_visited(rows, cols)

    figures = []

    for row in range(rows):
        for col in range(cols):
            if matrix[row][col] == 1 and not visited[row][col]:
                figure_cells = bfs(matrix, row, col, visited, rows, cols)
                figures.append(figure_cells)
    
    return figures

def count_figure_types(matrix, figures):
    square_count = 0
    circle_count = 0

    for figure_cells in figures:
        figure_type = get_figure_type(matrix, figure_cells)

        if figure_type == "square":
            square_count += 1
        else:
            circle_count += 1

    return square_count, circle_count

def main():
    matrix = read_from_file("input.txt")
    figures = find_figures(matrix)
    square_count, circle_count = count_figure_types(matrix, figures)
    print(square_count, circle_count)


if __name__ == "__main__":
    main()