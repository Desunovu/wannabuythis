from dataclasses import dataclass

from src.shared_kernel.domain.events import DomainEvent


@dataclass
class WishlistCreated(DomainEvent):
    uuid: str
    name: str


@dataclass
class WishlistNameChanged(DomainEvent):
    uuid: str
    name: str


@dataclass
class WishlistItemAdded(DomainEvent):
    uuid: str
    name: str


@dataclass
class WishlistItemRemoved(DomainEvent):
    uuid: str
