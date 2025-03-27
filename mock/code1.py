import unittest
from unittest.mock import Mock, patch


# Funkcja, którą będziemy testować
def process_data(data_service):
    result = data_service.get_data()
    if result:
        return result.upper()
    return None


# Test z użyciem mocka
class TestProcessData(unittest.TestCase):
    def test_process_data_success(self):
        # Tworzenie mocka
        mock_service = Mock()
        # Konfiguracja zachowania mocka
        mock_service.get_data.return_value = "test data"

        # Wywołanie testowanej funkcji z mockiem
        result = process_data(mock_service)

        # Asercje
        self.assertEqual(result, "TEST DATA")
        # Sprawdzenie czy metoda get_data została wywołana
        mock_service.get_data.assert_called_once()

    def test_process_data_no_result(self):
        mock_service = Mock()
        mock_service.get_data.return_value = None

        result = process_data(mock_service)

        self.assertIsNone(result)
        mock_service.get_data.assert_called_once()


if __name__ == "__main__":
    unittest.main()