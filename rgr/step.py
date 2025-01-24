from sympy import symbols, Eq, mod_inverse, sqrt_mod

n = 2366449  # Пример значения n
v = 12345    # Пример значения v

# Находим s, такое что s^2 ≡ v mod n
s_candidates = sqrt_mod(v, n, all_roots=True)

if s_candidates:
    print(f"Найденные секреты s: {s_candidates}")
else:
    print("Секрет s не найден.")