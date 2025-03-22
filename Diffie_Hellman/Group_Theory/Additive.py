p = int(0xffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08ca237327ffffffffffffffff)
g = 2
A = int(0x9f2b5b29002971ca105353c786bd5bc6c718fe46e1c0cc3cca5c606202a7bb47b5df4b173077433d928cfb1156756e41f59048aac486bc81101dd2ed47e3e0792df60a8a8c4ea1d7627d7b21796be65b1ea5a476f949dc8e1082b7717c07e92549c7824e4c2f4277e956460fa7aae12134245c9d6449136e23eb80d0aa30616c0859b991bf023d47d1b5f7e2ebe9470fc337eb9a866e61bc1890dc3af297b75eb73243f88983be4ecd14a36442a0565e75be9f524e47d0bec24b5dcc75a49fbc)
B = int(0xd93713f9de43930cf920605a43494d967b7aa1e246d445e59b9a122870019a4bb5aedd0b0039bcb3aab2852fd108f4f2797769ea1b4012a6b146d089b1f648064eea25b50c81291d911e29c55a53c66c8d7504263c38f905cbc9e3e547c5db78c4aaba4fa906b5da16bff9e3c0982249c84fcd8ecf8d24e5f3b9d3d8e8fbdf8f54141f2917076baed7f4fc418a08bcd7e09708886d6d7cc453ab30df268d13072f53afe72112b43ea0e85d11ddee23b97d5e387f333d98a5450cfe3d4cba146c)
iv = "e1e8725946d21e3ae026b793d140b167"
ciphertext = "4a1b0c137f079ecacce32209a9c3e573094d8f017457ef93824aea30f82622949fa3d4ac05936ecea58a0ec40b6a3848"

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib

def is_pkcs7_padded(message):
    padding = message[-message[-1]:]
    return all(padding[i] == len(padding) for i in range(0, len(padding)))
def decrypt_flag(shared_secret: int, iv: str, ciphertext: str):
    sha1 = hashlib.sha1()
    sha1.update(str(shared_secret).encode('ascii'))
    key = sha1.digest()[:16]
    ciphertext = bytes.fromhex(ciphertext)
    iv = bytes.fromhex(iv)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext)

    if is_pkcs7_padded(plaintext):
        return unpad(plaintext, 16).decode('ascii')
    else:
        return plaintext.decode('ascii')
shared_secret = (pow(g,-1,p)*A*B)%p
print(decrypt_flag(shared_secret, iv, ciphertext))

# crypto{cycl1c_6r0up_und3r_4dd1710n?}
