from dataclasses import dataclass

from src.common.domain.commands import Command


@dataclass
class CreateRole(Command):
    name: str


@dataclass
class AddPermissionToRole(Command):
    role_name: str
    permission_name: str


@dataclass
class RemovePermissionFromRole(Command):
    role_name: str
    permission_name: str
