from base64 import b64decode
from string import printable

def hamming_distance(s1, s2):
    if len(s1) != len(s2):
        raise ValueError("Strings must be of equal length")
    return sum(1 for a, b in zip(s1, s2) if a != b)
average_distances = []
with open("./6.txt") as f:
    cipher_text = b64decode(f.read())
    for key_size in range(2, 41):
        blocks = [cipher_text[i:i+key_size] for i in range(0, len(cipher_text), key_size)]
        distances = []
        for i in range(len(blocks)-2):
            distances.append(hamming_distance(blocks[i], blocks[i+1]) / key_size)
        average_distances.append((key_size, sum(distances) / len(distances)))
average_distances.sort(key=lambda x: x[1])
probable_key_sizes = [t[0] for t in average_distances[0:7]]

def transpose_blocks(bt, key_size):
    blocks = []
    for i in range(key_size):
        blocks.append(bt[i::key_size])
    return blocks

with open("./6.txt") as f:
    cipher_text = b64decode(f.read())
    blocks = transpose_blocks(cipher_text, 29)
    block = blocks[2]  # I did it by iterating over all blocks and checking the output
    for c in printable:
        key = ord(c)
        decrypted = bytes([byte ^ key for byte in block])
        if all([char in list(bytes(printable,"utf-8")) for char in decrypted]):
            print("###########################")
            print(c,decrypted.decode())

#The key is "Terminator X: Bring the noise"
with open("./6.txt") as f:
    cipher_text = b64decode(f.read())
    key = b"Terminator X: Bring the noise"
    plain_text = bytes([byte ^ key[i % len(key)] for i, byte in enumerate(cipher_text)])
    print(plain_text.decode())