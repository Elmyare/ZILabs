import random
from CryptoLibrary import CryptoLibrary

# Функция для чтения графа из файла
def read_graph(filename):
    with open(filename, 'r') as file:
        n, m = map(int, file.readline().split())
        edges = [tuple(map(int, file.readline().split())) for _ in range(m)]
    return n, edges

# Функция для создания изоморфного графа
def create_isomorphic_graph(n, edges, permutation):
    new_edges = []
    for u, v in edges:
        new_u = permutation[u - 1]
        new_v = permutation[v - 1]
        new_edges.append((new_u, new_v))
    return new_edges

# Функция для создания матрицы смежности
def create_adjacency_matrix(n, edges):
    matrix = [[0] * n for _ in range(n)]
    for u, v in edges:
        matrix[u - 1][v - 1] = 1
        matrix[v - 1][u - 1] = 1
    return matrix

# Функция для кодирования матрицы смежности с добавлением случайных чисел
def encode_matrix(matrix):
    encoded_matrix = []
    for row in matrix:
        encoded_row = [int(str(random.randint(1, 5)) + str(x)) for x in row]
        encoded_matrix.append(encoded_row)
    return encoded_matrix

# Функция для шифрования матрицы с использованием RSA
def encrypt_matrix(matrix, d, N):
    encrypted_matrix = []
    for row in matrix:
        encrypted_row = [pow(x, d, N) for x in row]
        encrypted_matrix.append(encrypted_row)
    return encrypted_matrix

# Функция для расшифровки матрицы с использованием RSA
def decrypt_matrix(matrix, c, N):
    decrypted_matrix = []
    for row in matrix:
        decrypted_row = [pow(x, c, N) for x in row]
        decrypted_matrix.append(decrypted_row)
    return decrypted_matrix

# Функция для проверки изоморфизма графов
def check_isomorphism(permutation, original_edges, isomorphic_edges):
    for u, v in original_edges:
        new_u = permutation[u - 1]
        new_v = permutation[v - 1]
        if (new_u, new_v) not in isomorphic_edges and (new_v, new_u) not in isomorphic_edges:
            return False
    return True

# Основная функция
def main():
    # Чтение графа из файла
    n, edges = read_graph("graph.txt")
    print(f"Граф: {edges}")
    
    print("Матрица смежности: \n"+"\n".join(map(str, create_adjacency_matrix(n, edges))))

    # Чтение гамильтонова цикла из файла
    with open("cycle.txt", 'r') as file:
        cycle = list(map(int, file.readline().split()))
    print(f"Гамильтонов цикл: {cycle}")
    
    # Параметры RSA
    N = 55  # Модуль
    d = 3   # Открытый ключ
    c = 27  # Закрытый ключ (d * c ≡ 1 mod φ(N), где φ(N) = 40 для N = 55)
    
    # Демонстрация протокола
    print("Демонстрация протокола доказательства с нулевым знанием:")
    proof_successful = True
    
    for i in range(5):  # Повторяем протокол несколько раз для надежности
        print(f"\nПопытка {i + 1}:")
        
        # Шаг 1: Алиса создает изоморфный граф
        permutation = list(range(1, n + 1))
        random.shuffle(permutation)
        print(f"Перестановка вершин: {permutation}")
        isomorphic_edges = create_isomorphic_graph(n, edges, permutation)
        
        # Шаг 2: Алиса кодирует и шифрует матрицу смежности
        matrix = create_adjacency_matrix(n, isomorphic_edges)
        encoded_matrix = encode_matrix(matrix)
        encrypted_matrix = encrypt_matrix(encoded_matrix, d, N)
        print("Закодированная матрица: \n" + "\n".join(map(str, encoded_matrix)))
        print("Зашифрованная матрица: \n" + "\n".join(map(str, encrypted_matrix)))
        
        # Шаг 3: Боб выбирает вопрос
        challenge = random.randint(0, 1)
        print(f"Запрос проверяющего: {challenge}")
        
        # Шаг 4: Алиса отвечает на вопрос
        if challenge == 0:
            # Показать гамильтонов цикл в изоморфном графе
            isomorphic_cycle = [permutation[v - 1] for v in cycle]
            print("Изоморфный граф: \n"+"\n".join(map(str, matrix)))
            
            print(f"Гамильтонов цикл в изоморфном графе: {isomorphic_cycle}")
            
            # Алиса расшифровывает ребра, образующие гамильтонов цикл
            decrypted_cycle_edges = []
            for i in range(n):
                u = isomorphic_cycle[i]
                v = isomorphic_cycle[(i + 1) % n]
                decrypted_edge = pow(encrypted_matrix[u - 1][v - 1], c, N)
                decrypted_cycle_edges.append(decrypted_edge)
            print(f"Расшифрованные ребра цикла: {decrypted_cycle_edges}")
            
            # Проверка, что цикл корректен
            if not all((isomorphic_cycle[i], isomorphic_cycle[(i + 1) % n]) in isomorphic_edges for i in range(n)):
                print("Ошибка: доказательство не прошло проверку.")
                proof_succes= False
                break
        else:
            # Доказать изоморфизм графов
            print(f"Перестановка вершин: {permutation}")
            
            # Алиса расшифровывает матрицу полностью
            decrypted_matrix = decrypt_matrix(encrypted_matrix, c, N)
            print("Расшифрованная матрица: \n" + "\n".join(map(str, decrypted_matrix)))
            
            # Проверка изоморфизма
            if not check_isomorphism(permutation, edges, isomorphic_edges):
                print("Ошибка: доказательство не прошло проверку.")
                proof_successful = False
                break
            print("Изоморфизм графов подтвержден.")
        
        # Шаг 5: Боб проверяет правильность расшифровки
        if challenge == 0:
            # Проверка гамильтонова цикла
            # Боб проверяет, что ребра цикла соответствуют зашифрованной матрице
            for i in range(n):
                u = isomorphic_cycle[i]
                v = isomorphic_cycle[(i + 1) % n]
                if encrypted_matrix[u - 1][v - 1] != pow(encoded_matrix[u - 1][v - 1], d, N):
                    print("Ошибка: доказательство не прошло проверку.")
                    proof_successful = False
                    break
        else:
            # Проверка изоморфизма
            # Боб проверяет, что перестановка вершин корректна
            # Применяем операцию % 10 к каждому элементу двумерного списка
            decrypted_matrix = [[element % 10 for element in row] for row in decrypted_matrix]
            decrypted_edges = [(i, j) for j, val in enumerate([val for i, val in enumerate(decrypted_matrix)]) if val == 1]
            if not check_isomorphism(permutation, edges, isomorphic_edges):
                print("Ошибка: доказательство не прошло проверку.")
                proof_successful = False
                break
            else:
                print("Изоморфен")
    
    if proof_successful:
        print("Доказательство успешно завершено.")
    else:
        print("Доказательство не прошло проверку.")

if __name__ == "__main__":
    main()