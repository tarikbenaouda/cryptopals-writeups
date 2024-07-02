from binascii import hexlify

repeating_key = "ICE"

def repeating_key_xor(plain_text, key):
    key_length = len(key)
    return bytes([byte ^ key[i % key_length] for i, byte in enumerate(plain_text)])

plain_text = b"Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"
cipher_text = repeating_key_xor(plain_text, bytes(repeating_key, "utf-8"))
print(hexlify(cipher_text).decode())
