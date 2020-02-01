from dataclasses import dataclass
from datetime import datetime, tzinfo
from typing import List


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


@dataclass  # (frozen=True)
class Group_Todo:
    """
    """

    title: str
    id: str

    def __init__(self, dict):
        self.title = dict.get("title")
        self.id = dict.get("id")


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


# TODO: Subtasks/Steps
# If task has steps and no note, make isCheckList True, otherwise format steps
# as checklist in richtext description
@dataclass
class Step_Todo:
    """
    """

    title: str
    id: str
    task: Task_Todo

    completed: bool
    createdAt: dict

    def __init__(self, dict, tasks):
        self.title = dict.get("title")
        self.id = dict.get("id")
        self.completed = dict.get("completed")
        self.createdAt = dict.get("created_at")
        if dict.get("task_id"):
            for task in tasks:
                if task.id == dict.get("task_id"):
                    self.task = task
                    task.add_step(self)
                    break
            else:
                print("Step: %s - Task not found" % (self.title))
                self.task = None
        else:
            self.task = None


if __name__ == "__main__":
    import json

    todoExportFile = "todo_fulltest_2020-01-31.json"

    # Parsing requires items to be processed in this order
    # Have to sort dictionary according to this before iterating
    categoryOrder = ["listGroups", "lists", "tasks", "steps", "linkedEntities"]

    with open(todoExportFile, encoding="utf8") as file:
        datafile = json.load(file)
        print(type(datafile), type(datafile.items()))
        # .items returns tuples, the first of each is sorted against categoryOrder
        for category, dataset in sorted(
            datafile.items(), key=lambda x: categoryOrder.index(x[0])
        ):
            print(category, type(category))
            if category == "listGroups":
                groups = [Group_Todo(entry) for entry in dataset]
            elif category == "lists":
                lists = [List_Todo(entry, groups) for entry in dataset]
            elif category == "tasks":
                tasks = [Task_Todo(entry, lists) for entry in dataset]
            elif category == "steps":
                steps = [Step_Todo(entry, tasks) for entry in dataset]
            elif category == "linkedEntities":
                pass  # Not implemented (and not used by TT)
            else:
                print("Bad/extra category")

    tasks_output = []
    for task in tasks:
        task.convert_to_TT()
        tasks_output.append(task.task_TT.create_TT_csv_row())

    with open("output_test.csv", mode="w", encoding="utf8") as file:
        for row in tasks_output:
            file.write(row + "\n")
