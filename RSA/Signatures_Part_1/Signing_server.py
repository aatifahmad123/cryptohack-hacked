from pwn import *
from Crypto.Util.number import *
r = remote('socket.cryptohack.org', 13374)
print(r.recvline())
r.sendline(b'{"option": "get_secret"}')
x = eval(r.recvline().decode().strip('\n'))["secret"]
print(x)
print(b'{"option": "sign", "msg": \"' + str(x).encode() + b'\"}')
r.sendline(b'{"option": "sign", "msg": \"' + str(x).encode() + b'\"}')
x = int(eval(r.recvline().decode().strip('\n'))["signature"][2:],16)
print(long_to_bytes(x))

# crypto{d0n7_516n_ju57_4ny7h1n6}