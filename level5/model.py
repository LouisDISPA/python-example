from enum import Enum
from datetime import datetime


# --- Input model classes ---

class Car:
    id: int
    price_per_day: int
    price_per_km: int

    def __init__(self, id: int, price_per_day: int, price_per_km: int):
        self.id = id
        self.price_per_day = price_per_day
        self.price_per_km = price_per_km


class Rental:
    id: int
    car_id: int
    start_date: datetime
    end_date: datetime
    distance: int
    day_count: int

    def __init__(self, id: int, car_id: int, start_date: str, end_date: str, distance: int):
        self.id = id
        self.car_id = car_id
        self.start_date = datetime.strptime(start_date, '%Y-%m-%d')
        self.end_date = datetime.strptime(end_date, '%Y-%m-%d')
        self.distance = distance
        self.day_count = (self.end_date - self.start_date).days + 1


class OptionType(Enum):
    GPS = 'gps'
    BABY_SEAT = 'baby_seat'
    ADDITIONAL_INSURANCE = 'additional_insurance'

    def price_per_day(self) -> int:
        """Return the price per day for this option type."""
        match self:
            case OptionType.GPS:
                return 500
            case OptionType.BABY_SEAT:
                return 200
            case OptionType.ADDITIONAL_INSURANCE:
                return 1000

    def credited_to(self) -> str:
        """
        Return the actor who is credited for this option type.

        Possible actors are 'owner', 'insurance', 'assistance' and 'drivy'.
        """
        match self:
            case OptionType.GPS:
                return 'owner'
            case OptionType.BABY_SEAT:
                return 'owner'
            case OptionType.ADDITIONAL_INSURANCE:
                return 'drivy'

    def toJSON(self):
        return self.value


class Option:
    id: int
    rental_id: int
    type: OptionType

    def __init__(self, id: int, rental_id: int, type: str):
        self.id = id
        self.rental_id = rental_id
        self.type = OptionType(type)


# --- Output model classes ---

class ActionType(Enum):
    CREDIT = 'credit'
    DEBIT = 'debit'

    def toJSON(self):
        return self.value


class Action:
    who: str
    type: ActionType
    amount: int

    def __init__(self, who: str, type: ActionType, amount: int):
        self.who = who
        self.type = type
        self.amount = amount

    def toJSON(self):
        return self.__dict__


class RentalView:
    id: int
    options: list[OptionType]
    actions: list[Action]

    def __init__(self, id: int, options: list[OptionType], actions: list[Action]):
        self.id = id
        self.options = options
        self.actions = actions

    def toJSON(self):
        return self.__dict__


class ResultView:
    rentals: list[RentalView]

    def __init__(self, rentals: list[RentalView]):
        self.rentals = rentals

    def toJSON(self):
        return self.__dict__
