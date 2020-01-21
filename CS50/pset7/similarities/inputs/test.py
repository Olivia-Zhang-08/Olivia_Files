import sys
from cs50 import get_string
from nltk.tokenize import sent_tokenize

 # accept only exactly 2 command-line arguments; if not 2, exit with usage message, which automates return 1
if len(sys.argv) != 3:
    sys.exit("Usage: python helpers.py file1 file2")

#create set for both file1 and file2 to store the lines after they are stripped of \n
file1lines = set()
file2lines = set()
# create set to store the lines that are, identically, in both file1 and file2
samelines = set()

# open file1
file1 = open(sys.argv[1], "r")
file1lines = set(file1.splitlines())
# for line in file1:
#     file1lines.add(line.rstrip("\n"))
file1.close()
print(file1lines)

# open file2
file2 = open(sys.argv[2], "r")
file2lines = set(file2.splitlines())
# for line in file2:
#     file2lines.add(line.rstrip("\n"))
# file2.close()
print(file2lines)

# create set to store the lines that are, identically, in both file1 and file2
samelines = file1lines & file2lines
print("\n", samelines)

# asents = set(sent_tokenize(file1))
# bsents = set(sent_tokenize(file2))

# # Python code to remove duplicate elements
# def Remove(duplicate):
#     final_list = []
#     for num in duplicate:
#         if num not in final_list:
#             final_list.append(num)
#     return final_list