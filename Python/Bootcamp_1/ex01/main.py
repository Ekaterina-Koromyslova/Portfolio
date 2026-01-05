import numpy as np

vector_a_str = input()
vector_b_str = input()

vector_a = np.array(list(map(float, vector_a_str.split())))
vector_b = np.array(list(map(float, vector_b_str.split())))

dot = vector_a @ vector_b

print(dot)