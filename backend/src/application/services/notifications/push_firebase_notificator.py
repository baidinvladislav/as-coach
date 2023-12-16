import json
from dataclasses import dataclass, asdict

from firebase_admin import initialize_app, messaging, credentials

from src.config import (
    FIREBASE_TYPE,
    FIREBASE_PROJECT_ID,
    FIREBASE_PRIVATE_KEY_ID,
    FIREBASE_PRIVATE_KEY,
    FIREBASE_CLIENT_EMAIL,
    FIREBASE_CLIENT_ID,
    FIREBASE_AUTH_URI,
    FIREBASE_TOKEN_URI,
    FIREBASE_AUTH_PROVIDER_CERT_URL,
    FIREBASE_CLIENT_CERT_URL,
    FIREBASE_UNIVERSE_DOMAIN,
)
from src.application.services.notifications.notificator import AbstractNotificator


class PushNotificationEmptyDataMessage(Exception):
    pass


@dataclass
class FirebaseConfig:
    type: str = FIREBASE_TYPE
    project_id: str = FIREBASE_PROJECT_ID
    private_key_id: str = FIREBASE_PRIVATE_KEY_ID
    private_key: str = FIREBASE_PRIVATE_KEY
    client_email: str = FIREBASE_CLIENT_EMAIL
    client_id: str = FIREBASE_CLIENT_ID
    auth_uri: str = FIREBASE_AUTH_URI
    token_uri: str = FIREBASE_TOKEN_URI
    auth_provider_x509_cert_url: str = FIREBASE_AUTH_PROVIDER_CERT_URL
    client_x509_cert_url: str = FIREBASE_CLIENT_CERT_URL
    universe_domain: str = FIREBASE_UNIVERSE_DOMAIN


class PushFirebaseNotificator(AbstractNotificator):

    def __init__(self):
        self.firebase_config = asdict(FirebaseConfig())
        self.firebase_config["private_key"] = self.firebase_config["private_key"].replace('\\n', '\n')

        self.firebase_cred = credentials.Certificate(self.firebase_config)
        initialize_app(self.firebase_cred)

    def send_notification(self, recipient_id: str, recipient_data: dict) -> None:
        if "title" not in recipient_data or "body" not in recipient_data:
            raise PushNotificationEmptyDataMessage("Recipient data must have either title and body")

        registration_token = recipient_id

        # apns
        alert = messaging.ApsAlert(title=recipient_data["title"], body=recipient_data["body"])
        aps = messaging.Aps(alert=alert, sound="default")
        payload = messaging.APNSPayload(aps)

        # message
        msg = messaging.Message(
            notification=messaging.Notification(
                title=recipient_data["title"],
                body=recipient_data["body"]
            ),
            data={"key": "value"},
            token=registration_token,
            apns=messaging.APNSConfig(payload=payload)
        )

        # send
        res = messaging.send(msg)
        print(res)
