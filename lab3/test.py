import unittest
from DigitalSignatureLibrary import DigitalSignatureLibrary

class TestDigitalSignatureLibrary(unittest.TestCase):
    def setUp(self):
        """Инициализация объекта DigitalSignatureLibrary перед каждым тестом."""
        self.dsl = DigitalSignatureLibrary()
        self.data = b"Hello, World!"
        self.invalid_data = b"Invalid Data"

    def test_elgamal_sign_and_verify(self):
        """Тест для подписи и проверки подписи Эль-Гамаля."""
        # Создаем подпись
        signature = self.dsl.ElGamalSign(self.data)
        self.assertIsInstance(signature, list)
        self.assertEqual(len(signature), 2)

        # Проверяем подпись
        self.assertTrue(self.dsl.ElGamalSignCheck(self.data, signature))

        # Проверяем подпись с некорректными данными
        self.assertFalse(self.dsl.ElGamalSignCheck(self.invalid_data, signature))

    def test_rsa_sign_and_verify(self):
        """Тест для подписи и проверки подписи RSA."""
        # Создаем подпись
        signature = self.dsl.RSASign(self.data)
        self.assertIsInstance(signature, list)
        self.assertEqual(len(signature), 16)  # MD5 хэш имеет 16 байт

        # Проверяем подпись
        self.assertTrue(self.dsl.RSASignCheck(self.data, signature))

        # Проверяем подпись с некорректными данными
        self.assertFalse(self.dsl.RSASignCheck(self.invalid_data, signature))

    def test_gost_sign_and_verify(self):
        """Тест для подписи и проверки подписи ГОСТ."""
        # Создаем подпись
        signature = self.dsl.GOSTSign(self.data)
        self.assertIsInstance(signature, int)

        # Проверяем подпись
        self.assertTrue(self.dsl.GOSTSignCheck(self.data, signature))

        # Проверяем подпись с некорректными данными
        self.assertFalse(self.dsl.GOSTSignCheck(self.invalid_data, signature))

if __name__ == "__main__":
    unittest.main()