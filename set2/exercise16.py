import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad

class Exercise16:
    def __init__(self):
        self.key = os.urandom(16)

    def encrypt(self, data):
        iv = os.urandom(16)
        data = data.replace(b';', b'%3B').replace(b'=', b'%3D')
        full_data = (
            b"comment1=cooking%20MCs;userdata="
            + data
            + b";comment2=%20like%20a%20pound%20of%20bacon"
        )
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        ciphertext =  cipher.encrypt(pad(full_data, AES.block_size))
        return {"iv":iv, "ciphertext":ciphertext}

    def decrypt(self, cryptogram):
        cipher = AES.new(self.key, AES.MODE_CBC, cryptogram['iv'])
        plaintext = cipher.decrypt(cryptogram['ciphertext'])
        return unpad(plaintext, AES.block_size)
    
    def validate(self, plaintext):
        KVs = plaintext.split(b';')
        if b'admin=true' in KVs:
            return True
        return False

Exercise16 = Exercise16()
cryptogram = Exercise16.encrypt(b'IamThirdBlock333XadminYtrue')
# Now I will flip the bits of the 3rd block to get the desired plaintext
X = cryptogram['ciphertext'][32] ^ ord(';') ^ ord('X')
Y = cryptogram['ciphertext'][38] ^ ord('=') ^ ord('Y')
bytearr = bytearray(cryptogram['ciphertext'])
bytearr[32] = X
bytearr[38] = Y
cryptogram['ciphertext'] = bytes(bytearr)
plaintext = Exercise16.decrypt(cryptogram)

print(plaintext)
assert Exercise16.validate(plaintext), "admin=true not found in plaintext"
