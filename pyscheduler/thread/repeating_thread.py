from pyscheduler.task import Task
from pyscheduler.thread.scheduler_thread import SchedulerThread
from time import time


class RepeatingThread(SchedulerThread):
    def actual_run(self) -> None:
        for task_id in self.scheduler.repeating_tasks:
            task_data: dict[str, any] = self.scheduler.repeating_tasks[task_id]
            task: Task = task_data['task']
            now: int = int(time())
            if (now - task.get_last_run()) >= task_data['delay']:
                task.run()
                task.set_last_run(now)
