from src.users.domain.events import UserCreated


class TestUserCreated:
    def test_email_confirmation_sent(self, capsys, messagebus, user):
        messagebus.handle(UserCreated(username=user.username, email=user.email))
        # Test what fakenotificator print message to stdout
        captured = capsys.readouterr()
        assert user.username in captured.out
