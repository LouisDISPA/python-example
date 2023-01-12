import json
from datetime import datetime

DATE_FORMAT = '%Y-%m-%d'

with open('data/input.json') as f:
    data = json.load(f)

cars = data['cars']
rentals = data['rentals']

for rental in rentals:
    car_id = rental['car_id']
    car = next(c for c in cars if c['id'] == car_id)

    start_date = datetime.strptime(rental['start_date'], DATE_FORMAT)
    end_date = datetime.strptime(rental['end_date'], DATE_FORMAT)
    distance_km = rental['distance']
    price_per_day = car['price_per_day']
    price_per_km = car['price_per_km']

    day_count = (end_date - start_date).days + 1

    rental['price'] = day_count * price_per_day + distance_km * price_per_km

# keep only the id and price for each rental
rentals = [{'id': r['id'], 'price': r['price']} for r in rentals]

with open('data/output.json', 'w') as f:
    json.dump({'rentals': rentals}, f, indent=2)
