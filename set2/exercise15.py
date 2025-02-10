# PKCS#7 padding validation


def validate(plaintext,block_size):
    if len(plaintext) % block_size != 0:
        raise Exception("Invalid padding")
    padding = plaintext[-1]
    if padding == 0 or padding > block_size:
        raise Exception("Invalid padding")
    for i in range(padding):
        if plaintext[-1-i] != padding:
            raise Exception("Invalid padding")
    return True

assert validate(b'helloworldhelloworld\x02\x02',11), "Test case 1 failed"