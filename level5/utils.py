class PriceRule:
    """
    The price rule is used to calculate the price of a rental.

    Attributes:
    - `after_day`: the number of days after which the rule is applied.
    - `reduction_percent`: the reduction percent applied to the price per day.
    """
    after_day: int
    reduction_percent: float

    def __init__(self, after_day: int, reduction_percent: float):
        self.after_day = after_day
        self.reduction_percent = reduction_percent


def calculate_days_price(day_count: int, price_per_day: int, price_rules: list[PriceRule] = []) -> int:
    """
    Calculate the price of a rental based on the number of days and the price per day.
    Take an optional list of price rules to apply reductions.

    Parameters:
    - `day_count`: the number of days.
    - `price_per_day`: the price per day.
    - `price_rules`: the list of price rules to apply.

    Example of rules:
    ```
    rules = [
        PriceRule(1, 0.2),
        PriceRule(3, 0.5),
    ]
    result = calculate_days_price(5, 100, rules)
    ```
    This will apply the first rule (20% reduction) after the first day, and the second rule (50% reduction) after 3 days. \\
    So the price will be `100 * 1day + 80 * 2days + 50 * 2days = 260`.
    """

    if len(price_rules) == 0:
        return day_count * price_per_day

    price: int = 0

    price_rules.sort(key=lambda x: -x.after_day)
    for rule in price_rules:
        if day_count > rule.after_day:
            days = day_count - rule.after_day
            amout = price_per_day * (1 - rule.reduction_percent)
            price += int(days * amout)
            day_count = rule.after_day

    if day_count > 0:
        price += int(day_count * price_per_day)

    return price
