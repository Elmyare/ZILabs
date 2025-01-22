import random
from CryptoLibrary import CryptoLibrary  # Используем вашу криптографическую библиотеку
import tkinter as tk
from tkinter import messagebox

class MentalPoker:
    def __init__(self):
        self.types = {"P": "♠", "K": "♣", "C": "♥", "B": "♦"}
        self.card_types = ["P", "K", "C", "B"]
        self.card_numbers = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        self.cards_deck = []
        self.generate_deck()

    def generate_deck(self):
        """Генерация колоды карт."""
        for ct in self.card_types:
            for cn in self.card_numbers:
                self.cards_deck.append(f"{cn}{ct}")

    def shuffle_deck(self, deck):
        """Перемешивание колоды."""
        return random.sample(deck, len(deck))

    def mental_poker(self, players_num):
        """Реализация алгоритма Ментальный покер."""
        # Генерация простого числа p
        while True:
            q = CryptoLibrary.generate_prime(0, 1000000000)
            p = 2 * q + 1
            if CryptoLibrary.check_prime(p):
                break

        # Генерация ключей для каждого игрока
        C = []
        D = []
        for _ in range(players_num):
            c_temp = CryptoLibrary.generate_random_big_integer(1, p - 1)
            while CryptoLibrary.gcd(c_temp, p - 1) != 1:
                c_temp = CryptoLibrary.generate_random_big_integer(1, p - 1)
            d_temp = CryptoLibrary.gcd_mod(c_temp, p - 1)[1]
            if d_temp < 0:
                d_temp += p - 1
            C.append(c_temp)
            D.append(d_temp)

        # Создание колоды карт
        deck_keys = list(range(2, 2 + len(self.cards_deck)))  # Индексы карт
        deck_keys = self.shuffle_deck(deck_keys)

        # Шифрование колоды каждым игроком
        for i in range(players_num):
            new_deck_keys = []
            for key in deck_keys:
                new_key = CryptoLibrary.pow_module(key, C[i], p)
                new_deck_keys.append(new_key)
            deck_keys = self.shuffle_deck(new_deck_keys)

        # Раздача карт игрокам и на стол
        hands = []
        for _ in range(players_num):
            hand = []
            for _ in range(2):
                card = deck_keys.pop()
                hand.append(card)
            hands.append(hand)

        table = []
        for _ in range(5):
            table.append(deck_keys.pop())

        # Расшифровка карт на столе
        for i in range(players_num):
            for j in range(len(table)):
                table[j] = CryptoLibrary.pow_module(table[j], D[i], p)

        # Расшифровка карт игроков
        for i in range(players_num):
            for j in range(players_num):
                if i != j:
                    for k in range(len(hands[i])):
                        hands[i][k] = CryptoLibrary.pow_module(hands[i][k], D[j], p)
            for k in range(len(hands[i])):
                hands[i][k] = CryptoLibrary.pow_module(hands[i][k], D[i], p)

        # Преобразование индексов в карты
        result = []
        for hand in hands:
            result.append([self.cards_deck[key - 2] for key in hand])
        result.append([self.cards_deck[key - 2] for key in table])

        return result


class PokerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ментальный покер")
        self.players_num = 2  # По умолчанию 2 игрока

        self.label = tk.Label(root, text="Введите количество игроков:")
        self.label.pack()

        self.entry = tk.Entry(root)
        self.entry.pack()

        self.button = tk.Button(root, text="Начать игру", command=self.start_game)
        self.button.pack()

    def format_card(self, card):
        """Преобразует буквенные масти в символы."""
        suit_map = {"P": "♠", "K": "♣", "C": "♥", "B": "♦"}
        number = card[:-1]  # Все символы, кроме последнего (номер)
        suit = card[-1]     # Последний символ (масть)
        return f"{number}{suit_map.get(suit, suit)}"  # Если масть не найдена, оставляем как есть

    def start_game(self):
        try:
            self.players_num = int(self.entry.get())
            if self.players_num < 2:
                raise ValueError("Количество игроков должно быть не менее 2.")
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))
            return

        poker = MentalPoker()
        result = poker.mental_poker(self.players_num)

        # Отображение результатов
        result_window = tk.Toplevel(self.root)
        result_window.title("Результаты")

        # Вывод карт игроков
        for i in range(self.players_num):
            formatted_cards = [self.format_card(card) for card in result[i]]
            label = tk.Label(result_window, text=f"Игрок {i + 1}: {', '.join(formatted_cards)}")
            label.pack()

        # Вывод карт на столе
        formatted_table_cards = [self.format_card(card) for card in result[-1]]
        label = tk.Label(result_window, text=f"На столе: {', '.join(formatted_table_cards)}")
        label.pack()


if __name__ == "__main__":
    root = tk.Tk()
    app = PokerApp(root)
    root.mainloop()