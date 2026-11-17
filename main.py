"Консольный интерфейс для проверки СНИЛС"

from snils import is_valid_snils


def main() -> None:

    "Запрос строку и показ результата проверки"

    value = input("Введите СНИЛС: ")
    if is_valid_snils(value):
        print("Формат СНИЛС корректен.")
    else:
        print("Формат СНИЛС некорректен.")


if __name__ == "__main__":
    main()