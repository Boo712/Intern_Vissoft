file_path = "sample.txt"

try:
    with open(file_path, "r", encoding="utf-8") as file:
        input_string = file.read()

        string_length = len(input_string)
        word_count = len(input_string.split())
        char_count = len(input_string.replace(" ", ""))

        print(f"String length: {string_length}")
        print(f"Word count: {word_count}")
        print(f"Character count (excluding spaces): {char_count}")
except FileNotFoundError:
    print("File not found!")