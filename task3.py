input_string = "First day in Vissoft"

string_length = len(input_string)
word_count = len(input_string.split())
char_count = len(input_string.replace(" ", ""))

print(f"String length: {string_length}")
print(f"Word count: {word_count}")
print(f"Character count (excluding spaces): {char_count}")