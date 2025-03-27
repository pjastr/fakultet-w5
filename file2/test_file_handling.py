import unittest
import os
import csv
import tempfile

class TestFileHandling(unittest.TestCase):
    def setUp(self):
        # Utworzenie tymczasowego katalogu na pliki testowe
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_file = os.path.join(self.temp_dir.name, "test.txt")
        # Przykładowy plik tekstowy zapisany w utf-8
        with open(self.temp_file, "w", encoding="utf8") as f:
            f.write("Hello World!\n")

    def tearDown(self):
        # Usunięcie tymczasowego katalogu i wszystkich plików
        self.temp_dir.cleanup()

    def test_file_exists(self):
        # Test istnienia pliku
        self.assertTrue(os.path.exists(self.temp_file))

    def test_file_not_exists(self):
        # Test nieistnienia pliku
        non_existent_file = os.path.join(self.temp_dir.name, "nonexistent.txt")
        self.assertFalse(os.path.exists(non_existent_file))

    def test_non_ascii_characters(self):
        # Test zapisu i odczytu znaków spoza ASCII
        non_ascii_file = os.path.join(self.temp_dir.name, "nonascii.txt")
        content = "Hello, zażółć gęślą jaźń"
        with open(non_ascii_file, "w", encoding="utf8") as f:
            f.write(content)
        with open(non_ascii_file, "r", encoding="utf8") as f:
            data = f.read()
        self.assertEqual(data, content)

    def test_csv_separator_detection(self):
        # Test wykrycia separatora w pliku CSV
        csv_file = os.path.join(self.temp_dir.name, "test.csv")
        # Zapis CSV z separatorem ';'
        with open(csv_file, "w", newline="", encoding="utf8") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(["col1", "col2"])
            writer.writerow(["value1", "value2"])
        # Odczyt próbki i wykrycie separatora
        with open(csv_file, "r", newline="", encoding="utf8") as f:
            sample = f.read(1024)
            dialect = csv.Sniffer().sniff(sample)
            self.assertEqual(dialect.delimiter, ";")

    def test_empty_file(self):
        # Test obsługi pustego pliku
        empty_file = os.path.join(self.temp_dir.name, "empty.txt")
        with open(empty_file, "w", encoding="utf8") as f:
            pass
        with open(empty_file, "r", encoding="utf8") as f:
            data = f.read()
        self.assertEqual(data, "")

    # def test_permission_error(self):
    #     # Test próby odczytu pliku bez uprawnień
    #     perm_file = os.path.join(self.temp_dir.name, "perm.txt")
    #     with open(perm_file, "w", encoding="utf8") as f:
    #         f.write("content")
    #     # Usunięcie uprawnień do odczytu
    #     os.chmod(perm_file, 0o000)
    #     with self.assertRaises(PermissionError):
    #         with open(perm_file, "r", encoding="utf8") as f:
    #             f.read()
    #     # Przywrócenie uprawnień, aby możliwe było usunięcie pliku
    #     os.chmod(perm_file, 0o644)

if __name__ == '__main__':
    unittest.main()
