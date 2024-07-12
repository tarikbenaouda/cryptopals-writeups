from Crypto.Random import get_random_bytes
from base64 import b64decode
from string import ascii_letters, digits
from ptrlib import xor
from exercise18 import Exercise18


KEY_SIZE = 16
printable = ascii_letters + digits + ' ' + '.,?!\'\"' # put all characters that may appear in the plaintext
encrypt_ctr = Exercise18.encrypt_ctr
decrypt_ctr = Exercise18.decrypt_ctr

key = get_random_bytes(KEY_SIZE)  # 16 bytes key for AES-128
nonce = bytes(8) # fixing nonce to 0

ciphertexts = []
with open('set3/19.txt') as f:
    for line in f:
        plaintext = b64decode(line.strip())
        ciphertexts.append(encrypt_ctr(key, nonce, plaintext))

# The idea is that all the ciphertexts are encrypted with the same keystream
# So ? , The first byte of the keystream xor the first byte of each ciphertext
# should give the first byte of the plaintext (yeah plaintext)
# The longest ciphertext length is 36 so we need to find 3 keystreams
first_real_keystream = encrypt_ctr(key, nonce, bytes(KEY_SIZE))
print(first_real_keystream)
keystreams = []
for k in range(3):
    keystream = b''
    for j in range(KEY_SIZE):
        candidates = []
        for i in range(256):
            plaintexts = []
            for ciphertext in ciphertexts:
                try :
                    plaintexts.append(i ^ ciphertext[KEY_SIZE * k + j])
                except IndexError:
                    pass
            if all(chr(plaintext) in printable for plaintext in plaintexts):
                candidates.append({'byte': i, 'plaintexts': bytes(plaintexts)})
        print(candidates)
        chosen_byte = input('Enter the byte: ')
        keystream += bytes([int(chosen_byte)])
    keystreams.append(keystream)
for keystream in keystreams:
    print(len(keystream),keystream)

plaintexts = []
for ciphertext in ciphertexts:
    plaintexts.append(
        xor(ciphertext, b''.join(keystreams))
    )

print(plaintexts)

# This method is not perfect, but it works (by guessing the keystreams byte by byte)
