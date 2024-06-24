import abc
from smtplib import SMTP

from src import config
from src.users.domain.model import User


class Notificator(abc.ABC):
    @abc.abstractmethod
    def send_notification(
        self, recipient: "User", subject: str, message: str
    ) -> None: ...

    def send_activation_link(self, recipient: "User", activation_token: str):
        link = f"{config.get_base_url()}/activate/{activation_token}"
        self.send_notification(
            recipient=recipient,
            subject="WannaBuyThis Account activation",
            message=f"Activate your account by clicking on this link: {link}",
        )


class EmailNotificator(Notificator):
    def send_notification(self, recipient: "User", subject: str, message: str) -> None:
        with SMTP(config.get_smtp_host()) as smtp:
            smtp.sendmail(
                from_addr=config.get_smtp_sender(),
                to_addrs=[recipient.email],
                msg=f"Subject: {subject}\n\n{message}".encode(),
            )
