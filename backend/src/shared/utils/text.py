def canonicalize(value: str) -> str:
    """The single canonical form for usernames and emails."""
    return value.casefold()
