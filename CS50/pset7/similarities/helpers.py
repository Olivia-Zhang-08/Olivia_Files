# Olivia Zhang, P-Set 7, Similarities, helpers.py

from nltk.tokenize import sent_tokenize


def lines(a, b):
    """Return lines in both a and b"""
    # a and b are file1 and file2 after having been opened and read

    # create set for both a and b for when they are split into lines
    alines = set(a.splitlines())
    blines = set(b.splitlines())

    # create set with the lines that are, identically, in both a and b
    samelines = alines & blines

    return samelines


def sentences(a, b):
    """Return sentences in both a and b"""

    # create sets for a and b that to store contents after split into sentences
    asents = set(sent_tokenize(a))
    bsents = set(sent_tokenize(b))

    # create set of the sentences that are, identically, in both a and b
    samesents = asents & bsents

    return samesents


def substrings(a, b, n):
    """Return substrings of length n in both a and b"""

    # create sets for a and b to store all possible substrings of length n
    asubstrings = set()
    bsubstrings = set()

    # find all possible substrings of length n and add to the corresponding set
    for i in range(len(a) - n + 1):
        asubstrings.add(a[i:(i + n)])
    for i in range(len(b) - n + 1):
        bsubstrings.add(b[i:(i + n)])

    # create set of the substrings that are, identically, in both a and b
    samesubstrings = asubstrings & bsubstrings

    return samesubstrings
