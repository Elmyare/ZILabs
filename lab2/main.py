from EncryptLibrary import EncryptLibrary

# Чтение файла
data = EncryptLibrary.read_file("input.txt")
if data is None:
    print("Не удалось прочитать файл. Завершение программы.")
    exit()

# Шифрование Вернама
print("Шифрование Вернама...")
encoded_vernam, key = EncryptLibrary.vernam_encode(data)
EncryptLibrary.write_bytes_to_file("encoded_vernam.bin", encoded_vernam)

# Дешифрование Вернама
print("Дешифрование Вернама...")
decoded_vernam = EncryptLibrary.vernam_decode(encoded_vernam, key)
EncryptLibrary.write_bytes_to_file("decoded_vernam.txt", decoded_vernam)

# Шифрование RSA
print("Шифрование RSA...")
encoded_rsa, rsa_keys = EncryptLibrary.rsa_encode(data)
EncryptLibrary.write_big_integers_to_file("encoded_rsa.bin", encoded_rsa)

# Дешифрование RSA
print("Дешифрование RSA...")
decoded_rsa = EncryptLibrary.rsa_decode(encoded_rsa, rsa_keys)
EncryptLibrary.write_bytes_to_file("decoded_rsa.txt", decoded_rsa)

# Шифрование Эль-Гамаля
print("Шифрование Эль-Гамаля...")
encoded_elgamal, elgamal_keys = EncryptLibrary.elgamal_encode(data)
EncryptLibrary.write_big_integers_to_file("encoded_elgamal.bin", encoded_elgamal)

# Дешифрование Эль-Гамаля
print("Дешифрование Эль-Гамаля...")
decoded_elgamal = EncryptLibrary.elgamal_decode(encoded_elgamal, elgamal_keys)
EncryptLibrary.write_bytes_to_file("decoded_elgamal.txt", decoded_elgamal)

# Шифрование Шамира
print("Шифрование Шамира...")
encoded_shamir, shamir_keys = EncryptLibrary.shamir_encode(data)
EncryptLibrary.write_big_integers_to_file("encoded_shamir.bin", encoded_shamir)

# Дешифрование Шамира
print("Дешифрование Шамира...")
decoded_shamir = EncryptLibrary.shamir_decode(encoded_shamir, shamir_keys)
EncryptLibrary.write_bytes_to_file("decoded_shamir.txt", decoded_shamir)

print("Все операции завершены.")