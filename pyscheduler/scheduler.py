from pyscheduler.scheduler_exception import SchedulerException
from pyscheduler.task_type import TaskType
from pyscheduler.task import Task
from pyscheduler.thread.delayed_thread import DelayedThread
from pyscheduler.thread.repeating_delayed_thread import RepeatingDelayedThread
from pyscheduler.thread.repeating_thread import RepeatingThread
from time import time


class Scheduler:
    def __init__(self):
        self.task_id: int = 1

        self.repeating_tasks: dict[int, dict[str, any]] = {}
        self.delayed_tasks: dict[int, dict[str, any]] = {}
        self.repeating_delayed_tasks: dict[int, dict[str, any]] = {}

        self.repeating_thread: RepeatingThread = RepeatingThread(self)
        self.delayed_thread: DelayedThread = DelayedThread(self)
        self.repeating_delayed_thread: RepeatingDelayedThread = RepeatingDelayedThread(self)

    def schedule_repeating_task(self, task: Task, delay: int) -> None:
        task.set_id(self.task_id)
        task.set_type(TaskType.REPEATING)
        task.set_last_run(int(time()))

        self.repeating_tasks[self.task_id] = {
            'task': task,
            'delay': delay
        }
        self.__check_thread(TaskType.REPEATING)
        self.task_id += 1

    def schedule_delayed_task(self, task: Task, delay: int) -> None:
        task.set_id(self.task_id)
        task.set_type(TaskType.DELAYED)
        task.set_last_run(int(time()))

        self.delayed_tasks[self.task_id] = {
            'task': task,
            'delay': delay
        }
        self.__check_thread(TaskType.DELAYED)
        self.task_id += 1

    def schedule_repeating_delayed_task(self, task: Task, delay: int, repeat_delay: int) -> None:
        task.set_id(self.task_id)
        task.set_type(TaskType.REPEATING_DELAYED)
        task.set_last_run(int(time()))

        self.repeating_tasks[self.task_id] = {
            'task': task,
            'delay': delay,
            'repeat_delay': repeat_delay,
            'delay_ended': False
        }
        self.__check_thread(TaskType.REPEATING_DELAYED)
        self.task_id += 1

    def cancel_task(self, task: Task) -> None:
        match task.get_type():
            case TaskType.NOT_ASSIGNED:
                raise SchedulerException('Task is not scheduled')
            case TaskType.REPEATING:
                self.repeating_tasks.pop(task.get_id())
            case TaskType.DELAYED:
                self.delayed_tasks.pop(task.get_id())
            case TaskType.REPEATING_DELAYED:
                self.repeating_delayed_tasks.pop(task.get_id())

    def __check_thread(self, task_type: TaskType) -> None:
        match task_type:
            case TaskType.NOT_ASSIGNED:
                pass
            case TaskType.REPEATING:
                if self.repeating_tasks:
                    if not self.repeating_thread.is_running():
                        self.repeating_thread.start()
                else:
                    if self.delayed_thread.is_running():
                        self.repeating_thread.stop()
            case TaskType.DELAYED:
                if self.delayed_tasks:
                    if not self.delayed_thread.is_running():
                        self.delayed_thread.start()
                else:
                    if self.delayed_thread.is_running():
                        self.delayed_thread.stop()
            case TaskType.REPEATING_DELAYED:
                if self.repeating_delayed_tasks:
                    if not self.repeating_delayed_thread.is_running():
                        self.repeating_delayed_thread.start()
                else:
                    if self.repeating_delayed_thread.is_running():
                        self.repeating_delayed_thread.stop()
