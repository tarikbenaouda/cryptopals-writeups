# The CBC padding oracle
import os 
import random
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Util.strxor import strxor_c
from base64 import b64decode

class Exercise17:
    KEY_SIZE = 16
    data = list(map(b64decode, [
        'MDAwMDAwTm93IHRoYXQgdGhlIHBhcnR5IGlzIGp1bXBpbmc=',
        'MDAwMDAxV2l0aCB0aGUgYmFzcyBraWNrZWQgaW4gYW5kIHRoZSBWZWdhJ3MgYXJlIHB1bXBpbic=',
        'MDAwMDAyUXVpY2sgdG8gdGhlIHBvaW50LCB0byB0aGUgcG9pbnQsIG5vIGZha2luZw==',
        'MDAwMDAzQ29va2luZyBNQydzIGxpa2UgYSBwb3VuZCBvZiBiYWNvbg==',
        'MDAwMDA0QnVybmluZyAnZW0sIGlmIHlvdSBhaW4ndCBxdWljayBhbmQgbmltYmxl',
        'MDAwMDA1SSBnbyBjcmF6eSB3aGVuIEkgaGVhciBhIGN5bWJhbA==',
        'MDAwMDA2QW5kIGEgaGlnaCBoYXQgd2l0aCBhIHNvdXBlZCB1cCB0ZW1wbw==',
        'MDAwMDA3SSdtIG9uIGEgcm9sbCwgaXQncyB0aW1lIHRvIGdvIHNvbG8=',
        'MDAwMDA4b2xsaW4nIGluIG15IGZpdmUgcG9pbnQgb2g=',
        'MDAwMDA5aXRoIG15IHJhZy10b3AgZG93biBzbyBteSBoYWlyIGNhbiBibG93'
    ]))
    def __init__(self):
        self.key = os.urandom(16)

    def encrypt(self):
        iv = os.urandom(16)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        plaintext = pad(random.choice(self.data), 16)
        cryptogram = {'iv': iv, 'ciphertext': cipher.encrypt(plaintext)}
        return cryptogram
    
    def decrypt(self, ciphertext, iv):
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        plaintext = cipher.decrypt(ciphertext)
        return unpad(plaintext, 16) # This will raise an exception if the padding is invalid
    
Exercise17 = Exercise17()

KEY_SIZE = Exercise17.KEY_SIZE

cryptogram = Exercise17.encrypt()

# This will raise an exception if the padding is invalid
def padding_oracle(ciphertext, iv):
    try :
        # Exercise17.decrypt(os.urandom(16), cryptogram['iv'])
        Exercise17.decrypt(ciphertext, iv)
        # print('No padding error')
        return True
    except Exception:
        # print('Padding error')
        return False

# Now I will xor the last byte of the last block with (for example) 0x01 
# The first bytes that will not return a padding error 
# will be the last byte of the unpadded plaintext
def detect_padding(cryptogram):
    for i in range(1,KEY_SIZE + 1):
        # I have added the IV as first block to get The padding in case of len(ciphertext) = 16
        iv = cryptogram['iv']
        ciphertext = iv + cryptogram['ciphertext']
        ciphertext = ciphertext[:-KEY_SIZE - i] + bytes([ciphertext[-KEY_SIZE - i] ^ 1]) + ciphertext[-KEY_SIZE - i + 1:]
    
        if padding_oracle(ciphertext, iv):
            return bytes([i - 1]) * (i - 1)
    else:
        return bytes([KEY_SIZE]) * KEY_SIZE

padding = detect_padding(cryptogram)
# At this point I know The padding of the ciphertext 
# Now I will decrypt the ciphertext byte by byte (flipping bytes) starting from the last byte

# So I decided to decrypt the whole plaintext recursively byte by byte :)
def decrypt(real_ct,ciphertext, iv, padding_len):
    last_byte = b''
    # Handling case of padding = KEY_SIZE
    if padding_len == KEY_SIZE:
        padding_len = 0
        real_ct = real_ct[:-KEY_SIZE]
        ciphertext = real_ct # We need to remove the last block
    # Stopping condition
    if len(ciphertext) == KEY_SIZE:
        return b''
    for i in range(256):
        new_ct = original = ciphertext # IV will be prepended to in the first call
        # I will xor the last byte of the last block with i 
        new_ct = (
            new_ct[:-KEY_SIZE - padding_len - 1] +
            bytes([i]) +
            strxor_c(new_ct[-KEY_SIZE - padding_len:-KEY_SIZE], (padding_len + 1) ^ padding_len) +
            new_ct[-KEY_SIZE:]
        )
        if padding_oracle(new_ct, iv):
            last_byte = bytes(
                [original[-KEY_SIZE - padding_len - 1] ^ i ^ (padding_len + 1)]
                )
            break

    return decrypt(real_ct,new_ct, iv, padding_len + 1) + last_byte

# Again: IV is prepended to the ciphertext to be used in first block decryption
plaintext = decrypt(
    cryptogram['iv'] + cryptogram['ciphertext'],
    # We are corrupting the n - 1 to decrypt the last block we need 
    # This first parameter to save the original ciphertext
    cryptogram['iv'] + cryptogram['ciphertext'],
    cryptogram['iv'],
    len(padding)
    )

assert (
    plaintext == Exercise17.decrypt(cryptogram['ciphertext'], cryptogram['iv'])
), 'Decryption failed'