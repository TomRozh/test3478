def xor(data):
    xor = 0
    try:
        for byte in data:
            xor ^= ord(byte)
    except:
        for byte in data:
            xor ^= byte
    return xor
