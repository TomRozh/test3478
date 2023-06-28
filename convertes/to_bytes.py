def to_bytes(data):
    bits = bin(data)[2:]

    out = []
    while len(bits) > 0:
        out.append(int(bits[-8:], 2))
        bits = bits[:-8]

    return out