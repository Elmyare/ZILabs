import socket
import json
import random
from CryptoLibrary import CryptoLibrary

# ======= Серверная часть =======
class FiatShamirServer:
    def __init__(self, host="localhost", port=12345):
        self.host = host
        self.port = port
        self.public_keys = {}  # Хранение открытых ключей в формате {login: (v, n)}
        self.n = CryptoLibrary.generate_n()  # Генерация модуля n

    def load_keys(self, filename="keys.txt"):
        try:
            with open(filename, "r") as file:
                self.public_keys = json.load(file)
        except FileNotFoundError:
            self.public_keys = {}

    def save_keys(self, filename="keys.txt"):
        with open(filename, "w") as file:
            json.dump(self.public_keys, file)
            
    def handle_client(self, client_socket):
        try:
            # Отправка модуля n клиенту
            print(f"Sending n to client: n={self.n}")  # Отладочный вывод
            client_socket.send(json.dumps({"n": self.n}).encode())

            # Получение логина и открытого ключа от клиента
            data = json.loads(client_socket.recv(1024).decode())
            login = data["login"]
            v = data["v"]

            # Сохранение открытого ключа
            self.public_keys[login] = v
            self.save_keys()

            # Взаимодействие по протоколу
            y = int(client_socket.recv(1024).decode())
            c = random.randint(0, 1)
            client_socket.send(str(c).encode())

            r = int(client_socket.recv(1024).decode())
            v = self.public_keys[login]

            # Проверка доказательства
            left = CryptoLibrary.pow_module(r, 2, self.n)
            right = (y * CryptoLibrary.pow_module(v, c, self.n)) % self.n

            print(f"DEBUG: Server Verification:")
            print(f"  Left (r^2 mod n): {left}")
            print(f"  Right (y * v^c mod n): {right}")
            print(f"  Parameters: r={r}, y={y}, c={c}, v={v}, n={self.n}")

            if left == right:
                client_socket.send("OK".encode())
            else:
                client_socket.send("FAIL".encode())

        except Exception as e:
            print(f"Error handling client: {e}")

    def start(self):
        self.load_keys()
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        print(f"Server running on {self.host}:{self.port}")

        while True:
            client_socket, addr = server_socket.accept()
            print(f"Connection from {addr}")
            self.handle_client(client_socket)
            client_socket.close()

# ======= Клиентская часть =======
class FiatShamirClient:
    def __init__(self, host="localhost", port=12345):
        self.host = host
        self.port = port
        self.n = None  # Модуль n
        self.secret_key = None

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))

    def receive_params(self):
        # Получение параметра n от сервера
        print("Waiting for parameters from server...")  # Отладочный вывод
        params = json.loads(self.socket.recv(1024).decode())
        print(f"Received parameters: {params}")  # Отладочный вывод
        self.n = params["n"]

    def register(self, login):
        self.secret_key = CryptoLibrary.generate_random_big_integer(2, self.n - 1)
        v = CryptoLibrary.pow_module(self.secret_key, 2, self.n)  # v = s^2 mod n
        print(f"DEBUG: Client Registration:")
        print(f"  Secret Key: {self.secret_key}")
        print(f"  Public Key (v): {v}")
        self.socket.send(json.dumps({"login": login, "v": v}).encode())

    def authenticate(self):
        r = CryptoLibrary.generate_random_big_integer(1, self.n - 1)
        y = CryptoLibrary.pow_module(r, 2, self.n)  # y = r^2 mod n
        print(f"DEBUG: Client Authentication:")
        print(f"  Random r: {r}")
        print(f"  y (r^2 mod n): {y}")
        self.socket.send(str(y).encode())

        c = int(self.socket.recv(1024).decode())
        print(f"  Challenge (c): {c}")
        r_response = (r + c * self.secret_key) % self.n
        print(f"  r_response ((r + c * secret_key) mod n): {r_response}")
        self.socket.send(str(r_response).encode())

        result = self.socket.recv(1024).decode()
        return result

    def close(self):
        self.socket.close()

# ======= Запуск =======
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Fiat-Shamir Protocol")
    parser.add_argument("role", choices=["server", "client"], help="Role: server or client")
    parser.add_argument("--login", help="Login for the client")

    args = parser.parse_args()

    if args.role == "server":
        server = FiatShamirServer()
        server.start()
    elif args.role == "client":
        if not args.login:
            print("Login is required for client.")
            exit(1)

        client = FiatShamirClient()
        client.connect()
        client.receive_params()
        client.register(args.login)

        result = client.authenticate()
        print(f"Authentication result: {result}")
        client.close()