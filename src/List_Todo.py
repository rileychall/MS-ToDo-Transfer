from dataclasses import dataclass
from datetime import datetime, tzinfo
from Group_Todo import Group_Todo


@dataclass  # (frozen=True)
class List_Todo:
    """
    """

    title: str
    id: str
    group: Group_Todo

    def __init__(self, dict, groups):
        self.title = dict.get("title")
        self.id = dict.get("id")
        if dict.get("parent_group_id"):
            for group in groups:
                if group.id == dict.get("parent_group_id"):
                    self.group = group
                    break
            else:
                print("List: %s - Group not found" % (self.title))
                self.group = None
        else:
            self.group = None


# Unit tests (Not implemented)
if __name__ == "__main__":
    pass
