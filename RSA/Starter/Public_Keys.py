def rsa_encrypt(message, e, p, q):
    # Calculate the modulus N = p * q
    N = p * q
    
    # Perform RSA encryption: c = m^e mod N
    ciphertext = pow(message, e, N)
    
    return ciphertext

# Given parameters
message = 12
e = 65537
p = 17
q = 23

# Encrypt the message
ciphertext = rsa_encrypt(message, e, p, q)

print(f"Message: {message}")
print(f"Public key (N, e): ({p*q}, {e})")
print(f"Ciphertext: {ciphertext}")