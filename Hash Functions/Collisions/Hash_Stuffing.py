from pwn import *
import itertools

# Definitions from the provided source code
BLOCK_SIZE = 32
W = [0x6b17d1f2, 0xe12c4247, 0xf8bce6e5, 0x63a440f2, 0x77037d81, 0x2deb33a0, 0xf4a13945, 0xd898c296]
X = [0x4fe342e2, 0xfe1a7f9b, 0x8ee7eb4a, 0x7c0f9e16, 0x2bce3357, 0x6b315ece, 0xcbb64068, 0x37bf51f5]
Y = [0xc97445f4, 0x5cdef9f0, 0xd3e05e1e, 0x585fc297, 0x235b82b5, 0xbe8ff3ef, 0xca67c598, 0x52018192]
Z = [0xb28ef557, 0xba31dfcb, 0xdd21ac46, 0xe2a91e3c, 0x304f44cb, 0x87058ada, 0x2cb81515, 0x1e610046]

# Byte conversion 
W_bytes = b''.join([x.to_bytes(4,'big') for x in W])
X_bytes = b''.join([x.to_bytes(4,'big') for x in X])
Y_bytes = b''.join([x.to_bytes(4,'big') for x in Y])
Z_bytes = b''.join([x.to_bytes(4,'big') for x in Z])

def pad(data):
    padding_len = (BLOCK_SIZE - len(data)) % BLOCK_SIZE
    return data + bytes([padding_len]*padding_len)

def blocks(data):
    return [data[i:(i+BLOCK_SIZE)] for i in range(0,len(data),BLOCK_SIZE)]

def xor(a, b):
    return bytes([x^y for x,y in zip(a,b)])

def rotate_left(data, x):
    x = x % BLOCK_SIZE
    return data[x:] + data[:x]

def rotate_right(data, x):
    x = x % BLOCK_SIZE
    return data[-x:] + data[:-x]

def scramble_block(block):
    for _ in range(40):
        block = xor(W_bytes, block)
        block = rotate_left(block, 6)
        block = xor(X_bytes, block)
        block = rotate_right(block, 17)
    return block

def cryptohash(msg):
    initial_state = xor(Y_bytes, Z_bytes)
    msg_padded = pad(msg)
    msg_blocks = blocks(msg_padded)
    for i, b in enumerate(msg_blocks):
        mix_in = scramble_block(b)
        for _ in range(i):
            mix_in = rotate_right(mix_in, i+11)
            mix_in = xor(mix_in, X_bytes)
            mix_in = rotate_left(mix_in, i+6)
        initial_state = xor(initial_state, mix_in)
    return initial_state.hex()

def find_collision():
    # The key vulnerability is in the padding scheme
    # Messages that only differ in their padding can lead to the same hash value
    
    # If we create a message that is exactly BLOCK_SIZE - 1 bytes long,
    # it will be padded with a single byte of value 1
    msg1 = b'A' * (BLOCK_SIZE - 1)  # Will be padded with 0x01
    
    # If we create a message that is exactly BLOCK_SIZE bytes long with the last byte as 1,
    # it will have no padding (since it's already a multiple of BLOCK_SIZE)
    msg2 = b'A' * (BLOCK_SIZE - 1) + bytes([1])  # Already BLOCK_SIZE bytes, so no padding needed
    
    hash1 = cryptohash(msg1)
    hash2 = cryptohash(msg2)
    
    print(f"Message 1: {msg1.hex()}")
    print(f"Padded to: {pad(msg1).hex()}")
    print(f"Hash 1: {hash1}")
    print()
    print(f"Message 2: {msg2.hex()}")
    print(f"Padded to: {pad(msg2).hex()}")
    print(f"Hash 2: {hash2}")
    
    if hash1 == hash2:
        print("Collision found!")
        return msg1, msg2
    else:
        print("No collision found with this approach.")
        return None, None

def main():
    # Connect to the server
    r = remote('socket.cryptohack.org', 13405)
    print(r.recvline().decode())
    
    # Find a collision in the hash function
    msg1, msg2 = find_collision()
    
    if msg1 is not None and msg2 is not None:
        # Send the first message
        r.sendline(f'{{"msg": "{msg1.hex()}"}}'.encode())
        print(r.recvline().decode())
        
        # Send the second message
        r.sendline(f'{{"msg": "{msg2.hex()}"}}'.encode())
        print(r.recvline().decode())
    else:
        # Try alternative approach using length extension
        # Let's try with messages that will have the same padded representation
        # This is a different approach than the padding collision
        
        # Create a message that's exactly (BLOCK_SIZE-1) bytes
        base_msg = b'A' * (BLOCK_SIZE - 1)
        
        # When we pad this, we get a single byte of padding with value 1
        # So our message becomes: base_msg + bytes([1])
        # Which is exactly BLOCK_SIZE bytes
        padded_msg = pad(base_msg)
        
        # Now let's create another message that has the same padding pattern
        alt_msg = b'B' * (BLOCK_SIZE - 1)
        padded_alt = pad(alt_msg)
        
        print(f"Trying with base_msg: {base_msg.hex()}")
        print(f"Padded to: {padded_msg.hex()}")
        
        print(f"Trying with alt_msg: {alt_msg.hex()}")
        print(f"Padded to: {padded_alt.hex()}")
        
        # Send the first message
        r.sendline(f'{{"msg": "{base_msg.hex()}"}}'.encode())
        print(r.recvline().decode())
        
        # Send the second message
        r.sendline(f'{{"msg": "{alt_msg.hex()}"}}'.encode())
        response = r.recvline().decode()
        print(response)
        
        # Check if we need to try more approaches
        if "flag" not in response.lower():
            # Let's try a more general approach - we'll find two different messages that hash to the same value
            # The key vulnerability in this hash is likely in the padding or block processing
            
            # Let's try messages of length 0 and BLOCK_SIZE with proper padding to see if they collide
            empty_msg = b''
            empty_padded = pad(empty_msg)  # Should be BLOCK_SIZE bytes of value BLOCK_SIZE
            
            full_block_msg = bytes([BLOCK_SIZE]) * BLOCK_SIZE  # A full block with the padding value
            full_block_padded = pad(full_block_msg)  # Should be 2*BLOCK_SIZE bytes
            
            print(f"Trying with empty_msg: {empty_msg.hex()}")
            print(f"Padded to: {empty_padded.hex()}")
            
            print(f"Trying with full_block_msg: {full_block_msg.hex()}")
            print(f"Padded to: {full_block_padded.hex()}")
            
            # Send the empty message
            r.sendline(f'{{"msg": "{empty_msg.hex()}"}}'.encode())
            print(r.recvline().decode())
            
            # Send the full block message
            r.sendline(f'{{"msg": "{full_block_msg.hex()}"}}'.encode())
            print(r.recvline().decode())
    
    # Close the connection
    r.close()

if __name__ == "__main__":
    main()