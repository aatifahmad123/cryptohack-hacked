def decrypt_rsa(ciphertext, d, N):
    # RSA decryption: m = c^d mod N
    message = pow(ciphertext, d, N)
    return message

# Given parameters
N = 882564595536224140639625987659416029426239230804614613279163
e = 65537
ciphertext = 77578995801157823671636298847186723593814843845525223303932

# We need to calculate the private key d
# First, we need to find p and q (the prime factors of N)
# From the previous challenge:
p = 857504083339712752489993810777
q = 1029224947942998075080348647219

# Calculate Euler's totient: φ(N) = (p-1)(q-1)
phi = (p - 1) * (q - 1)

# Calculate private key: d ≡ e^(-1) mod φ(N)
d = pow(e, -1, phi)

# Decrypt the ciphertext
decrypted_message = decrypt_rsa(ciphertext, d, N)

print(f"Ciphertext: {ciphertext}")
print(f"Private key d: {d}")
print(f"Decrypted message: {decrypted_message}")