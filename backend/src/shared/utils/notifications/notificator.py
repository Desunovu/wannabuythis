import abc
import logging
from email.message import EmailMessage
from email.policy import SMTP as SMTP_POLICY
from email.utils import formatdate, make_msgid
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

    def send_email_change_code(self, email: str, code: str):
        self.send_notification(
            email=email,
            subject="WannaBuyThis Email change",
            message=f"Confirmation code: {code}",
        )


class EmailNotificator(Notificator):
    def __init__(self, settings: Settings):
        self._smtp_host = settings.smtp_host
        self._smtp_port = settings.smtp_port
        self._smtp_timeout = settings.smtp_timeout
        self._smtp_sender = settings.smtp_sender
        self._smtp_username = settings.smtp_username
        self._smtp_password = settings.smtp_password
        self._smtp_use_tls = settings.smtp_use_tls
        # 7bit payload, no 8BITMIME support needed.
        self._policy = SMTP_POLICY.clone(cte_type="7bit")

    def send_notification(self, email: str, subject: str, message: str) -> None:
        msg = EmailMessage(policy=self._policy)
        msg["Subject"] = subject
        msg["From"] = self._smtp_sender
        msg["To"] = email
        msg["Date"] = formatdate(localtime=True)
        msg["Message-ID"] = make_msgid()
        msg.set_content(message, charset="utf-8")

        with SMTP(self._smtp_host, self._smtp_port, timeout=self._smtp_timeout) as smtp:
            if self._smtp_use_tls:
                smtp.starttls()
            if self._smtp_username:
                smtp.login(self._smtp_username, self._smtp_password or "")
            smtp.send_message(msg)


class FakeEmailNotificator(Notificator):
    """Test/development double that logs emails instead of sending them."""

    def send_notification(self, email: str, subject: str, message: str) -> None:
        logger.info(
            "Fake email notificator: %s, %s, %s",
            email,
            subject,
            message,
        )
