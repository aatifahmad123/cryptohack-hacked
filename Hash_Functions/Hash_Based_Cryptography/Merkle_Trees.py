import hashlib

def hash256(data):
    return hashlib.sha256(bytes.fromhex(data)).digest()

def merge_nodes(a, b):
    return hashlib.sha256(bytes.fromhex(a) + bytes.fromhex(b)).digest()

def verify_merkle_tree(a, b, c, d, root):
    # Compute left subtree
    left_leaf = merge_nodes(a, b)
    
    # Compute right subtree
    right_leaf = merge_nodes(c, d)
    
    # Compute root
    computed_root = merge_nodes(left_leaf.hex(), right_leaf.hex())
    
    # Check if computed root matches given root
    return computed_root.hex() == root

def solve_merkle_challenge(filename):
    flag_bits = []
    
    with open(filename, 'r') as f:
        for line in f:
            # Safely evaluate the line
            tree = eval(line.strip())
            a, b, c, d, root = tree
            
            # Verify the Merkle tree and record the bit
            flag_bits.append('1' if verify_merkle_tree(a, b, c, d, root) else '0')
    
    # Convert binary to ASCII
    flag = ''.join(flag_bits)
    print("Full binary string:", flag)
    print("Binary string length:", len(flag))
    
    # Convert binary to bytes, handling potential decoding issues
    try:
        # Pad the binary string to ensure it's a multiple of 8
        while len(flag) % 8 != 0:
            flag = '0' + flag
        
        # Convert to bytes
        byte_result = bytes(int(flag[i:i+8], 2) for i in range(0, len(flag), 8))
        
        # Try different decodings
        try:
            result = byte_result.decode('utf-8')
        except UnicodeDecodeError:
            try:
                result = byte_result.decode('latin-1')
            except UnicodeDecodeError:
                result = byte_result.hex()
        
        return result
    except Exception as e:
        print("Error converting flag:", e)
        return flag

# Run the solver
print(solve_merkle_challenge('merkle_trees_output.txt'))
