N, x0 = input().split()
N = int(N)
x0 = float(x0)

coeffs = []
for _ in range(N + 1):
    coeffs.append(float(input()))

result = 0.0
power = N

for a in coeffs:
    if power > 0:
        result += a * power * (x0 ** (power - 1))
    power -= 1

print(f"{result:.3f}")
