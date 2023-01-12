import json
from utils import calculate_days_price, PriceRule
from model import Action, ActionType, Car, Rental, Option, OptionType, RentalView, ResultView

# --- Constants ---

DATE_FORMAT = '%Y-%m-%d'
RENT_PRICE_RULES = [
    PriceRule(1, 0.1),
    PriceRule(4, 0.3),
    PriceRule(10, 0.5),
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

    # add the options
    for option_type in rental_options:
        price_option = rental.day_count * option_type.price_per_day()
        price += price_option

        match option_type.credited_to():
            case 'insurance': insurance_fee += price_option
            case 'assistance': assistance_fee += price_option
            case 'drivy': drivy_fee += price_option
            case 'owner': owner_fee += price_option

    # build the view
    options_list = list(rental_options)
    actions = [
        Action('driver', ActionType.DEBIT, price),
        Action('owner', ActionType.CREDIT, owner_fee),
        Action('insurance', ActionType.CREDIT, insurance_fee),
        Action('assistance', ActionType.CREDIT, assistance_fee),
        Action('drivy', ActionType.CREDIT, drivy_fee),
    ]
    rentals_view.append(RentalView(rental.id, options_list, actions))

result_view = ResultView(rentals_view)

# --- Write the view to 'output.json' file ---

with open('data/output.json', 'w') as f:
    json.dump(result_view, f, indent=2, default=lambda o: o.toJSON())
