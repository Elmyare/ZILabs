import socket
import threading
import json
import random
import sys
from CryptoLibrary import CryptoLibrary

def server():
    try:
        # Генерация открытых параметров системы
        n = CryptoLibrary.generate_n()
        print(f"Сервер: n = {n}")
        
        # Загрузка открытых ключей из файла
        keys = {}
        with open("keys.txt", "r") as f:
            for line in f:
                try:
                    login, v = line.strip().split()
                    keys[login] = int(v)
                except ValueError:
                    print(f"Ошибка в формате строки: {line}")
                    continue
        
        # Создание сокета
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Переиспользование порта
        server_socket.bind(('localhost', 12345))
        server_socket.listen(5)
        print("Сервер запущен и ожидает подключения...")
        
        while True:
            try:
                client_socket, addr = server_socket.accept()
                print(f"Подключен клиент: {addr}")
                
                # Отправка клиенту открытых параметров системы в формате JSON
                client_socket.send(json.dumps({"n": n}).encode())
                
                # Получение логина от клиента
                login = client_socket.recv(1024).decode()
                if login not in keys:
                    client_socket.send("Логин не найден".encode())
                    client_socket.close()
                    continue
                
                v = keys[login]
                print(f"Сервер: Логин = {login}, v = {v}")
                client_socket.send(json.dumps({"v": v}).encode())
                
                # Проведение нескольких раундов доказательства
                for _ in range(10):  # 10 раундов для надежности
                    # Получение x от клиента
                    x = int(client_socket.recv(1024).decode())
                    
                    # Генерация случайного бита (0 или 1)
                    e = random.randint(0, 1)
                    client_socket.send(f"{e}".encode())
                    
                    # Получение y от клиента
                    y = int(client_socket.recv(1024).decode())
                    
                    # Проверка доказательства
                    if y == 0:
                        client_socket.send("Доказательство не прошло".encode())
                        client_socket.close()
                        break
                    
                    # Вычисление ожидаемого значения
                    expected = (x * (v ** e)) % n
                    actual = (y * y) % n
                    
                    if actual == expected:
                        client_socket.send("Доказательство прошло".encode())
                    else:
                        print(f"Сервер: Ошибка в раунде. Ожидалось: {expected}, Получено: {actual}")
                        client_socket.send("Доказательство не прошло".encode())
                        client_socket.close()
                        break
                else:
                    client_socket.send("Авторизация успешна".encode())
                    client_socket.close()
            except Exception as e:
                print(f"Ошибка при обработке клиента: {e}")
                client_socket.close()
    except Exception as e:
        print(f"Ошибка на сервере: {e}")
    finally:
        server_socket.close()
        print("Сервер завершил работу.")

def client():
    try:
        # Подключение к серверу
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('localhost', 12345))
        
        # Получение открытых параметров системы в формате JSON
        n_data = client_socket.recv(1024).decode()
        n = json.loads(n_data)["n"]
        print(f"Клиент: n = {n}")
        
        # Ввод логина
        login = input("Введите логин: ")
        client_socket.send(login.encode())
        
        # Получение v от сервера в формате JSON
        v_data = client_socket.recv(1024).decode()
        v = json.loads(v_data)["v"]
        print(f"Клиент: v = {v}")
        
        # Ввод секрета s
        s = int(input("Введите секрет s: "))
        
        # Проведение нескольких раундов доказательства
        for _ in range(10):  # 10 раундов для надежности
            # Генерация случайного r
            r = CryptoLibrary.generate_random_big_integer(1, n - 1)
            x = CryptoLibrary.pow_module(r, 2, n)
            client_socket.send(f"{x}".encode())
            
            # Получение e от сервера
            e = int(client_socket.recv(1024).decode())
            
            # Вычисление y
            y = (r * (s ** e)) % n
            client_socket.send(f"{y}".encode())
            
            # Получение результата проверки
            result = client_socket.recv(1024).decode()
            print(result)
            if result != "Доказательство прошло":
                break
        else:
            print("Авторизация успешна")
    except Exception as e:
        print(f"Ошибка в клиенте: {e}")
    finally:
        client_socket.close()

# Запуск сервера или клиента
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Использование: python3 rgr.py [server|client]")
    elif sys.argv[1] == "server":
        server()
    elif sys.argv[1] == "client":
        client()
    else:
        print("Неверный аргумент. Используйте 'server' или 'client'.")