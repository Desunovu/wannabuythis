def canonicalize(value: str) -> str:
    """The single canonical form for emails, applied by every write path."""
    return value.strip().casefold()
