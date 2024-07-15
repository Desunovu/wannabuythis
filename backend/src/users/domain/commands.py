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
class ActivateUserWithCode(Command):
    username: str
    code: str


@dataclass(frozen=True)
class ResendActivationCode(Command):
    username: str
    password: str


@dataclass(frozen=True)
class DeactivateUser(Command):
    username: str


@dataclass(frozen=True)
class ChangePasswordWithOldPassword(Command):
    username: str
    new_password: str
    old_password: str


@dataclass(frozen=True)
class ChangePasswordWithoutOldPassword(Command):
    username: str
    new_password: str


@dataclass(frozen=True)
class ChangeEmail(Command):
    username: str
    new_email: str
