import json
from utils import calculate_days_price, PriceRule
from model import Action, ActionType, Car, Rental, Option, OptionType, RentalView, ResultView

# --- Constants ---

RENT_PRICE_RULES = [
    PriceRule(after_day=1,  reduction_percent=0.1),
    PriceRule(after_day=4,  reduction_percent=0.3),
    PriceRule(after_day=10, reduction_percent=0.5),
]

# --- Load the data from 'input.json' ---

with open('data/input.json') as f:
    data = json.load(f)

cars: list[Car] = [Car(**car) for car in data['cars']]
rentals: list[Rental] = [Rental(**rental) for rental in data['rentals']]
options: list[Option] = [Option(**option) for option in data['options']]


# --- Build the view for every rental ---

rentals_view: list[RentalView] = []

for rental in rentals:

    # load the car and options
    car = next(c for c in cars if c.id == rental.car_id)
    rental_options = {
        option.type for option in options
        if option.rental_id == rental.id
    }

    # calculate the price
    price_days = calculate_days_price(
        rental.day_count,
        car.price_per_day,
        RENT_PRICE_RULES
    )
    price_distance = rental.distance * car.price_per_km
    price = price_days + price_distance

    # calculate the commissions
    commission = int(price * 0.3)
    insurance_fee = int(commission * 0.5)
    assistance_fee = int(rental.day_count * 100)
    drivy_fee = commission - insurance_fee - assistance_fee
    owner_fee = price - commission

    fees = {
        'owner': owner_fee,
        'insurance': insurance_fee,
        'assistance': assistance_fee,
        'drivy': drivy_fee,
    }

    # add the options
    for option_type in rental_options:
        price_option = rental.day_count * option_type.price_per_day()
        credited_to = option_type.credited_to()

        if fees.get(credited_to) is None:
            raise RuntimeError(
                f'Unknown creditor "{credited_to}" with option type "{option_type.value}"')

        fees[credited_to] += price_option

    # build the view
    options_list = list(rental_options)
    actions = [Action('driver', ActionType.DEBIT, sum(fees.values()))]
    actions.extend(
        Action(credited_to, ActionType.CREDIT, fee)
        for credited_to, fee in fees.items()
    )

    rentals_view.append(RentalView(rental.id, options_list, actions))

result_view = ResultView(rentals_view)

# --- Write the view to 'output.json' file ---

with open('data/output.json', 'w') as f:
    json.dump(result_view, f, indent=2, default=lambda o: o.toJSON())
