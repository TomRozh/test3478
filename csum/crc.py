def crc16(data):
    # init
    CRC16_CCITT_POLY = 0x1021
    crc = 0xffff

    # update
    for byte in data:
        v = 0x80
        for i in range(8):
            xor_flag = (crc & 0x8000) != 0

            crc <<= 1
            crc &= 0xffff

            if (ord(byte) & v) != 0:
                crc += 1

            if xor_flag:
                crc ^= CRC16_CCITT_POLY

            v >>= 1

    # finalize
    for i in range(16):
        xor_flag = (crc & 0x8000) != 0

        crc <<= 1
        crc &= 0xffff

        if xor_flag:
            crc ^= CRC16_CCITT_POLY

    return crc
