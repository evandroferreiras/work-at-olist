import unittest
from app.business.price import PriceBus
from datetime import datetime


class PriceCalculationTestCase(unittest.TestCase):
    def test_if_calc_standard_time(self):
        price_bus = PriceBus()
        start_date = datetime(2018, 1, 1, 21, 57, 13)
        end_date = datetime(2018, 1, 1, 22, 17, 53)
        price = price_bus.calc_price(start_date, end_date)
        self.assertEqual(0.54, price)

    def test_if_calc_one_day_to_another(self):
        price_bus = PriceBus()
        start_date = datetime(2018, 1, 1, 21, 00, 00)
        end_date = datetime(2018, 1, 2, 21, 00, 00)
        price = price_bus.calc_price(start_date, end_date)
        self.assertEqual(86.76, price)

    def test_if_calc_reduced_time(self):
        price_bus = PriceBus()
        start_date = datetime(2018, 1, 1, 22, 00, 00)
        end_date = datetime(2018, 1, 2, 6, 00, 00)
        price = price_bus.calc_price(start_date, end_date)
        self.assertEqual(0.36, price)
