def calculate_euler_totient(p, q):
    # Euler's totient for RSA: φ(N) = (p-1)(q-1)
    phi = (p - 1) * (q - 1)
    return phi

# Given prime factors
p = 857504083339712752489993810777
q = 1029224947942998075080348647219

# Calculate Euler's totient function
phi_n = calculate_euler_totient(p, q)

print(f"p = {p}")
print(f"q = {q}")
print(f"N = p * q = {p * q}")
print(f"φ(N) = {phi_n}")