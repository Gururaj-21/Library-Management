import random
import string
import base64


def generate_random_string(length=10):
    letters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(letters) for i in range(length))
    return random_string


def encode_string(input_string):
    # Convert the string to bytes
    byte_string = input_string.encode('utf-8')
    # Encode the bytes
    base64_bytes = base64.b64encode(byte_string)
    # Convert the Base64 bytes back to a string
    encoded_string = base64_bytes.decode('utf-8')
    return encoded_string


def decode_string(encoded_string):
    # Convert the string to bytes
    base64_bytes = encoded_string.encode('utf-8')
    # Decode the bytes
    byte_string = base64.b64decode(base64_bytes)
    # Convert the bytes back to a string
    decoded_string = byte_string.decode('utf-8')
    return decoded_string