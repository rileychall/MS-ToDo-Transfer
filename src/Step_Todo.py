from dataclasses import dataclass
from datetime import datetime, tzinfo
from Task_Todo import Task_Todo


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


# Unit tests (Not implemented)
if __name__ == "__main__":
    pass
