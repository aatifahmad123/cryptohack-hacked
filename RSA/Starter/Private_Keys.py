def calculate_private_key(p, q, e):
    # Calculate Euler's totient: φ(N) = (p-1)(q-1)
    phi = (p - 1) * (q - 1)
    
    # Calculate the modular multiplicative inverse of e modulo φ(N)
    # d ≡ e^(-1) mod φ(N)
    d = pow(e, -1, phi)
    
    return d

# Given parameters
p = 857504083339712752489993810777
q = 1029224947942998075080348647219
e = 65537

# Calculate the private key
private_key = calculate_private_key(p, q, e)

print(f"p = {p}")
print(f"q = {q}")
print(f"e = {e}")
print(f"Private key d = {private_key}")