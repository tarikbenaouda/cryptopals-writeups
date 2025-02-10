from binascii import unhexlify

def detect_aes_ecb(ciphertext):
    blocks = [ciphertext[i:i+16] for i in range(0, len(ciphertext), 16)]
    return len(blocks) != len(set(blocks))


with open('set1/8.txt') as f:
    lines = f.readlines()
    for line in lines: 
        if detect_aes_ecb(unhexlify(line.strip())):
            print(line.strip())
