import telnetlib
import json

r = telnetlib.Telnet("socket.cryptohack.org", 13403)

def readline():
    return r.read_until(b"\n")

def json_send(hsh):
    request = json.dumps(hsh).encode()
    r.write(request)

#read q
q = readline().split()[-1].decode()[1:-1]
q = int(q, 16)

#send g and n
g = q+1
n = q**2
json_send({"g":hex(g), "n":hex(n)})

#receive h
h = readline().split()[-1].decode()[1:-1]
h = int(h, 16)

# h = (q+1)^x mod q^2
# h = qx + 1
x = (h-1)//q

#send x to get flag
json_send({"x":hex(x)})
print(readline().decode())
#crypto{Grabbing_Flags_with_Pascal_Paillier}
