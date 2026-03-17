# Read and print file contents

with open("sample.txt", "r") as file:
    content = file.read()
    print(content)