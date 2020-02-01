from dataclasses import dataclass
from datetime import datetime, tzinfo


@dataclass
class Task_TT:
    """
    """

    folderName: str = ""
    listName: str = ""
    title: str = ""
    tags: str = ""
    content: str = ""
    isCheckList: bool = False
    startDate: datetime = None
    dueDate: datetime = None
    reminder: str = ""
    repeat: str = ""
    priority: int = 0
    status: int = 0
    createdTime: datetime = datetime.min
    completedTime: datetime = None
    order: int = 0
    timezone: tzinfo = None  # FIX
    isAllDay: bool = None
    isFloating: bool = False

    def create_TT_csv_row(self):
        strList = [
            str(val) for _, val in vars(self).items()
        ]  # Initial string conversion
        strList = ["N" if x == "False" else x for x in strList]  # Replace False
        strList = ["Y" if x == "True" else x for x in strList]  # Replace True
        strList = ["" if x == "None" else x for x in strList]  # Replace None
        csv_row = ",".join(
            '"{0}"'.format(x) for x in strList
        )  # Concatenate wrapped in quotes
        return csv_row


# Unit tests (Not implemented)
if __name__ == "__main__":
    pass
