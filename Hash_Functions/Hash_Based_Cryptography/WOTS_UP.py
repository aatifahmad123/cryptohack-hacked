#!/usr/bin/env python3
import hashlib
import json
from Crypto.Cipher import AES

class Winternitz:
    def __init__(self):
        self.priv_key = []
        self.pub_key = []
        BYTE_MAX = 255
        KEY_LEN = 32

    def hash(self, data):
        return hashlib.sha256(data).digest()

    def sign(self, data):
        data_hash = self.hash(data)
        data_hash_bytes = bytearray(data_hash)
        sig = []
        for i in range(len(self.priv_key)):
            sig_item = self.priv_key[i]
            int_val = data_hash_bytes[i]
            hash_iters = 255 - int_val
            for _ in range(hash_iters):
                sig_item = self.hash(sig_item)
            sig.append(sig_item)
        return sig

# Load the data
with open('wots_up_data.json', 'r') as f:
    data = json.load(f)

# Debug prints
print("Signature (first element):", data.get('signature')[0])
print("First signature byte:", bytes.fromhex(data.get('signature')[0])[0])

# Derive private key
priv = [bytes.fromhex(data.get('signature')[0])]
while len(priv) != 32:
    priv.append(hashlib.sha256(priv[-1]).digest())

# Create Winternitz instance
w = Winternitz()
w.priv_key = priv

# Set up decryption
message2 = b"Sign for flag"
signature2 = w.sign(message2)

# Debug prints
print("Derived AES key:", bytes([s[0] for s in signature2]).hex())
print("IV:", data.get('iv'))
print("Encrypted text:", data.get('enc'))

ct, iv = map(bytes.fromhex, [data.get('enc'), data.get('iv')])
aes_key = bytes([s[0] for s in signature2])

# Decrypt and print flag
cipher = AES.new(aes_key, AES.MODE_CBC, iv)
decrypted = cipher.decrypt(ct)

# Print all debug information
print("Raw decrypted:", decrypted)
print("Raw decrypted (hex):", decrypted.hex())

# Remove PKCS7 padding
padding_length = decrypted[-1]
flag = decrypted[:-padding_length]

try:
    print("Decoded flag:", flag.decode())
except Exception as e:
    print("Decoding error:", e)
    print("Flag (hex):", flag.hex())
