import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64
from binascii import hexlify

HIDDEN_STRING = "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK"
KEY = os.urandom(16)

def encryption_oracle(plaintext):
    plaintext = plaintext + base64.b64decode(HIDDEN_STRING)
    plaintext = pad(plaintext, 16)
    cipher = AES.new(KEY, AES.MODE_ECB)
    return cipher.encrypt(plaintext)
# I skipped the part of encryption mode detection (done in exercise11.py)

# key size detection
for i in range(1,20):
    plain_text = i*2*b'A'
    cipher_text = encryption_oracle(plain_text)
    blocks = [cipher_text[j:j+i] for j in range(0, len(cipher_text), i)]
    if blocks[0] == blocks[1]:
        print(f"Key size is {i}")
        break
# Now I know the key size is 16
# Now I will decrypt the HIDDEN_STRING byte by byte
def decrypt_hidden_string():
    KEY_SIZE = 16
    hidden_string = b''
    for i in range(1, len(HIDDEN_STRING)+1):
        payload = b'A'*(KEY_SIZE - i % KEY_SIZE)
        cipher_text = encryption_oracle(payload)
        for j in range(256):
            test = payload + hidden_string + bytes([j])
            if encryption_oracle(test)[KEY_SIZE * (i // KEY_SIZE):KEY_SIZE * ((i // KEY_SIZE+1))] == cipher_text[KEY_SIZE * (i // KEY_SIZE):KEY_SIZE * ((i // KEY_SIZE+1))]:
                hidden_string += bytes([j])
                break
    return hidden_string

string = decrypt_hidden_string()
# string[-1] == 1 so The padding is 1 byte
string = string[:-1]
assert string.decode() == base64.b64decode(HIDDEN_STRING).decode() , "Failed"