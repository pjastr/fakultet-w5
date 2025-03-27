import unittest
from unittest.mock import patch, mock_open, MagicMock


class FileProcessor:
    def process_file(self, filename):
        try:
            with open(filename, 'r') as file:
                content = file.read()
                return self.analyze_content(content)
        except FileNotFoundError:
            return "Plik nie istnieje"

    def analyze_content(self, content):
        # Jakaś logika przetwarzania zawartości pliku
        return len(content.split())  # Przykładowo: zliczanie słów


class TestFileProcessor(unittest.TestCase):

    def test_process_existing_file(self):
        # Mockowanie funkcji open za pomocą mock_open
        sample_content = "To jest przykładowa zawartość pliku testowego."
        with patch('builtins.open', mock_open(read_data=sample_content)):
            processor = FileProcessor()

            # Mockowanie metody analyze_content
            processor.analyze_content = MagicMock(return_value=42)

            result = processor.process_file("test.txt")

            # Sprawdzenie, czy analyze_content zostało wywołane z odpowiednim argumentem
            processor.analyze_content.assert_called_once_with(sample_content)

            # Sprawdzenie wyniku
            self.assertEqual(result, 42)

    def test_process_nonexistent_file(self):
        # Mockowanie funkcji open tak, aby zgłaszała wyjątek FileNotFoundError
        with patch('builtins.open', side_effect=FileNotFoundError()):
            processor = FileProcessor()
            result = processor.process_file("nieistniejacy.txt")

            # Sprawdzenie, czy metoda zwróciła oczekiwany komunikat błędu
            self.assertEqual(result, "Plik nie istnieje")


if __name__ == '__main__':
    unittest.main()