import os 
from Crypto.Cipher import AES
from random import randint
from Crypto.Util.Padding import pad
from binascii import hexlify

def encryption_oracle(plaintext):
    random_key = os.urandom(16)
    gen_random_bytes = lambda :os.urandom(randint(5, 10))
    plaintext = gen_random_bytes() + plaintext + gen_random_bytes()
    plaintext = pad(plaintext, 16)
    choice = randint(0, 1)
    if choice == 0:
        print('Encrypting using ECB')
        cipher = AES.new(random_key, AES.MODE_ECB)
        return cipher.encrypt(plaintext)
    else:
        print('Encrypting using CBC')
        IV = os.urandom(16)
        cipher = AES.new(random_key, AES.MODE_CBC, IV)
        return cipher.encrypt(plaintext)

# Now we need to detect the mode of encryption
# the idea here is : as an attacker I will send a plaintext that is repeated
# if the encryption is ECB then the repeated blocks will be encrypted to the same
# for example if the plaintext is 'A'*16*3 then the second 16 bytes 
# will be the same as the third 16 bytes (but not the first & last 16 bytes )
def detect_mode_of_encryption():
    plaintext = b'A'*16*4
    ciphertext = encryption_oracle(plaintext)
    blocks = [ciphertext[i:i+16] for i in range(0, len(ciphertext), 16)]
    if blocks[1] == blocks[2]:
        return 'ECB'
    return 'CBC'
# Testing
for i in range(10):
    print("#############################################")
    print(detect_mode_of_encryption())
