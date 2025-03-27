import unittest
from unittest.mock import patch, MagicMock


# Klasa do przetestowania
class PaymentGateway:
    def process_payment(self, amount, card_number):
        # W rzeczywistości wysyłałaby żądanie do zewnętrznego API
        response = self.send_payment_request(amount, card_number)

        if response.get('status') == 'success':
            return True
        else:
            return False

    def send_payment_request(self, amount, card_number):
        # Ta metoda zostanie zamockowana
        pass


class TestPaymentGateway(unittest.TestCase):

    def setUp(self):
        self.gateway = PaymentGateway()
        self.valid_card = '4111111111111111'
        self.invalid_card = '1234567890123456'

    @patch.object(PaymentGateway, 'send_payment_request')
    def test_successful_payment(self, mock_send_request):
        # Konfiguracja mocka, aby zwracał sukces dla prawidłowej karty
        mock_send_request.return_value = {'status': 'success', 'transaction_id': 'TX123456'}

        # Wywołanie testowanej metody
        result = self.gateway.process_payment(100.00, self.valid_card)

        # Sprawdzenie, czy mock został wywołany z odpowiednimi argumentami
        mock_send_request.assert_called_once_with(100.00, self.valid_card)

        # Sprawdzenie wyniku
        self.assertTrue(result)

    @patch.object(PaymentGateway, 'send_payment_request')
    def test_failed_payment(self, mock_send_request):
        # Konfiguracja mocka, aby zwracał błąd dla nieprawidłowej karty
        mock_send_request.return_value = {'status': 'error', 'message': 'Invalid card number'}

        # Wywołanie testowanej metody
        result = self.gateway.process_payment(100.00, self.invalid_card)

        # Sprawdzenie, czy mock został wywołany z odpowiednimi argumentami
        mock_send_request.assert_called_once_with(100.00, self.invalid_card)

        # Sprawdzenie wyniku
        self.assertFalse(result)

    @patch.object(PaymentGateway, 'send_payment_request')
    def test_dynamic_response_based_on_input(self, mock_send_request):
        # Użycie side_effect do dynamicznego określenia odpowiedzi na podstawie wejścia
        def mock_response(amount, card_number):
            if card_number == self.valid_card and amount <= 1000:
                return {'status': 'success', 'transaction_id': 'TX123456'}
            elif amount > 1000:
                return {'status': 'error', 'message': 'Amount exceeds limit'}
            else:
                return {'status': 'error', 'message': 'Invalid card number'}

        mock_send_request.side_effect = mock_response

        # Test dla prawidłowej karty i kwoty w limicie
        result1 = self.gateway.process_payment(500.00, self.valid_card)
        self.assertTrue(result1)

        # Test dla prawidłowej karty, ale kwoty powyżej limitu
        result2 = self.gateway.process_payment(1500.00, self.valid_card)
        self.assertFalse(result2)

        # Test dla nieprawidłowej karty
        result3 = self.gateway.process_payment(100.00, self.invalid_card)
        self.assertFalse(result3)

        # Sprawdzenie liczby wywołań mocka
        self.assertEqual(mock_send_request.call_count, 3)


if __name__ == '__main__':
    unittest.main()