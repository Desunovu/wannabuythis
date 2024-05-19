from dataclasses import dataclass

from src.domain.shared_kernel.commands import Command


@dataclass
class CreateUser(Command):
    username: str
    email: str
    password: str


@dataclass
class ChangePassword(Command):
    username: str
    new_password: str
    old_password: str = ""
    called_by_admin: bool = False
