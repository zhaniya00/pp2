def divisible_by_3_and_4(n):
    for i in range(n + 1):
        if i % 12 == 0:
            yield i

n = int(input("Enter n: "))

for num in divisible_by_3_and_4(n):
    print(num)