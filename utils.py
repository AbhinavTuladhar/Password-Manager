"""
Stuff involving conversion of bytes to string and vice-versa.
"""
import base64
from hashlib import sha256


def get_hash(message):
    return sha256(message.encode()).hexdigest()


def bytes_to_string(message):
    decoded = base64.b64encode(message)
    return bytes.decode(decoded, encoding='utf-8')


def string_to_bytes(message):
    temp1 = message.encode('utf-8')
    temp2 = base64.b64decode(temp1)
    return temp2
