def square_generator(n):
    for i in range(n + 1):
        yield i * i


n = 5
for value in square_generator(n):
    print(value)