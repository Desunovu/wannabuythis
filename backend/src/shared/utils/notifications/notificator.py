import abc
import logging
from smtplib import SMTP

from src.config import Settings
from src.modules.users.domain.model import User

logger = logging.getLogger(__name__)


class Notificator(abc.ABC):
    @abc.abstractmethod
    def send_notification(
        self, recipient: "User", subject: str, message: str
    ) -> None: ...

    def send_activation_code(self, recipient: "User", activation_code: str):
        self.send_notification(
            recipient=recipient,
            subject="WannaBuyThis Account activation",
            message=f"Activation code: {activation_code}",
        )


class EmailNotificator(Notificator):
    def __init__(self, settings: Settings):
        self._smtp_host = settings.smtp_host
        self._smtp_sender = settings.smtp_sender

    def send_notification(self, recipient, subject, message):
        with SMTP(self._smtp_host) as smtp:
            smtp.sendmail(
                from_addr=self._smtp_sender,
                to_addrs=[recipient.email],
                msg=f"Subject: {subject}\n\n{message}".encode(),
            )


class FakeNotificator(Notificator):
    def send_notification(self, recipient: "User", subject: str, message: str) -> None:
        logger.info(
            "Fake notificator: %s (%s), %s, %s",
            recipient.username,
            recipient.email,
            subject,
            message,
        )
