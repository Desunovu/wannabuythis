import logging

from src.modules.users.domain.events import UserCreated


class TestUserCreated:
    def test_email_confirmation_sent(self, caplog, messagebus, uow, user):
        caplog.set_level(logging.INFO)
        uow.user_repository.add(user)
        messagebus.handle(UserCreated(username=user.username, email=user.email))
        assert user.email in caplog.text
