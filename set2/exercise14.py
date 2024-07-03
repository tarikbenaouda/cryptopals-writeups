import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64
from random import randint

HIDDEN_STRING = "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK"

KEY = os.urandom(16)
random_count = randint(1, 10)
random_prefix = os.urandom(random_count) ## This is the new part

def encryption_oracle(plaintext):
    plaintext = random_prefix + plaintext + base64.b64decode(HIDDEN_STRING)
    plaintext = pad(plaintext, 16)
    cipher = AES.new(KEY, AES.MODE_ECB)
    return cipher.encrypt(plaintext)
# I skipped the part of encryption mode detection (done in exercise11.py)
# I skipped the key size detection part because it is the same as exercise12.py
# Detection of the length of the random prefix
def detect_prefix_length():
    previous = encryption_oracle(b'')[:16]
    # I will try to find the length of the prefix by adding bytes 
    # until the first block doesn't change (meaning the block is ct of the prefix + plaintext)
    for i in range(1, 100):
        plain_text = i*b'A'
        cipher_text = encryption_oracle(plain_text)
        current_block = cipher_text[:16]
        if current_block == previous:
            return 16 - i+1 # Length of the prefix
        previous = current_block
    else:
        raise Exception("Prefix length not found")
# Now I will decrypt the HIDDEN_STRING byte by byte

def attack():
    KEY_SIZE = 16
    hidden_string = b''
    random_prefix_length = detect_prefix_length()
    for i in range(1, len(HIDDEN_STRING)+1):
        prev = KEY_SIZE - i % KEY_SIZE
        payload = b'A'* (prev + KEY_SIZE - random_prefix_length)
        cipher_text = encryption_oracle(payload)
        for j in range(256):
            test = payload + hidden_string + bytes([j])
            if encryption_oracle(test)[KEY_SIZE * ((i // KEY_SIZE+1)):KEY_SIZE * ((i // KEY_SIZE+2))] == cipher_text[KEY_SIZE * ((i // KEY_SIZE+1)):KEY_SIZE * ((i // KEY_SIZE+2))]:
                hidden_string += bytes([j])
                break
    return hidden_string

string = attack()
# Removing padding
string = string[:-1]

assert string.decode() == base64.b64decode(HIDDEN_STRING).decode() , "Failed"