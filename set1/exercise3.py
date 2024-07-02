from binascii import unhexlify
from string import printable

hex_encoded_string = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"
bytes_encoded_string = unhexlify(hex_encoded_string)
for c in printable:
    key = ord(c)
    decrypted = bytes([byte ^ key for byte in bytes_encoded_string])
    if all([char in printable for char in decrypted.decode()]):
        print(c,decrypted.decode())
# Output: Cooking MC's like a pound of bacon , "X" used to xor the message