names = ["Ali", "Dana", "Aruzhan"]
scores = [90, 85, 95]

# enumerate example
print("Enumerate:")
for index, name in enumerate(names):
    print(index, name)

# zip example
print("\nZip:")
for name, score in zip(names, scores):
    print(name, score)

# type checking and conversion
value = "123"

print("\nType before:", type(value))

value = int(value)

print("Type after:", type(value))
print("Value + 10 =", value + 10)