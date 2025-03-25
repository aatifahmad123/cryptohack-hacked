import cypari2
import math
from decimal import *
getcontext().prec = 100

pari = cypari2.Pari()

PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103]
cipher = 1350995397927355657956786955603012410260017344805998076702828160316695004588429433

PRIMES_sqrt_pow2 = list(map(lambda x:Decimal(x).sqrt() * (16**64), PRIMES))

n = len(PRIMES)
C = int(Decimal(n).sqrt()) + 1

mat = pari.matrix(n+1, n+1)
for i in range(n):
    mat[i, i] = 1
    mat[n, i] = -C * PRIMES_sqrt_pow2[i]
mat[n, n] = C * cipher

trans_L = pari.qflll(mat)
print(''.join(list(map(chr, trans_L[0]))))
