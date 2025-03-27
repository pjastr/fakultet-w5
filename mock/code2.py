import unittest
from unittest.mock import patch


# Funkcja, którą będziemy testować
def get_user_data(user_id):
    # W rzeczywistości ta funkcja mogłaby komunikować się z bazą danych
    # lub API, ale my ją zamockujemy
    return fetch_data_from_api(user_id)


def fetch_data_from_api(user_id):
    # Ta funkcja w rzeczywistości mogłaby wykonywać zapytanie HTTP
    # My ją zamockujemy, więc jej implementacja nie ma znaczenia
    pass


class TestUserData(unittest.TestCase):

    @patch('code2.fetch_data_from_api')
    def test_get_user_data(self, mock_fetch):
        # Konfiguracja mocka
        mock_fetch.return_value = {'id': 1, 'name': 'Jan Kowalski', 'email': 'jan@example.com'}

        # Wywołanie funkcji, która korzysta z zamockowanej funkcji
        result = get_user_data(1)

        # Sprawdzenie, czy mock został wywołany z odpowiednim argumentem
        mock_fetch.assert_called_once_with(1)

        # Sprawdzenie, czy wynik jest zgodny z oczekiwaniami
        self.assertEqual(result, {'id': 1, 'name': 'Jan Kowalski', 'email': 'jan@example.com'})


if __name__ == '__main__':
    unittest.main()