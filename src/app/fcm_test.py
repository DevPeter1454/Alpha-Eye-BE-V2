import firebase_admin
from firebase_admin import credentials
import firebase_admin.messaging as messaging

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
