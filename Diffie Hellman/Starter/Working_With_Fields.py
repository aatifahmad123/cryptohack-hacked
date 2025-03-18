def mod_inverse(g, p):
    """
    Find the multiplicative inverse of g modulo p
    where g * d ≡ 1 (mod p)
    
    This uses Fermat's Little Theorem, which states that when p is prime,
    g^(p-1) ≡ 1 (mod p) for any g not divisible by p.
    
    Therefore, g^(p-2) ≡ g^(-1) (mod p)
    """
    # First, let's check if g and p are coprime (which is guaranteed if p is prime and g < p)
    if p <= 0 or g <= 0 or g >= p:
        raise ValueError("Invalid input: p must be positive and g must be between 1 and p-1")
    
    # Fermat's Little Theorem approach
    return pow(g, p - 2, p)

# Given values
p = 991  # prime modulus
g = 209  # element to find inverse for

# Find the inverse
d = mod_inverse(g, p)

print(f"The multiplicative inverse of {g} modulo {p} is: {d}")
# Also verify the result
print(f"Verification: {g} * {d} mod {p} = {(g * d) % p}")