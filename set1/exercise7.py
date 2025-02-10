from Crypto.Cipher import AES
from base64 import b64decode

def decrypt_aes_ecb(ciphertext, key):
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.decrypt(ciphertext)

with open('set1/7.txt', 'r') as f:
    ciphertext = b64decode(f.read())
    key = b'YELLOW SUBMARINE'
    print(decrypt_aes_ecb(ciphertext, key).decode('utf-8'))