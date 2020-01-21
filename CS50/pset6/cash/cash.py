# Olivia Zhang, P-Set 6, Cash
from cs50 import get_float

# Prompt user for amount of change, and keep prompting until the input is positive number
while True:
    # Convert input into cents for subsequent calculations
    change = round(get_float("Change owed: ") * 100)
    if change > 0:
        break

# Initialize the counter for number of coins
numcoins = 0

# Divide input by largest coin value to find how many of those coins can be used
# Then use modulo to continue to the next, smaller coin value until the remainder of change is 0
numcoins += change // 25
change %= 25
numcoins += change // 10
change %= 10
numcoins += change // 5
change %= 5
numcoins += change

print(numcoins)
