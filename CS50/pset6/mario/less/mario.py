# Olivia Zhang, P-Set 6, mario (less)
from cs50 import get_int

# Prompt user for pyramid height and keep prompting if input is not an integer between 1 and 8, inclusive.
while True:
    num = get_int("Positive number: ")
    if num > 0 and num <= 8:
        break

# Print out this many rows, with spaces and hashes accordingly to make a right-aligned pyramid
for i in range(num):
    print(" " * (num - i - 1), end="")
    print("#" * (i + 1), end="")
    print()