import threading
import pyscheduler


class SchedulerThread(threading.Thread):
    def __init__(self, scheduler):
        super().__init__()
        self.scheduler: pyscheduler.scheduler.Scheduler = scheduler
        self.running = False

    def start(self) -> None:
        self.running = True
        super().start()

    def stop(self) -> None:
        self.running = False

    def is_running(self) -> bool:
        return self.running

    def run(self) -> None:
        if self.running:
            self.actual_run()

    def actual_run(self) -> None:
        pass
