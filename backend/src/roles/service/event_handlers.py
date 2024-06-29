from src.common.domain.events import DomainEvent
from src.roles.domain.events import (
    RoleCreated,
    PermissionAddedToRole,
    PermissionRemovedFromRole,
)

ROLE_EVENT_HANDLERS: dict[type[DomainEvent], list[callable]] = {
    RoleCreated: [],
    PermissionAddedToRole: [],
    PermissionRemovedFromRole: [],
}
