import unittest
import math
from CryptoLibrary import CryptoLibrary

class TestCryptoLibrary(unittest.TestCase):

    def test_generate_random_big_integer(self):
        min_value, max_value = 10, 1000
        result = CryptoLibrary.generate_random_big_integer(min_value, max_value)
        self.assertGreaterEqual(result, min_value)
        self.assertLess(result, max_value)

    def test_pow_module(self):
        a, x, p = 4, 13, 497
        expected = pow(a, x, p)
        result = CryptoLibrary.pow_module(a, x, p)
        self.assertEqual(result, expected)

    def test_gcd_mod(self):
        a, b = 252, 198
        gcd = math.gcd(a, b)
        result = CryptoLibrary.gcd_mod(a, b)
        self.assertEqual(result[0], gcd)
        self.assertTrue(a * result[1] + b * result[2] == gcd)

    def test_check_prime(self):
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23]
        non_primes = [4, 6, 8, 9, 10, 12, 14, 15, 16]

        for p in primes:
            self.assertTrue(CryptoLibrary.check_prime(p), f"{p} is prime, but check_prime returned False")
        for np in non_primes:
            self.assertFalse(CryptoLibrary.check_prime(np), f"{np} is not prime, but check_prime returned True")

    def test_generate_prime(self):
        left, right = 10, 100
        result = CryptoLibrary.generate_prime(left, right)
        self.assertTrue(CryptoLibrary.check_prime(result))
        self.assertGreaterEqual(result, left)
        self.assertLess(result, right)

    def test_diffie_hellman_algorithm(self):
        Xa, Xb, Ya, Yb, Zab, Zba = CryptoLibrary.diffie_hellman_algorithm()
        self.assertEqual(Zab, Zba)

    def test_giant_baby_step(self):
        a, p, y = 2, 101, 10
        result = CryptoLibrary.giant_baby_step(a, p, y)
        expected = None
        for x in range(p):
            if CryptoLibrary.pow_module(a, x, p) == y:
                expected = x
                break
        self.assertEqual(result, expected)

    def test_pow_big_integer(self):
        a, p = 2, 10
        result = CryptoLibrary.pow_big_integer(a, p)
        expected = a ** p
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()
