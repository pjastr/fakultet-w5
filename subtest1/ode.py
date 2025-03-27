import unittest


def calculate_discount(amount, discount_percent):
    if not (0 <= discount_percent <= 100):
        raise ValueError("Discount percent must be between 0 and 100")

    return amount - (amount * discount_percent / 100)


class TestDiscountCalculation(unittest.TestCase):
    def test_valid_discounts(self):
        test_cases = [
            # (kwota, procent_zniżki, oczekiwany_wynik)
            (100, 10, 90),
            (200, 25, 150),
            (50, 0, 50),
            (75, 100, 0)
        ]

        for amount, discount, expected in test_cases:
            with self.subTest(amount=amount, discount=discount):
                result = calculate_discount(amount, discount)
                self.assertEqual(result, expected)

    def test_invalid_discounts(self):
        invalid_cases = [
            # (kwota, nieprawidłowy_procent_zniżki)
            (100, -10),
            (100, 110)
        ]

        for amount, discount in invalid_cases:
            with self.subTest(amount=amount, discount=discount):
                with self.assertRaises(ValueError):
                    calculate_discount(amount, discount)


if __name__ == '__main__':
    unittest.main()