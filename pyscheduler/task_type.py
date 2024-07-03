import enum


class TaskType(enum.Enum):
    NOT_ASSIGNED = 0
    REPEATING = 1
    DELAYED = 2
    REPEATING_DELAYED = 3
