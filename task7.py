import os

file_path = "sample.txt"

try:
    with open(file_path, "r", encoding="utf-8") as file:
        input_string = file.read()
        reversed_string = input_string[::-1]

    dir_name, file_name = os.path.split(file_path)
    new_file_name = os.path.splitext(file_name)[0] + "_reversed.txt"
    new_file_path = os.path.join(dir_name, new_file_name)

    with open(new_file_path, "w", encoding="utf-8") as new_file:
        new_file.write(reversed_string)

    print(f"Reversed string saved to: {new_file_path}")
except FileNotFoundError:
    print("File not found!")