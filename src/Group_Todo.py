from dataclasses import dataclass
from datetime import datetime, tzinfo


@dataclass  # (frozen=True)
class Group_Todo:
    """
    """

    title: str
    id: str

    def __init__(self, dict):
        self.title = dict.get("title")
        self.id = dict.get("id")


# Unit tests (Not implemented)
if __name__ == "__main__":
    pass
