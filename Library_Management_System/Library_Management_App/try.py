import random
import string
import base64

# Step 1: Generate a random string
def generate_random_string(length=10):
    letters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(letters) for i in range(length))
    return random_string

# Step 2: Encode the string using Base64
def encode_string(input_string):
    # Convert the string to bytes
    byte_string = input_string.encode('utf-8')
    # Encode the bytes
    base64_bytes = base64.b64encode(byte_string)
    # Convert the Base64 bytes back to a string
    encoded_string = base64_bytes.decode('utf-8')
    return encoded_string

# Step 3: Decode the Base64 encoded string
def decode_string(encoded_string):
    # Convert the string to bytes
    base64_bytes = encoded_string.encode('utf-8')
    # Decode the bytes
    byte_string = base64.b64decode(base64_bytes)
    # Convert the bytes back to a string
    decoded_string = byte_string.decode('utf-8')
    return decoded_string

# Example usage
random_string = generate_random_string()
print(f"Random String: {random_string}")

encoded_string = encode_string(random_string)
print(f"Encoded String: {encoded_string}")

decoded_string = decode_string(encoded_string)
print(f"Decoded String: {decoded_string}")