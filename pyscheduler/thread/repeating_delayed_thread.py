from pyscheduler.task import Task
from pyscheduler.thread.scheduler_thread import SchedulerThread
from time import time


class RepeatingDelayedThread(SchedulerThread):
    def actual_run(self) -> None:
        for task_id in self.scheduler.repeating_delayed_tasks:
            task_data: dict[str, any] = self.scheduler.repeating_delayed_tasks[task_id]
            task: Task = task_data['task']
            now: int = int(time())

            if not task_data['delay_ended']:
                if (now - task.get_last_run()) >= task_data['delay']:
                    self.scheduler.repeating_delayed_tasks[task_id]['delay_ended'] = True
                    task.run()
                    task.set_last_run(now)
                return

            if (now - task.get_last_run()) >= task_data['repeat_delay']:
                task.run()
                task.set_last_run(now)
