from EncryptLibrary import EncryptLibrary
# Чтение файла
data = EncryptLibrary.read_file("input.txt")

# Шифрование Вернама
encoded_vernam, key = EncryptLibrary.vernam_encode(data)
EncryptLibrary.write_bytes_to_file("encoded_vernam.bin", encoded_vernam)

# Дешифрование Вернама
decoded_vernam = EncryptLibrary.vernam_decode(encoded_vernam, key)
EncryptLibrary.write_bytes_to_file("decoded_vernam.txt", decoded_vernam)

# Шифрование RSA
encoded_rsa, rsa_keys = EncryptLibrary.rsa_encode(data)
EncryptLibrary.write_big_integers_to_file("encoded_rsa.bin", encoded_rsa)

# Дешифрование RSA
decoded_rsa = EncryptLibrary.rsa_decode(encoded_rsa, rsa_keys)
EncryptLibrary.write_bytes_to_file("decoded_rsa.txt", decoded_rsa)