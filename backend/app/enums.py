import enum


class MealplanState(str, enum.Enum):
    open = "open"
    bought = "bought"
    done = "done"
