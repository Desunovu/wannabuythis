import datetime
from dataclasses import dataclass

from src.common.domain.commands import Command


@dataclass(frozen=True)
class CreateUser(Command):
    username: str
    email: str
    password: str


@dataclass(frozen=True)
class GenerateAuthToken(Command):
    username: str
    password: str
    token_lifetime: None | datetime.timedelta


@dataclass(frozen=True)
class ActivateUser(Command):
    username: str


@dataclass(frozen=True)
class ActivateUserWithToken(Command):
    token: str


@dataclass(frozen=True)
class ResendActivationLink(Command):
    username: str
    password: str


@dataclass(frozen=True)
class DeactivateUser(Command):
    username: str


@dataclass(frozen=True)
class ChangePassword(Command):
    username: str
    new_password: str
    old_password: str = ""
    called_by_admin: bool = False


@dataclass(frozen=True)
class ChangeEmail(Command):
    username: str
    new_email: str
