from dataclasses import dataclass

from src.shared_kernel.domain.commands import Command


@dataclass
class CreateUser(Command):
    username: str
    email: str
    password_hash: str


@dataclass
class ChangePassword(Command):
    username: str
    password: str
