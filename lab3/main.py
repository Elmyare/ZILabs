from DigitalSignatureLibrary import DigitalSignatureLibrary

def main():
    dsl = DigitalSignatureLibrary()

    # Путь к файлу для подписи
    input_file = "input.txt"
    output_file = "output.txt"

    # Чтение данных из файла
    data = dsl.read_file(input_file)
    if data is None:
        print("Не удалось прочитать файл. Завершение программы.")
        return

    # Подписание файла с использованием Эль-Гамаля
    print("Подписание файла с использованием Эль-Гамаля...")
    elgamal_signature = dsl.ElGamalSign(data)
    dsl.write_signature("elgamal_signature.txt", elgamal_signature)

    # Проверка подписи Эль-Гамаля
    print("Проверка подписи Эль-Гамаля...")
    if dsl.ElGamalSignCheck(data, elgamal_signature):
        print("Подпись Эль-Гамаля верна.")
    else:
        print("Подпись Эль-Гамаля недействительна.")

    # Подписание файла с использованием RSA
    print("Подписание файла с использованием RSA...")
    rsa_signature = dsl.RSASign(data)
    dsl.write_signature("rsa_signature.txt", rsa_signature)

    # Проверка подписи RSA
    print("Проверка подписи RSA...")
    if dsl.RSASignCheck(data, rsa_signature):
        print("Подпись RSA верна.")
    else:
        print("Подпись RSA недействительна.")

    # Подписание файла с использованием ГОСТ
    print("Подписание файла с использованием ГОСТ...")
    gost_signature = dsl.GOSTSign(data)
    dsl.write_signature("gost_signature.txt", gost_signature)

    # Проверка подписи ГОСТ
    print("Проверка подписи ГОСТ...")
    if dsl.GOSTSignCheck(data, gost_signature):
        print("Подпись ГОСТ верна.")
    else:
        print("Подпись ГОСТ недействительна.")

if __name__ == "__main__":
    main()