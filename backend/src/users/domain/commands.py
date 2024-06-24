from dataclasses import dataclass

from src.common.domain.commands import Command


@dataclass
class CreateUser(Command):
    username: str
    email: str
    password: str


@dataclass
class ActivateUser(Command):
    username: str


@dataclass
class ResendActivationLink(Command):
    username: str
    password: str


@dataclass
class DeactivateUser(Command):
    username: str


@dataclass
class ChangePassword(Command):
    username: str
    new_password: str
    old_password: str = ""
    called_by_admin: bool = False


@dataclass
class ChangeUserEmail(Command):
    username: str
    new_email: str


@dataclass
class AddRoleToUser(Command):
    username: str
    role_name: str


@dataclass
class RemoveRoleFromUser(Command):
    username: str
    role_name: str
