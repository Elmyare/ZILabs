import unittest
import os
from EncryptLibrary import EncryptLibrary

class TestEncryptLibrary(unittest.TestCase):

    def setUp(self):
        """Создаем тестовый файл перед каждым тестом."""
        self.test_file = "test_input.txt"
        with open(self.test_file, "wb") as file:
            file.write(b"Hello, World! This is a test message.")

    def tearDown(self):
        """Удаляем тестовый файл после каждого теста."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_read_file(self):
        """Тест чтения файла."""
        data = EncryptLibrary.read_file(self.test_file)
        self.assertEqual(data, b"Hello, World! This is a test message.")

    def test_write_bytes_to_file(self):
        """Тест записи байтов в файл."""
        test_data = b"Test data"
        output_file = "test_output.bin"
        EncryptLibrary.write_bytes_to_file(output_file, test_data)
        with open(output_file, "rb") as file:
            self.assertEqual(file.read(), test_data)
        os.remove(output_file)

    def test_write_and_read_big_integers(self):
        """Тест записи и чтения массива BigInteger."""
        test_data = [123456789, 987654321, 555555555]
        output_file = "test_big_integers.bin"
        EncryptLibrary.write_big_integers_to_file(output_file, test_data)
        read_data = EncryptLibrary.read_big_integers_from_file(output_file)
        self.assertEqual(read_data, test_data)
        os.remove(output_file)

    def test_vernam_encode_decode(self):
        """Тест шифрования и дешифрования Вернама."""
        data = b"Hello, World!"
        encoded, key = EncryptLibrary.vernam_encode(data)
        decoded = EncryptLibrary.vernam_decode(encoded, key)
        self.assertEqual(decoded, data)

    def test_rsa_encode_decode(self):
        """Тест шифрования и дешифрования RSA."""
        data = b"Hello, RSA!"
        encoded, keys = EncryptLibrary.rsa_encode(data)
        decoded = EncryptLibrary.rsa_decode(encoded, keys)
        self.assertEqual(decoded, data)

    def test_elgamal_encode_decode(self):
        """Тест шифрования и дешифрования Эль-Гамаля."""
        data = b"Hello, ElGamal!"
        encoded, keys = EncryptLibrary.elgamal_encode(data)
        decoded = EncryptLibrary.elgamal_decode(encoded, keys)
        self.assertEqual(decoded, data)

    def test_shamir_encode_decode(self):
        """Тест шифрования и дешифрования Шамира."""
        data = b"Hello, Shamir!"
        encoded, keys = EncryptLibrary.shamir_encode(data)
        decoded = EncryptLibrary.shamir_decode(encoded, keys)
        self.assertEqual(decoded, data)

if __name__ == "__main__":
    unittest.main()