from Crypto.Random import get_random_bytes
from base64 import b64decode
from string import ascii_letters, digits
from ptrlib import xor
from exercise18 import Exercise18


KEY_SIZE = 16
printable = ascii_letters + digits + ' ' + '.,?!\'\"/-:' # put all characters that may appear in the plaintext
encrypt_ctr = Exercise18.encrypt_ctr
decrypt_ctr = Exercise18.decrypt_ctr

key = get_random_bytes(KEY_SIZE)  # 16 bytes key for AES-128
nonce = bytes(8) # fixing nonce to 0
real_keystreams = encrypt_ctr(key, nonce, bytes(KEY_SIZE*4))
ciphertexts = []
with open('set3/20.txt') as f:
    lines = f.readlines()
    min_length = min(list(map(lambda l : len(b64decode(l.strip())), lines)))
    for line in lines:
        plaintext = b64decode(line.strip())[:min_length]
        ciphertexts.append(encrypt_ctr(key, nonce, plaintext))

# Now we have ciphertexts with same length and XORed against the same keystream with length
# of the ciphertexts. We can now use the same technique as in set1/exercise6.py to decrypt

def transpose_blocks(bt, key_size):
    blocks = []
    for i in range(key_size):
        blocks.append(bt[i::key_size])
    return blocks


blocks = transpose_blocks(b''.join(ciphertexts), len(ciphertexts[0]))

decrypted_blocks = []
for i,block in enumerate(blocks):
    for k in range(256):
        decrypted = xor(block, k)
        if all([char in list(bytes(printable,"utf-8")) for char in decrypted]):
            # print("###########################")
            decrypted_blocks.append({'key':i, 'plaintext':decrypted})
            # print(decrypted.decode())

keys =  list(map(lambda x: x['key'] , decrypted_blocks))
repeated_keys = list(set([item for item in keys if keys.count(item) > 1]))

# Repeated keys are 21, 29, 42, and 44
# I will select the repeated blocks manually

for k in repeated_keys:
    first = list(filter(lambda x: x['key'] == k, decrypted_blocks))[0]['plaintext']
    second = list(filter(lambda x: x['key'] == k, decrypted_blocks))[1]['plaintext']
    print(f"First: {first}")
    print(f"Second: {second}")
    choice = input("Choose the correct one: ")
    if choice == '0':
        decrypted_blocks = list(filter(lambda x: x['plaintext'] != second, decrypted_blocks))
    else:
        decrypted_blocks = list(filter(lambda x: x['plaintext'] != first, decrypted_blocks))
# Now we have the correct decrypted blocks , Just we still need to transpose them back
decrypted_blocks = list(map(lambda x: x['plaintext'], decrypted_blocks))

decrypted_blocks = transpose_blocks(b''.join(decrypted_blocks), len(decrypted_blocks[0]))

# Now we have the decrypted blocks, Let's print them (some of them still uncomplete we need 
# to decrypt the by guessing as we did in set3/exercise19.py
print(len(decrypted_blocks))    
for block in decrypted_blocks:
    print(block.decode())