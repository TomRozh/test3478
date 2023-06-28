def to_int(bytes):
    out = ''
    bytes = bytes[::-1]
    for byte in bytes:
        byte_2 = bin(ord(byte))[2:]
        out += ('0' * (8 - len(byte_2))) + byte_2

    return int(out, 2)