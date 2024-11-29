def calculate_sum(n):
    return n * (n + 1) // 2

def process_string(input_string):
    string_length = len(input_string)
    word_count = len(input_string.split())
    char_count = len(input_string.replace(" ", ""))
    word_length_dict = {word: len(word) for word in input_string.split()}
    return string_length, word_count, char_count, word_length_dict

input_data = "First day in Vissoft"

if input_data.isdigit():
    n = int(input_data)
    print(f"The sum from 1 to {n} is: {calculate_sum(n)}")
else:
    string_length, word_count, char_count, word_length_dict = process_string(input_data)
    print(f"String length: {string_length}")
    print(f"Word count: {word_count}")
    print(f"Character count (excluding spaces): {char_count}")
    print(f"Word length dictionary: {word_length_dict}")