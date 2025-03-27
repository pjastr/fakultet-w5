import unittest
import os
import csv
import tempfile
import codecs
import chardet
from file_processor import FileProcessor


class TestFileOperations(unittest.TestCase):

    def setUp(self):
        """Przygotowanie przed każdym testem"""
        # Utwórz tymczasowe pliki do testów
        self.temp_dir = tempfile.TemporaryDirectory()

        # Plik UTF-8
        self.utf8_file = os.path.join(self.temp_dir.name, 'utf8_file.txt')
        with open(self.utf8_file, 'w', encoding='utf-8') as f:
            f.write("Witaj świecie! ŁĄŚ")

        # Plik CSV z przecinkiem jako separatorem
        self.csv_comma_file = os.path.join(self.temp_dir.name, 'comma.csv')
        with open(self.csv_comma_file, 'w', encoding='utf-8') as f:
            f.write("imię,nazwisko,wiek\nJan,Kowalski,30\nAnna,Nowak,25")

        # Plik CSV z średnikiem jako separatorem
        self.csv_semicolon_file = os.path.join(self.temp_dir.name, 'semicolon.csv')
        with open(self.csv_semicolon_file, 'w', encoding='utf-8') as f:
            f.write("imię;nazwisko;wiek\nJan;Kowalski;30\nAnna;Nowak;25")

        # Plik CSV ze znakami spoza ASCII
        self.csv_non_ascii_file = os.path.join(self.temp_dir.name, 'non_ascii.csv')
        with open(self.csv_non_ascii_file, 'w', encoding='utf-8') as f:
            f.write("imię,nazwisko,miasto\nŁukasz,Żółć,Kraków\nŚwiętosław,Węgierski,Łódź")

    def tearDown(self):
        """Czyszczenie po każdym teście"""
        self.temp_dir.cleanup()

    # 1) Testy na istnienie/nieistnienie pliku
    def test_file_exists(self):
        """Test czy plik istnieje"""
        self.assertTrue(os.path.exists(self.utf8_file))

    def test_file_not_exists(self):
        """Test czy plik nie istnieje"""
        non_existent_file = os.path.join(self.temp_dir.name, 'nieistniejacy.txt')
        self.assertFalse(os.path.exists(non_existent_file))

    def test_file_not_exists_exception(self):
        """Test czy wywołanie wyjątku gdy plik nie istnieje"""
        non_existent_file = os.path.join(self.temp_dir.name, 'nieistniejacy.txt')
        with self.assertRaises(FileNotFoundError):
            FileProcessor.read_text_file(non_existent_file)


    # 3) Testy na znaki poza ASCII
    def test_non_ascii_characters(self):
        """Test czy znaki poza ASCII są poprawnie obsługiwane"""
        content = FileProcessor.read_text_file(self.utf8_file)
        self.assertIn("ś", content)
        self.assertIn("Ł", content)

    def test_non_ascii_in_csv(self):
        """Test czy znaki poza ASCII są poprawnie obsługiwane w CSV"""
        data, _ = FileProcessor.read_csv_file(self.csv_non_ascii_file)
        self.assertEqual(data[1][0], "Łukasz")
        self.assertEqual(data[1][1], "Żółć")

    # 4) Testy na wykrycie separatora w CSV
    def test_detect_comma_separator(self):
        """Test wykrywania przecinka jako separatora"""
        _, delimiter = FileProcessor.read_csv_file(self.csv_comma_file)
        self.assertEqual(delimiter, ',')

    def test_detect_semicolon_separator(self):
        """Test wykrywania średnika jako separatora"""
        _, delimiter = FileProcessor.read_csv_file(self.csv_semicolon_file)
        self.assertEqual(delimiter, ';')

    def test_csv_with_explicit_delimiter(self):
        """Test czy podanie separatora działa poprawnie"""
        data, _ = FileProcessor.read_csv_file(self.csv_semicolon_file, delimiter=';')
        self.assertEqual(data[0], ["imię", "nazwisko", "wiek"])
        self.assertEqual(data[1], ["Jan", "Kowalski", "30"])

    # 5) Inne typowe sytuacje testowe
    def test_empty_file(self):
        """Test obsługi pustego pliku"""
        empty_file = os.path.join(self.temp_dir.name, 'empty.txt')
        with open(empty_file, 'w') as f:
            pass  # Tworzenie pustego pliku

        content = FileProcessor.read_text_file(empty_file)
        self.assertEqual(content, "")

    def test_large_file_simulation(self):
        """Test symulacji dużego pliku (mockowanie)"""
        large_file = os.path.join(self.temp_dir.name, 'large.txt')
        with open(large_file, 'w') as f:
            f.write("x" * 10000)  # Symulacja dużego pliku

        content = FileProcessor.read_text_file(large_file)
        self.assertEqual(len(content), 10000)

    def test_file_permissions(self):
        """Test praw dostępu do pliku"""
        # Uwaga: Ten test działa tylko na systemach Unix/Linux
        if os.name != 'nt':  # Jeśli nie Windows
            no_read_file = os.path.join(self.temp_dir.name, 'no_read.txt')
            with open(no_read_file, 'w') as f:
                f.write("Zawartość")

            # Zmiana praw dostępu - brak prawa odczytu
            os.chmod(no_read_file, 0o000)

            with self.assertRaises(PermissionError):
                FileProcessor.read_text_file(no_read_file)

            # Przywrócenie praw dostępu do czyszczenia
            os.chmod(no_read_file, 0o644)


if __name__ == '__main__':
    unittest.main()