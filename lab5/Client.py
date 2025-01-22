from CryptoLibrary import CryptoLibrary
from Server import ServerModule

class ClientModule:
    def __init__(self, server, name):
        self.server = server
        self.name = name

    def vote(self, vote_option):
        """Голосование с использованием 'слепой' подписи."""
        # Генерация случайного числа r
        r = CryptoLibrary.generate_random_big_integer(2, self.server.N - 1)
        while CryptoLibrary.gcd(r, self.server.N) != 1:
            r = CryptoLibrary.generate_random_big_integer(2, self.server.N - 1)

        # Формирование бюллетеня
        shifted_r = r << 512
        n = shifted_r | vote_option

        # "Ослепление" бюллетеня
        hash_10 = self.server.my_sha(n)
        hh = (hash_10 * CryptoLibrary.pow_module(r, self.server.D, self.server.N)) % self.server.N

        # Получение подписи от сервера
        ss = self.server.get_blank(self.name, hh)
        if ss == 0:
            print("[CLIENT] Голосование отклонено: вы уже проголосовали.")
            return

        # "Снятие ослепления"
        s = (ss * self.server.inverse(r, self.server.N)) % self.server.N

        # Отправка бюллетеня на сервер
        if self.server.set_blank(n, s):
            print("[CLIENT] Ваш голос принят.")
        else:
            print("[CLIENT] Ваш голос не принят.")