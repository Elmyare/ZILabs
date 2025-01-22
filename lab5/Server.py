from CryptoLibrary import CryptoLibrary
import hashlib

class ServerModule:
    class VoteOption:
        YES = 0
        NO = 1
        ABSTAIN = 2

    def __init__(self):
        # Генерация ключей RSA
        self.P = CryptoLibrary.generate_prime(2**511, 2**512 - 1)
        self.Q = CryptoLibrary.generate_prime(2**511, 2**512 - 1)
        self.N = self.P * self.Q
        self.Phi = (self.P - 1) * (self.Q - 1)
        self.D = CryptoLibrary.generate_random_big_integer(2, self.Phi - 1)
        while CryptoLibrary.gcd(self.D, self.Phi) != 1:
            self.D = CryptoLibrary.generate_random_big_integer(2, self.Phi - 1)
        self.C = CryptoLibrary.gcd_mod(self.D, self.Phi)[1]
        if self.C < 0:
            self.C += self.Phi

        self.names_voted = set()  # Имена проголосовавших
        self.votes_voted = []     # Список бюллетеней

    def get_blank(self, name, hh):
        """Подпись 'слепого' бюллетеня."""
        if name in self.names_voted:
            print(f"[SERVER] Пользователь {name} уже проголосовал.")
            return 0
        self.names_voted.add(name)
        print(f"[SERVER] Пользователь {name} получил бюллетень.")
        return CryptoLibrary.pow_module(hh, self.C, self.N)

    def set_blank(self, n, s):
        """Проверка и сохранение бюллетеня."""
        hash_10 = self.my_sha(n)
        if hash_10 == CryptoLibrary.pow_module(s, self.D, self.N):
            self.votes_voted.append([n, s])
            print("[SERVER] Бюллетень принят.")
            return True
        else:
            print("[SERVER] Бюллетень не принят.")
            return False

    def voting_results(self):
        """Подсчет результатов голосования."""
        votes_dict = {
            self.VoteOption.YES: 0,
            self.VoteOption.NO: 0,
            self.VoteOption.ABSTAIN: 0,
        }

        for vote in self.votes_voted:
            n = vote[0]
            masked_n = n & 0b11  # Маскируем, чтобы получить вариант голоса
            if masked_n in votes_dict:
                votes_dict[masked_n] += 1

        print("[SERVER] Текущие итоги голосования:")
        for option, count in votes_dict.items():
            print(f"\t{option}: {count} голосов")
        return votes_dict

    @staticmethod
    def my_sha(n):
        """Хэш-функция SHA-3 (512 бит)."""
        byte_array = n.to_bytes((n.bit_length() + 7) // 8, 'big')
        hash_obj = hashlib.sha3_512(byte_array)
        hash_hex = hash_obj.hexdigest()
        return int(hash_hex, 16)

    @staticmethod
    def inverse(n, p):
        """Обратное число по модулю."""
        inv = CryptoLibrary.gcd_mod(n, p)[1]
        if inv < 0:
            inv += p
        return inv