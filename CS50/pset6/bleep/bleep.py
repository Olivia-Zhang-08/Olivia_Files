# Olivia Zhang, P-Set 6, Bleep
import sys
from cs50 import get_string

# in this file, one function main is defined, which is called at the end of the file


def main():
    # accept only exactly 2 command-line arguments; if not 2, exit with usage message, which automates return 1
    if len(sys.argv) != 2:
        sys.exit("Usage: python bleep.py dictionary")

    # create set to store banned words
    bannedwords = set()

    # open imported dictionary and add to set of banned words
    txt = open(sys.argv[1], "r")
    for line in txt:
        bannedwords.add(line.rstrip("\n"))
    txt.close()

    # prompt user for message to censor and split into individual words in a list
    message = get_string("What message would you like to censor?\n")
    messagesplit = message.split()

    # check each word against the banned words list and censor with * accordingly
    for word in messagesplit:
        if word.lower() in bannedwords:
            print("*" * len(word), end=" ")
        else:
            print(word, end=" ")
    print()


# call main
if __name__ == "__main__":
    main()
