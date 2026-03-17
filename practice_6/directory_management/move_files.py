import shutil

# Copy file to directory
shutil.copy("sample.txt", "dir1/sample.txt")

# Move file
shutil.move("sample.txt", "dir1/sample_moved.txt")

print("File moved and copied")