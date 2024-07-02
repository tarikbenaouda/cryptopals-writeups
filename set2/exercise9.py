from Crypto.Util.Padding import pad

data = b'YELLOW SUBMARINE'

padded_data = pad(data, 20)
# Padding bytes added according to the length of the data
print(padded_data)