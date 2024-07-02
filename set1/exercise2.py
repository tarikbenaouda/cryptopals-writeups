from Cryptodome.Util.number import bytes_to_long, long_to_bytes
from binascii import hexlify, unhexlify

first_buffer = b"1c0111001f010100061a024b53535009181c"
second_buffer = b"686974207468652062756c6c277320657965"
print(hexlify(long_to_bytes(bytes_to_long(unhexlify(first_buffer)) ^ bytes_to_long(unhexlify(second_buffer)))))