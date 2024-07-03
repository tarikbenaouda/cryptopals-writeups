import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad , unpad
from ptrlib import chunks

KEY = os.urandom(16)
def routine(string):
    KVs = string.split('&')
    dictionary = {}
    for KV in KVs:
        key, value = KV.split('=')
        dictionary[key] = value
    return dictionary

def profile_for(email):
    email = email.replace('&', '').replace('=', '')
    return 'email=' + email + '&uid=10&role=user'

def encrypt_profile(email, key):
    profile = pad(profile_for(email).encode(), 16)
    return AES.new(key, AES.MODE_ECB).encrypt(profile)
def decrypt_profile(ciphertext, key):
    return AES.new(key, AES.MODE_ECB).decrypt(ciphertext)

payload_1 = 'esi@gmail.com' 
# When we use this email blocks will be :
# ['email=esi@gmail.', 'com&uid=10&role=', 'user'] 
# Now will be able to change the last block to admin
payload_2 = 'nextBlock:'
admin_block = pad('admin'.encode(), 16)
admin_block_enc = encrypt_profile(payload_2 + admin_block.decode(), KEY)[16:32]
ciphertext = encrypt_profile(payload_1, KEY)
# replace the last block with the admin_block_enc
ciphertext = ciphertext[:32] + admin_block_enc
# Decrypt the ciphertext
plain = decrypt_profile(ciphertext, KEY)
# Remove padding
plain = unpad(plain, 16)
# Print the dictionary
parsed_profile = routine(plain.decode())

assert parsed_profile['role'] == 'admin', 'Failed'
