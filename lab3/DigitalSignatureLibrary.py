import hashlib
from CryptoLibrary import CryptoLibrary

class DigitalSignatureLibrary:
    def __init__(self):
        self.GamalKeys = []
        self.RSAKeys = []
        self.GOSTKeys = []

    def read_file(self, file_path):
        """Чтение файла в виде массива байтов."""
        try:
            with open(file_path, "rb") as file:
                return file.read()
        except Exception as e:
            print(f"Ошибка при чтении файла: {e}")
            return None

    def write_file(self, file_path, data):
        """Запись данных в файл."""
        try:
            with open(file_path, "wb") as file:
                file.write(data)
            print(f"Файл {file_path} успешно записан.")
        except Exception as e:
            print(f"Ошибка при записи файла: {e}")

    def write_signature(self, file_path, signature):
        """Запись подписи в файл."""
        try:
            with open(file_path, "w") as file:
                file.write(str(signature))
            print(f"Подпись сохранена в файл {file_path}.")
        except Exception as e:
            print(f"Ошибка при записи подписи: {e}")

    def read_signature(self, file_path):
        """Чтение подписи из файла."""
        try:
            with open(file_path, "r") as file:
                return eval(file.read())
        except Exception as e:
            print(f"Ошибка при чтении подписи: {e}")
            return None

    def ElGamalSign(self, data):
        while True:
            q = CryptoLibrary.generate_prime(0, 1000000000)
            p = 2 * q + 1
            if CryptoLibrary.check_prime(p):
                break

        g = CryptoLibrary.generate_random_big_integer(2, p - 1)
        while CryptoLibrary.pow_module(g, q, p) != 1:
            g = CryptoLibrary.generate_random_big_integer(2, p - 1)

        x = CryptoLibrary.generate_prime(0, p - 1)
        y = CryptoLibrary.pow_module(g, x, p)

        k = CryptoLibrary.generate_random_big_integer(1, p - 1)
        while CryptoLibrary.gcd(k, p - 1) != 1:
            k = CryptoLibrary.generate_random_big_integer(1, p - 1)

        r = CryptoLibrary.pow_module(g, k, p)

        hash_obj = hashlib.md5(data)
        hash_bytes = hash_obj.digest()
        hash_int = int.from_bytes(hash_bytes, 'big')

        s = (self.mod_inverse(k, p - 1) * (hash_int - x * r)) % (p - 1)
        if s < 0:
            s += (p - 1)

        self.GamalKeys = [p, g, y, r]
        return [r, s]

    def ElGamalSignCheck(self, data, signature):
        p, g, y, r = self.GamalKeys
        s = signature[1]

        hash_obj = hashlib.md5(data)
        hash_bytes = hash_obj.digest()
        hash_int = int.from_bytes(hash_bytes, 'big')

        v1 = (CryptoLibrary.pow_module(y, r, p) * CryptoLibrary.pow_module(r, s, p)) % p
        v2 = CryptoLibrary.pow_module(g, hash_int, p)

        return v1 == v2

    def RSASign(self, data):
        P = CryptoLibrary.generate_prime(0, 1000000000)
        Q = CryptoLibrary.generate_prime(0, 1000000000)
        N = P * Q
        Phi = (P - 1) * (Q - 1)

        d = CryptoLibrary.generate_random_big_integer(1, Phi)
        while CryptoLibrary.gcd(d, Phi) != 1:
            d = CryptoLibrary.generate_random_big_integer(1, Phi)

        c = CryptoLibrary.gcd_mod(d, Phi)[1]
        if c < 0:
            c += Phi

        self.RSAKeys = [N, d]

        hash_obj = hashlib.md5(data)
        hash_bytes = hash_obj.digest()

        # Подписываем каждый байт хэша
        signature = []
        for byte in hash_bytes:
            signature.append(CryptoLibrary.pow_module(byte, c, N))

        return signature

    def RSASignCheck(self, data, signature):
        N, d = self.RSAKeys

        hash_obj = hashlib.md5(data)
        hash_bytes = hash_obj.digest()

        # Проверяем каждый байт подписи
        for i, byte in enumerate(hash_bytes):
            calculated_byte = CryptoLibrary.pow_module(signature[i], d, N)
            if calculated_byte != byte:
                return False

        return True

    def GOSTSign(self, data):
        while True:
            q = CryptoLibrary.generate_prime(0, 1000000000)
            b = CryptoLibrary.generate_random_big_integer(0, 1000000000)
            p = q * b + 1
            if CryptoLibrary.check_prime(p):
                break

        g = CryptoLibrary.generate_random_big_integer(1, p - 1)
        a = CryptoLibrary.pow_module(g, b, p)
        while a <= 1:
            g = CryptoLibrary.generate_random_big_integer(1, p - 1)
            a = CryptoLibrary.pow_module(g, b, p)

        x = CryptoLibrary.generate_random_big_integer(1, q - 1)
        y = CryptoLibrary.pow_module(a, x, p)

        hash_obj = hashlib.md5(data)
        hash_bytes = hash_obj.digest()
        hash_int = int.from_bytes(hash_bytes, 'big')

        while True:
            k = CryptoLibrary.generate_random_big_integer(1, q - 1)
            r = CryptoLibrary.pow_module(a, k, p) % q
            if r != 0:
                s = (k * hash_int + x * r) % q
                if s != 0:
                    break

        self.GOSTKeys = [q, a, y, p, r]
        return s

    def GOSTSignCheck(self, data, signature):
        q, a, y, p, r = self.GOSTKeys
        s = signature

        hash_obj = hashlib.md5(data)
        hash_bytes = hash_obj.digest()
        hash_int = int.from_bytes(hash_bytes, 'big')

        hash_inverse = self.mod_inverse(hash_int, q)
        u1 = (s * hash_inverse) % q
        u2 = (-r * hash_inverse) % q
        if u2 < 0:
            u2 += q

        v = ((CryptoLibrary.pow_module(a, u1, p) * CryptoLibrary.pow_module(y, u2, p)) % p) % q
        return v == r

    def mod_inverse(self, a, m):
        g, x, y = self.extended_gcd(a, m)
        if g != 1:
            return None  # Обратного элемента не существует
        else:
            return x % m

    def extended_gcd(self, a, b):
        if a == 0:
            return (b, 0, 1)
        else:
            g, x, y = self.extended_gcd(b % a, a)
            return (g, y - (b // a) * x, x)