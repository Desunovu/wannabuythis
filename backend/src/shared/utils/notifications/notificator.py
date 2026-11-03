import abc
import logging
from smtplib import SMTP

from src.config import Settings

logger = logging.getLogger(__name__)


class Notificator(abc.ABC):
    @abc.abstractmethod
    def send_notification(self, email: str, subject: str, message: str) -> None: ...

    def send_activation_code(self, email: str, code: str):
        self.send_notification(
            email=email,
            subject="WannaBuyThis Account activation",
            message=f"Activation code: {code}",
        )


class EmailNotificator(Notificator):
    def __init__(self, settings: Settings):
        self._smtp_host = settings.smtp_host
        self._smtp_port = settings.smtp_port
        self._smtp_sender = settings.smtp_sender
        self._smtp_username = settings.smtp_username
        self._smtp_password = settings.smtp_password
        self._smtp_use_tls = settings.smtp_use_tls

    def send_notification(self, email, subject, message):
        with SMTP(self._smtp_host, self._smtp_port) as smtp:
            if self._smtp_use_tls:
                smtp.starttls()
            if self._smtp_username:
                smtp.login(self._smtp_username, self._smtp_password or "")
            smtp.sendmail(
                from_addr=self._smtp_sender,
                to_addrs=[email],
                msg=f"Subject: {subject}\n\n{message}".encode(),
            )


class FakeEmailNotificator(Notificator):
    """Test/development double that logs emails instead of sending them."""

    def send_notification(self, email: str, subject: str, message: str) -> None:
        logger.info(
            "Fake email notificator: %s, %s, %s",
            email,
            subject,
            message,
        )
