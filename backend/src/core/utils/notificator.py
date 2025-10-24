import abc
from smtplib import SMTP

from src import config
from src.users.domain.model import User


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
    def send_notification(self, recipient: "User", subject: str, message: str) -> None:
        with SMTP(config.get_smtp_host()) as smtp:
            smtp.sendmail(
                from_addr=config.get_smtp_sender(),
                to_addrs=[recipient.email],
                msg=f"Subject: {subject}\n\n{message}".encode(),
            )
