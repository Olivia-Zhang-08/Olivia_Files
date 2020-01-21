# Olivia Zhang, P-Set 6, Caesar
import sys
from cs50 import get_string

# Make sure the user knows to only input one command-line argument, the key
if len(sys.argv) == 2:
    # The spec says we can assume the input will be a non-negative integer, no need to check if numeric
    # Convert the input from string type to integer type
    key = int(sys.argv[1])

    # Prompt user for plaintext and convert to ciphertext, preserving case
    message = get_string("plaintext: ")
    print("ciphertext: ", end="")
    for element in message:
        if element.islower():
            print(chr((ord(element) - 97 + key) % 26 + 97), end="")
        elif element.isupper():
            print(chr((ord(element) - 65 + key) % 26 + 65), end="")
        # Do not shift un-alphabetical characters
        else:
            print(element, end="")
    print()
else:
    # The following automatically results in an exit code of 1
    sys.exit("Usage: python caesar.py k")