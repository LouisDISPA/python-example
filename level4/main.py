import json
from datetime import datetime
from action import Action, ActionType

DATE_FORMAT = '%Y-%m-%d'

with open('data/input.json') as f:
    data = json.load(f)

cars = data['cars']
rentals = data['rentals']


def calculate_days_price(day_count: int, price_per_day: int) -> int:
    price: int = 0

    if day_count >= 1:
        price += price_per_day
        day_count -= 1
    else:
        return price

    if day_count >= 3:
        price += int(3 * price_per_day * 0.9)
        day_count -= 3
    else:
        return price + int(day_count * price_per_day * 0.9)

    if day_count >= 6:
        price += int(6 * price_per_day * 0.7)
        day_count -= 6
    else:
        return price + int(day_count * price_per_day * 0.7)

    return price + int(day_count * price_per_day * 0.5)


def get_actions(rental) -> list[Action]:
    actions: list[Action] = [
        Action(
            'driver',
            ActionType.DEBIT,
            rental['price'],
        ),
        Action(
            'owner',
            ActionType.CREDIT,
            rental['price'] - rental['commission']['insurance_fee']
            - rental['commission']['assistance_fee']
            - rental['commission']['drivy_fee'],
        ),
        Action(
            'insurance',
            ActionType.CREDIT,
            rental['commission']['insurance_fee'],
        ),
        Action(
            'assistance',
            ActionType.CREDIT,
            rental['commission']['assistance_fee']),
        Action(
            'drivy',
            ActionType.CREDIT,
            rental['commission']['drivy_fee'],
        ),
    ]
    return actions


for rental in rentals:
    car_id = rental['car_id']
    car = next(c for c in cars if c['id'] == car_id)

    start_date = datetime.strptime(rental['start_date'], DATE_FORMAT)
    end_date = datetime.strptime(rental['end_date'], DATE_FORMAT)
    distance_km = rental['distance']
    price_per_day = car['price_per_day']
    price_per_km = car['price_per_km']

    day_count = (end_date - start_date).days + 1

    # calculate the full price
    price_days = calculate_days_price(day_count, price_per_day)
    price_distance = distance_km * price_per_km
    price = price_days + price_distance

    # calculate the commissions
    commission = price * 0.3
    insurance_fee = commission * 0.5
    assistance_fee = day_count * 100
    drivy_fee = commission - insurance_fee - assistance_fee

    rental['price'] = price
    rental['commission'] = {
        'insurance_fee': int(insurance_fee),
        'assistance_fee': int(assistance_fee),
        'drivy_fee': int(drivy_fee),
    }


# keep only the id, action for each rental
rentals = [{
    'id': rental['id'],
    'actions': [{
        'who': action.who,
        'type': action.action_type.value,
        'amount': action.amount,
    } for action in get_actions(rental)
    ],
} for rental in rentals]

with open('data/output.json', 'w') as f:
    json.dump({'rentals': rentals}, f, indent=2)
