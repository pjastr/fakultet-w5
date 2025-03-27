import csv


class FileProcessor:
    """Przykładowa klasa do obsługi plików, którą będziemy testować"""

    @staticmethod
    def read_text_file(file_path, encoding='utf-8'):
        """Czyta plik tekstowy i zwraca jego zawartość"""
        with open(file_path, 'r', encoding=encoding) as f:
            return f.read()


    @staticmethod
    def read_csv_file(file_path, delimiter=None, encoding='utf-8'):
        """Czyta plik CSV z wykrywaniem separatora (jeśli nie podano)"""
        if delimiter is None:
            # Próba wykrycia separatora
            with open(file_path, 'r', encoding=encoding) as f:
                sample = f.read(1024)
                sniffer = csv.Sniffer()
                delimiter = sniffer.sniff(sample).delimiter

        data = []
        with open(file_path, 'r', encoding=encoding) as f:
            reader = csv.reader(f, delimiter=delimiter)
            for row in reader:
                data.append(row)
        return data, delimiter