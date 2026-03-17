import os

# Create nested directories
os.makedirs("dir1/dir2/dir3", exist_ok=True)

# List files and folders
print("Files and directories:")
for item in os.listdir("."):
    print(item)

# Find files with .txt extension
print("\nTXT files:")
for file in os.listdir("."):
    if file.endswith(".txt"):
        print(file)