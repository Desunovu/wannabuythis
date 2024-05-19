from src.domain.user.events import PasswordChanged


def test_user_can_change_password(user):
    """Test that a user can change their password and that the PasswordChanged event is published"""
    user.change_password_hash("newpassword")

    assert user.password_hash == "newpassword"
    assert user.events[-1] == PasswordChanged(user.username)
