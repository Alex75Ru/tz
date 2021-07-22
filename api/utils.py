def check_password(data):
    # Функция проверки пароля - минимум 8 знаков, должны быть цифры, строчные и заглавные буквы
    foo = (bool(len(data) > 7),
           any(map(lambda x: x.isdigit(), data)),
           any(map(lambda x: x.islower(), data)),
           any(map(lambda x: x.isupper(), data)))
    return all(foo)
