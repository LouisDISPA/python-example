from enum import Enum


class ActionType(Enum):
    CREDIT = 'credit'
    DEBIT = 'debit'


class Action:
    who: str
    action_type: ActionType
    amount: int

    def __init__(self, who: str, action_type: ActionType, amount: int):
        self.who = who
        self.action_type = action_type
        self.amount = amount
