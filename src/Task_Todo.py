from dataclasses import dataclass
from datetime import datetime, tzinfo
from typing import List
from List_Todo import List_Todo
from Task_TT import Task_TT


@dataclass  # (frozen=True)
class Task_Todo:
    """
    """

    title: str
    id: str
    list: List_Todo
    note: str
    steps: List

    completed: bool
    completedAt: dict
    createdAt: dict
    importance: int
    isReminderOn: bool
    reminderAt: dict
    dueAt: dict
    recurrence: dict

    task_TT: Task_TT = None

    def __init__(self, dict, lists):
        self.title = dict.get("title")
        self.id = dict.get("id")
        self.note = dict.get("note")
        self.steps = []

        self.completed = dict.get("completed")
        self.completedAt = dict.get("completed_at")
        self.createdAt = dict.get("created_at")
        self.importance = dict.get("importance")
        self.isReminderOn = dict.get("is_reminder_on")
        self.reminderAt = dict.get("reminder")
        self.dueAt = dict.get("due_date")
        self.recurrence = dict.get("recurrence")

        if dict.get("list_id"):
            for list in lists:
                if list.id == dict.get("list_id"):
                    self.list = list
                    break
            else:
                print("Task: %s - List not found" % (self.title))
                self.list = None
        else:
            self.list = None

    def add_step(self, step):
        self.steps.append(step)

    def convert_to_TT(self):
        """ PRELIMINARY
        """
        task_TT = Task_TT()
        task_TT.title = self.title
        task_TT.folderName = self.list.group.title if self.list.group else None
        task_TT.listName = self.list.title if self.list else None
        task_TT.tags = ""
        task_TT.content = self.note
        task_TT.isCheckList = False
        task_TT.startDate = None
        task_TT.dueDate = self.dueAt
        task_TT.reminder = self.reminderAt
        task_TT.repeat = self.recurrence
        task_TT.priority = self.importance
        task_TT.status = self.completed
        task_TT.createdTime = self.createdAt
        task_TT.completedTime = self.completedAt
        task_TT.order = 0
        task_TT.timezone = self.createdAt["time_zone"]
        task_TT.isAllDay = None
        task_TT.isFloating = False

        self.task_TT = task_TT


# Unit tests (Not implemented)
if __name__ == "__main__":
    pass
