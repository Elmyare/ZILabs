import random
import math

class CryptoLibrary:

    @staticmethod
    def generate_random_big_integer(min_value, max_value, size=8):
        if min_value >= max_value:
            raise ValueError(f"Minimum value must be less than maximum value: {min_value} >= {max_value}")
        range_value = max_value - min_value
        random_value = int.from_bytes(random.randbytes(size), 'big')
        return (random_value % range_value) + min_value

    @staticmethod
    def pow_module(a, x, p):
        result = 1
        a = a % p
        if a == 0:
            return 0

        while x > 0:
            if x & 1:
                result = (result * a) % p
            a = (a * a) % p
            x >>= 1

        return result

    @staticmethod
    def gcd_mod(a, b):
        U = [a, 1, 0]
        V = [b, 0, 1]

        while V[0] != 0:
            q = U[0] // V[0]
            T = [U[0] % V[0], U[1] - q * V[1], U[2] - q * V[2]]
            U, V = V, T

        return U

    @staticmethod
    def check_prime(p):
        if p <= 1:
            return False
        if p == 2 or p == 3:
            return True
        if p % 2 == 0:
            return False

        # Проверка делимости на нечётные числа до квадратного корня из p
        for i in range(3, int(math.sqrt(p)) + 1, 2):
            if p % i == 0:
                return False
        return True


    @staticmethod
    def gcd(a, b):
        while b != 0:
            a, b = b, a % b
        return a

    @staticmethod
    def generate_prime(left, right):
        if left >= right:
            raise ValueError("Left bound must be less than right bound.")
        while True:
            p = CryptoLibrary.generate_random_big_integer(left, right)
            if CryptoLibrary.check_prime(p):
                return p


    @staticmethod
    def diffie_hellman_algorithm():
        q = 0
        p = 0

        while True:
            q = CryptoLibrary.generate_prime(0, 1000000000)
            p = 2 * q + 1
            if CryptoLibrary.check_prime(p):
                break

        g = random.randint(1, p - 1)
        while CryptoLibrary.pow_module(g, q, p) == 1:
            g = random.randint(1, p - 1)

        Xa = random.randint(1, p)
        Xb = random.randint(1, p)

        Ya = CryptoLibrary.pow_module(g, Xa, p)
        Yb = CryptoLibrary.pow_module(g, Xb, p)

        Zab = CryptoLibrary.pow_module(Yb, Xa, p)
        Zba = CryptoLibrary.pow_module(Ya, Xb, p)

        return Xa, Xb, Ya, Yb, Zab, Zba

    @staticmethod
    def giant_baby_step(a, p, y):
        k = math.ceil(math.sqrt(p))
        m = math.ceil(math.sqrt(p))

        baby_steps = {CryptoLibrary.pow_module(a, j, p) * y % p: j for j in range(m)}
        for i in range(1, k + 1):
            giant_step = CryptoLibrary.pow_module(a, i * m, p)
            if giant_step in baby_steps:
                return i * m - baby_steps[giant_step]

        return None

    @staticmethod
    def pow_big_integer(a, p):
        result = a
        for _ in range(1, p):
            result *= a
        return result
