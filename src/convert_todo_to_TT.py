import json
from Task_TT import Task_TT
from Group_Todo import Group_Todo
from List_Todo import List_Todo
from Task_Todo import Task_Todo
from Step_Todo import Step_Todo


def main():
    # Parsing requires items to be processed in this order
    # Have to sort dictionary according to this before iterating
    categoryOrder = ["listGroups", "lists", "tasks", "steps", "linkedEntities"]

    todoExportFile = "../todo_fulltest_2020-01-31.json"
    outputTTFile = "./debug_output_TT.csv"

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

    with open(outputTTFile, mode="w", encoding="utf8") as file:
        for row in tasks_output:
            file.write(row + "\n")


# Unit tests (Not implemented)
if __name__ == "__main__":
    main()
