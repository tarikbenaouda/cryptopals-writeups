from binascii import unhexlify
from string import printable


def exercise3(hex_encoded_string):
    bytes_encoded_string = unhexlify(hex_encoded_string)
    for c in printable:
        key = ord(c)
        decrypted = bytes([byte ^ key for byte in bytes_encoded_string])
        if all([char in list(bytes(printable,"utf-8")) for char in decrypted]):
            print(c,decrypted.decode())

with open("set1/4.txt") as f:
    for line in f:
        exercise3(line.strip())