from dataclasses import dataclass

from src.common.domain.commands import Command


@dataclass(frozen=True)
class CreateRole(Command):
    name: str


@dataclass(frozen=True)
class AddPermissionToRole(Command):
    role_name: str
    permission_name: str


@dataclass(frozen=True)
class RemovePermissionFromRole(Command):
    role_name: str
    permission_name: str
