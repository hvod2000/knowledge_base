TYPES_TO_CODES = {int: ord("i"), str: ord("s")}
CODES_TO_TYPES = {code: typ for typ, code in TYPES_TO_CODES.items()}
SUPPORTED_TYPES = set(TYPES_TO_CODES)


def encode_type(typ: type):
    return bytes([TYPES_TO_CODES[typ]])


def decode_type(encoded: bytes, i: int):
    return CODES_TO_TYPES[encoded[i]], i + 1


def encode_str(string: str):
    return string.encode("utf-8") + b"\0"


def decode_str(data: bytes, i):
    j = data.index(b"\0", i)
    return data[i:j].decode("utf-8"), j + 1


def encode_int(number: int):
    # TODO: support encoding big numbers!!!
    return number.to_bytes(1, "little")


def decode_int(encoded: bytes, i: int):
    # TODO: support decoding big numbers!!!
    return encoded[i], i + 1


def encode_column(typ, values):
    header = encode_type(typ) + encode_int(len(values))
    if typ is int:
        return header + b"".join((map(encode_int, values)))
    return header + b"".join(s.encode("utf-8") + b"\0" for s in values)


def decode_column(encoded: bytes, i: int):
    typ, i = decode_type(encoded, i)
    length, i = decode_int(encoded, i)
    values = []
    if typ is int:
        for _ in range(length):
            value, i = decode_int(encoded, i)
            values.append(value)
    else:
        for _ in range(length):
            value, i = decode_str(encoded, i)
            values.append(value)
    return (typ, values), i


def encode_table(data, header=None, types=None):
    assert len(data) or types
    if types is None:
        types = [type(field) for field in data[0]]
    if header is None:
        header = [str(typ) for typ in types]
    encoded = [encode_int(len(header))]
    for column, column_header in enumerate(header):
        values = [row[column] for row in data]
        encoded.append(column_header.encode("utf-8") + b"\0")
        encoded.append(encode_column(types[column], values))
    return b"".join(encoded)


def decode_table(data: bytes, i: int = 0):
    width, i = decode_int(data, i)
    header, types, columns = [], [], []
    for _ in range(width):
        head, i = decode_str(data, i)
        (typ, values), i = decode_column(data, i)
        header.append(head)
        types.append(typ)
        columns.append(values)
    table = [[column[i] for column in columns] for i in range(len(columns[0]))]
    return (table, header, types)


def print_bytes(data: bytes):
    for i in range(0, len(data), 16):
        row = data[i : i + 16]
        hexes = " ".join(hex(byte)[2:].zfill(2) for byte in row)
        string = "".join(chr(b) if 32 <= b <= 126 else "▯" for b in row)
        print(hexes.ljust(50), string)


def test_tables():
    data = [[2, 3, "Hello there"], [4, 5, "Σe^ιτ=1"]]
    table = (data, [f"field{i}" for i in range(len(data[0]))])
    encoded = encode_table(*table)
    print(*table)
    print_bytes(encoded)
    print(*decode_table(encoded))


if __name__ == "__main__":
    test_tables()
