import math

# Total number of possible hash values
H = 2**11  # 2048 possible values

# Calculate n for 50% probability
n = math.log(0.5) / math.log(1 - 1/H)
print(f"Number of unique secrets needed: {math.ceil(n)}")