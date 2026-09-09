import logging

from src.modules.users.domain.events import UserCreated


class TestUserCreated:
    def test_email_confirmation_sent(self, caplog, mediator, uow, user):
        caplog.set_level(logging.INFO)
        uow.user_repository.add(user)
        mediator.handle(UserCreated(username=user.username, email=user.email))
        assert user.email in caplog.text
