import os
import random
from CryptoLibrary import CryptoLibrary  # Используем вашу библиотеку из первой лабораторной

class EncryptLibrary:

    @staticmethod
    def generate_coprime(p):
        """Генерация взаимно простого числа с p."""
        result = CryptoLibrary.generate_random_big_integer(2, p)
        while CryptoLibrary.gcd(p, result) != 1:
            result = CryptoLibrary.generate_random_big_integer(2, p)
        return result

    @staticmethod
    def read_file(file_path):
        """Чтение файла в виде массива байтов."""
        try:
            with open(file_path, "rb") as file:
                return bytearray(file.read())
        except Exception as e:
            print(f"Ошибка при чтении файла: {e}")
            return None

    @staticmethod
    def write_bytes_to_file(file_path, data):
        """Запись массива байтов в файл."""
        try:
            with open(file_path, "wb") as file:
                file.write(data)
            print("Файл успешно записан.")
        except Exception as e:
            print(f"Ошибка при записи файла: {e}")

    @staticmethod
    def write_big_integers_to_file(file_path, big_integers):
        """Запись массива BigInteger в файл."""
        try:
            with open(file_path, "wb") as file:
                for num in big_integers:
                    # Преобразуем число в байты и записываем его длину
                    byte_data = num.to_bytes((num.bit_length() + 7) // 8, byteorder='big')
                    file.write(len(byte_data).to_bytes(4, byteorder='big'))
                    file.write(byte_data)
            print("Файл успешно записан.")
        except Exception as e:
            print(f"Ошибка при записи файла: {e}")

    @staticmethod
    def read_big_integers_from_file(file_path):
        """Чтение массива BigInteger из файла."""
        try:
            with open(file_path, "rb") as file:
                big_integers = []
                while file.tell() < os.path.getsize(file_path):
                    # Читаем длину числа
                    length = int.from_bytes(file.read(4), byteorder='big')
                    # Читаем само число
                    byte_data = file.read(length)
                    big_integers.append(int.from_bytes(byte_data, byteorder='big'))
                return big_integers
        except Exception as e:
            print(f"Ошибка при чтении файла: {e}")
            return None

    @staticmethod
    def vernam_encode(data):
        """Шифрование Вернама."""
        key = bytearray(random.randint(0, 255) for _ in range(len(data)))
        encoded = bytearray(a ^ b for a, b in zip(data, key))
        return encoded, key

    @staticmethod
    def vernam_decode(data, key):
        """Дешифрование Вернама."""
        return bytearray(a ^ b for a, b in zip(data, key))

    @staticmethod
    def rsa_encode(data):
        """Шифрование RSA."""
        p = CryptoLibrary.generate_prime(0, 1000000000)
        q = CryptoLibrary.generate_prime(0, 1000000000)
        n = p * q
        phi = (p - 1) * (q - 1)
        d = EncryptLibrary.generate_coprime(phi)
        c = CryptoLibrary.gcd_mod(d, phi)[1]
        if c < 0:
            c += phi

        encoded = [CryptoLibrary.pow_module(byte, d, n) for byte in data]
        return encoded, (c, n)

    @staticmethod
    def rsa_decode(data, keys):
        """Дешифрование RSA."""
        c, n = keys
        return bytearray(CryptoLibrary.pow_module(num, c, n) for num in data)

    @staticmethod
    def elgamal_encode(data):
        """Шифрование Эль-Гамаля."""
        while True:
            q = CryptoLibrary.generate_prime(0, 1000000000)
            p = 2 * q + 1
            if CryptoLibrary.check_prime(p):
                break

        g = random.randint(2, p - 1)
        while CryptoLibrary.pow_module(g, q, p) != 1:
            g = random.randint(2, p - 1)

        x = random.randint(1, p - 1)
        y = CryptoLibrary.pow_module(g, x, p)
        k = random.randint(1, p - 2)
        a = CryptoLibrary.pow_module(g, k, p)

        encoded = [(byte * CryptoLibrary.pow_module(y, k, p)) % p for byte in data]
        return encoded, (p, g, x, y, k, a)

    @staticmethod
    def elgamal_decode(data, keys):
        """Дешифрование Эль-Гамаля."""
        p, _, x, _, _, a = keys
        return bytearray((num * CryptoLibrary.pow_module(a, p - 1 - x, p)) % p for num in data)

    @staticmethod
    def shamir_encode(data):
        """Шифрование Шамира."""
        p = CryptoLibrary.generate_prime(0, 1000000000)
        ca = EncryptLibrary.generate_coprime(p - 1)
        da = CryptoLibrary.gcd_mod(ca, p - 1)[1]
        if da < 0:
            da += p - 1

        cb = EncryptLibrary.generate_coprime(p - 1)
        db = CryptoLibrary.gcd_mod(cb, p - 1)[1]
        if db < 0:
            db += p - 1

        encoded = [
            CryptoLibrary.pow_module(
                CryptoLibrary.pow_module(
                    CryptoLibrary.pow_module(byte, ca, p), cb, p
                ), da, p
            ) for byte in data
        ]
        return encoded, (p, ca, da, cb, db)

    @staticmethod
    def shamir_decode(data, keys):
        """Дешифрование Шамира."""
        p, _, _, _, db = keys
        return bytearray(CryptoLibrary.pow_module(num, db, p) for num in data)