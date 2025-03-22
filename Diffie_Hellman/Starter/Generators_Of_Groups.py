def is_primitive_element(g, p):
    """
    Check if g is a primitive element of F_p.
    A primitive element generates all non-zero elements of F_p under multiplication.
    """
    # Compute p-1 (the order of the multiplicative group F_p*)
    order = p - 1
    
    # Find the prime factors of order
    factors = prime_factorization(order)
    
    # A number g is primitive if for every prime factor q of (p-1),
    # g^((p-1)/q) != 1 (mod p)
    for q in factors:
        # Calculate g^((p-1)/q) mod p
        exponent = order // q
        if pow(g, exponent, p) == 1:
            return False
    
    return True

def prime_factorization(n):
    """
    Return the unique prime factors of n.
    """
    i = 2
    factors = set()
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.add(i)
    if n > 1:
        factors.add(n)
    return factors

def find_smallest_primitive_element(p):
    """
    Find the smallest primitive element in F_p.
    """
    for g in range(2, p):
        if is_primitive_element(g, p):
            return g
    return None

# Given prime
p = 28151

# Find the smallest primitive element
smallest_primitive = find_smallest_primitive_element(p)
print(f"The smallest primitive element of F_{p} is: {smallest_primitive}")