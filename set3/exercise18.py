from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

class Exercise18:
    def __init__(self):
        pass

    @staticmethod
    def encrypt_ctr(key, nonce, plaintext):
        cipher = AES.new(key, AES.MODE_CTR, nonce=nonce)
        ciphertext = cipher.encrypt(plaintext)
        return ciphertext
    @staticmethod
    def decrypt_ctr(key, nonce, ciphertext):
        cipher = AES.new(key, AES.MODE_CTR, nonce=nonce)
        plaintext = cipher.decrypt(ciphertext)
        return plaintext
def __main():
    encrypt_ctr = Exercise18.encrypt_ctr
    decrypt_ctr = Exercise18.decrypt_ctr
    # Example usage
    key = get_random_bytes(16)  # 16 bytes key for AES-128
    nonce = get_random_bytes(8)  # 8 bytes nonce
    plaintext = b'This is a secret message'

    ciphertext = encrypt_ctr(key, nonce, plaintext)
    decrypted = decrypt_ctr(key, nonce, ciphertext)

    print(f'Key: {key.hex()}')
    print(f'Nonce: {nonce.hex()}')
    print(f'Ciphertext: {ciphertext.hex()}')
    print(f'Decrypted: {decrypted.decode()}')

if __name__ == '__main__':
    __main()
