from Crypto.Util.number import *
from Crypto.Cipher import AES
from pwn import remote
import hashlib
import json

r = remote('socket.cryptohack.org', 13371, level = 'DEBUG')

par = r.recvline(b'\n').lstrip(b"Intercepted from Alice: ").rstrip().decode()
param_a = json.loads(par)
p = param_a["p"]
g = param_a["g"]
A = param_a["A"]
print(p)
print(g)
print(A)
r.recv()
r.send(b'{"p": \"' + str(p).encode() + b'\", "g": \"' + str(g).encode() + b'\", "A": \"' + str(p).encode() + b'\"}')
ar = r.recvline(b'\n').lstrip(b"Intercepted from Bob: ").rstrip().decode()
param_b = json.loads(ar)
B = param_b["B"]
r.recv()
r.send(b'{"B": \"' + str(p).encode() + b'\"}')
real = r.recvline(b'\n').lstrip(b"Intercepted from Alice: ").rstrip().decode()
param_enc = json.loads(real)
iv = param_enc["iv"]
encrypted_flag = param_enc["encrypted_flag"]

def is_pkcs7_padded(message):
    padding = message[-message[-1]:]
    return all(padding[i] == len(padding) for i in range(0, len(padding)))

def pkcs7_unpad(message, block_size=16):
    if len(message) == 0:
        raise Exception("The input data must contain at least one byte")
    if not is_pkcs7_padded(message):
        return message
    padding_len = message[-1]
    return message[:-padding_len]

def decrypt_flag(shared_secret: int, iv: str, ciphertext: str):
    sha1 = hashlib.sha1()
    sha1.update(str(shared_secret).encode('ascii'))
    key = sha1.digest()[:16]
    ciphertext = bytes.fromhex(ciphertext)
    iv = bytes.fromhex(iv)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext)
    return pkcs7_unpad(plaintext).decode('ascii')

print(decrypt_flag(0,iv,encrypted_flag))

# crypto{n1c3_0n3_m4ll0ry!!!!!!!!}
