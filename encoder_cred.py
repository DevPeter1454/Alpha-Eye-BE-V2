import base64

with open('credentials.json', 'rb') as file:
    encoded_bytes = base64.b64encode(file.read())

encoded_string = encoded_bytes.decode('utf-8')

print(encoded_string)


def decode_base64(your_encoded_string):
    try:
        # Decode the Base64-encoded string
        decoded_bytes = base64.b64decode(your_encoded_string)

        # Convert bytes to string
        decoded_string = decoded_bytes.decode('utf-8')

        return decoded_string
    except Exception as e:
        print("Error decoding Base64 string:", e)
        return None


decoded_content = decode_base64(encoded_string)

if decoded_content:
    print("Decoded content:", decoded_content)
else:
    print("Decoding failed.")
