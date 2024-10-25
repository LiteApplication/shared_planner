from datetime import datetime, timedelta


def monday(date: datetime):
    """Return the Monday of the week that the given date is in."""
    return date - timedelta(days=date.weekday())


def monday_str(date: datetime):
    """Return the Monday of the week that the given date is in as a string."""
    return monday(date).strftime("%Y-%m-%d")
