import unittest
from utils import calculate_days_price, PriceRule


class TestUtils(unittest.TestCase):

    def test_calculate_days_price_no_rules(self):
        cases = [
            (1, 100, 100),
            (2, 100, 200),
            (10, 100, 1000),
            (4, 30, 120),
        ]
        for days, price_per_day, expected in cases:
            result = calculate_days_price(days, price_per_day)
            self.assertEqual(result, expected)

    def test_calculate_days_price_with_rules(self):
        rule1 = [PriceRule(1, 0.5)]
        rule2 = [PriceRule(3, 0.2), PriceRule(7, 0.5)]
        cases = [
            (1, 100, rule1, 100),
            (2, 100, rule1, 150),
            (3, 100, rule1, 200),
            (10, 100, rule1, 550),
            (2, 100, rule2, 200),
            (3, 100, rule2, 300),
            (4, 100, rule2, 3 * 100 + 1 * 80),
            (7, 100, rule2, 3 * 100 + 4 * 80),
            (10, 100, rule2, 3 * 100 + 4 * 80 + 3 * 50),
        ]
        for days, price_per_day, rules, expected in cases:
            result = calculate_days_price(days, price_per_day, rules)
            self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
