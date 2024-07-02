from Crypto.Cipher import AES
from base64 import b64decode

# The cheating way
# def decrypt_aes_ecb(ciphertext, key):
#     cipher = AES.new(key, AES.MODE_CBC, b'\x00' * 16)
#     return cipher.decrypt(ciphertext)

# The proper way
def xor_bytes(a, b):
    return bytes([x ^ y for x, y in zip(a, b)])

def decrypt_aes_ecb(ciphertext, key):
    blocks = [ciphertext[i:i+16] for i in range(0, len(ciphertext), 16)]
    plaintext = b''
    cipher = AES.new(key, AES.MODE_ECB) # ECB mode used to avoid exception from new() method
    for i,block in enumerate(blocks[::-1]):
        prev_block = blocks[-i-2] if i < len(blocks) - 1 else b'\x00' * 16
        plaintext = xor_bytes(cipher.decrypt(block), prev_block) + plaintext
    return plaintext

with open('./10.txt', 'r') as f:
    ciphertext = b64decode(f.read())
    key = b'YELLOW SUBMARINE'
    print(decrypt_aes_ecb(ciphertext, key).decode('utf-8'))