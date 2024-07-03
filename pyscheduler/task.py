from pyscheduler.task_type import TaskType


class Task:
    def __init__(self):
        self.task_id: int = 0
        self.task_type: TaskType = TaskType.NOT_ASSIGNED
        self.last_run: int = 0

    def run(self):
        pass

    def set_id(self, task_id: int):
        self.task_id = task_id

    def get_id(self):
        return self.task_id

    def set_type(self, task_type: TaskType):
        self.task_type = task_type

    def get_type(self):
        return self.task_type

    def set_last_run(self, last_run: int):
        self.last_run = last_run

    def get_last_run(self):
        return self.last_run
