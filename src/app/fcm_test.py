import firebase_admin
from firebase_admin import credentials
import firebase_admin.messaging as messaging
from starlette.config import Config
import json
import os
import base64


current_file_dir = os.path.dirname(os.path.realpath(__file__))

env_path = os.path.join(current_file_dir,"..", "..", ".env")

config = Config(env_path)

# json_private_key = config("CREDENTIAL_PRIVATE_KEY")

# encoded_private_key = base64.b64encode(json_private_key.encode()).decode()

# decoded_private_key = base64.b64decode(encoded_private_key).decode()

# # print("Decoded Private Key:", decoded_private_key)


# # print(encoded_private_key)

# # parsed_credentials = json.loads(config("CREDENTIALS"))

# my_credentials = {
#   "type": config("CREDENTIAL_TYPE"),
#   "project_id": config("CREDENTIAL_PROJECT_ID"),
#   "private_key_id": config("CREDENTIAL_PRIVATE_KEY_ID"),
#   "private_key": json.dumps(decoded_private_key),
#   "client_email": config("CREDENTIAL_CLIENT_EMAIL"),
#   "client_id": config("CREDENTIAL_CLIENT_ID"),
#   "auth_uri": config("CREDENTIAL_AUTH_URI"),
#   "auth_provider_x509_cert_url": config("CREDENTIAL_AUTH_PROVIDER"),
#   "token_uri": config("CREDENTIAL_TOKEN_URI"),
#   "client_x509_cert_url": config("CREDENTIAL_CERT_URL"),
#   "universe_domain": config("CREDENTIAL_UNIVERSE_DOMAIN")
# }


# json_data = json.dumps(my_credentials)

# credentials_dict = json.loads(json_data)

# print(json_data)

cred = credentials.Certificate("../../credentials.json")
default_app =  firebase_admin.initialize_app(cred)


def send_notification(title, msg, registration_token,data0bject=None):
    message = messaging.Message(
        notification = messaging.Notification(
            title= title,
            body = msg
        ),
        data={
            'testing': 'just seeinf',
            'time': '2:45',
        },
        token=registration_token,
    )


# Send a message to the device corresponding to the provided
# registration token.
    response = messaging.send(message)
# Response is a message ID string.
    print('Successfully sent message:', response)
