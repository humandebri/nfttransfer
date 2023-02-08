from ic.candid import encode
import math
import base64
from ic import Principal
import zlib

CRC_LENGTH_IN_BYTES = 4
HASH_LENGTH_IN_BYTES = 28
MAX_LENGTH_IN_BYTES = 29

def from_str(s):
    s1 = s.replace('-', '')
    pad_len = math.ceil(len(s1) / 8) * 8 - len(s1)
    b = base64.b32decode(s1.upper().encode() + b'=' * pad_len)
    if len(b) < CRC_LENGTH_IN_BYTES:
        raise "principal length error"
    p = Principal(bytes = b[CRC_LENGTH_IN_BYTES:])
    if not p.to_str() == s:
        raise "principal format error"
    return b

def to_str(bytes_m):
    checksum = zlib.crc32(bytes_m) & 0xFFFFFFFF
    b = b''
    b += checksum.to_bytes(CRC_LENGTH_IN_BYTES, byteorder='big')
    c =b + bytes_m
    s = base64.b32encode(bytes(c)).decode('utf-8').lower().replace('=', '')
    ret = ''
    while len(s) > 5:
        ret += s[:5]
        ret += '-'
        s = s[5:]
    ret += s
    return ret

def tokenIdentifier(canistar,indexno):
    index= list(indexno.to_bytes(4, 'big'))
    canistar_b=list(from_str(canistar))
    head=list("\x0Atid".encode())
    final_list =head + canistar_b +index
    final_list = final_list[:4]+final_list[8:]
    return to_str(bytes(final_list))
