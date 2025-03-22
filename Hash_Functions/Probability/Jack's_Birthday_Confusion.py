import math

# Total number of possible hash values
H = 2**11  # 2048 possible hash values

# Function to calculate probability of collision for n values
def collision_probability(n, H):
    return 1 - math.exp(-n*(n-1)/(2*H))

# Binary search to find n for 75% probability
def find_n_for_probability(target_prob, H):
    low, high = 1, H
    while low <= high:
        mid = (low + high) // 2
        prob = collision_probability(mid, H)
        if abs(prob - target_prob) < 0.0001:  # Close enough
            return mid
        elif prob < target_prob:
            low = mid + 1
        else:
            high = mid - 1
    return low  # Return the smallest n that exceeds the target probability

n = find_n_for_probability(0.75, H)
print(f"Number of unique secrets needed: {n}")