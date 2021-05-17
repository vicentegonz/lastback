from logging import getLogger

from exponent_server_sdk import (
    DeviceNotRegisteredError,
    PushClient,
    PushMessage,
    PushTicketError,
)

from backend.common.metaclasses import Singleton

logger = getLogger(__name__)


class Notificator(metaclass=Singleton):
    EXCEPTION_MESSAGE = "Unable to send push notification to {device}: {e}"

    def __init__(self):
        self.client = PushClient()

    def send(self, device, body, data=None):
        kwargs = {"device": device, "body": body, "data": data}
        self._send(**kwargs)

    def _send(self, device, body, data):
        try:
            response = self._publish_message(
                token=device.expo_push_token, body=body, data=data
            )
        except Exception as error:  # pylint: disable=W0703
            logger.error(self.EXCEPTION_MESSAGE.format(device=device, e=error))
        else:
            try:
                response.validate_response()
            except DeviceNotRegisteredError as error:
                logger.warning(self.EXCEPTION_MESSAGE.format(device=device, e=error))
                device.delete()
            except PushTicketError as error:
                logger.error(self.EXCEPTION_MESSAGE.format(device=device, e=error))

    def _publish_message(self, token, body, data):
        message = PushMessage(to=token, body=body, data=data)
        return self.client.publish(message)
