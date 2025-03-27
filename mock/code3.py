import unittest
from unittest.mock import patch, Mock


class Database:
    def connect(self):
        # W rzeczywistości nawiązywałoby połączenie z bazą danych
        pass

    def query(self, sql):
        # W rzeczywistości wykonywałoby zapytanie SQL
        pass

    def close(self):
        # W rzeczywistości zamykałoby połączenie
        pass


class UserRepository:
    def __init__(self, database):
        self.db = database

    def get_user_by_id(self, user_id):
        self.db.connect()
        result = self.db.query(f"SELECT * FROM users WHERE id = {user_id}")
        self.db.close()
        return result


class TestUserRepository(unittest.TestCase):

    def test_get_user_by_id(self):
        # Tworzenie mocka dla klasy Database
        mock_db = Mock()

        # Konfiguracja zachowania metod mocka
        mock_db.query.return_value = {'id': 1, 'name': 'Jan Kowalski'}

        # Utworzenie testowanego obiektu z zamockowaną zależnością
        repo = UserRepository(mock_db)

        # Wywołanie testowanej metody
        result = repo.get_user_by_id(1)

        # Sprawdzenie, czy metody mocka zostały wywołane w odpowiedniej kolejności
        mock_db.connect.assert_called_once()
        mock_db.query.assert_called_once_with("SELECT * FROM users WHERE id = 1")
        mock_db.close.assert_called_once()

        # Sprawdzenie wyniku
        self.assertEqual(result, {'id': 1, 'name': 'Jan Kowalski'})


if __name__ == '__main__':
    unittest.main()