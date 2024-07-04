from dataclasses import dataclass, field
from datetime import datetime, UTC


@dataclass(frozen=True)
class CommandMetadata:
    username: str | None = None
    is_superuser: bool = False
    timestamp: datetime = datetime.now(UTC)


@dataclass(frozen=True, kw_only=True)
class Command:
    metadata: CommandMetadata = CommandMetadata()
