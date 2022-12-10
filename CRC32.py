def generate_crc32_table(_poly):
    custom_crc32_table = [0] * 256

    for i in range(256):
        c = i << 24

        for j in range(8):
            if c & 0x80000000:
                c = (c << 1) ^ _poly
            else:
                c = c << 1

        custom_crc32_table[i] = hex(c & 0xffffffff)
    return custom_crc32_table


crc32mpeg_poly = 0x04c11db7
crc_table = generate_crc32_table(crc32mpeg_poly)


def getCrc32(bytes_arr):
    length = len(bytes_arr)

    if bytes_arr != None:
        crc = 0xffffffff

        for i in range(0, length):
            crc = (crc << 8) ^ crc_table[(getReverse(bytes_arr[i], 8) ^ ) ]

