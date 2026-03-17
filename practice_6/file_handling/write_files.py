# Create a file and write sample data

with open("sample.txt", "w") as file:
    file.write("Name: Damilya\n")
    file.write("Age: 17\n")
    file.write("City: Almaty\n")

# Append new lines
with open("sample.txt", "a") as file:
    file.write("University: KBTU\n")
    file.write("Major: IT\n")

print("Data written to file")