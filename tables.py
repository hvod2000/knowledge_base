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
