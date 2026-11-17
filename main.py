"""Консольный интерфейс для проверки и поиска СНИЛС."""

from pathlib import Path

from snils import find_snils, is_valid_snils


def search_in_file(path: Path) -> list[str]:
    """Прочитать UTF-8-файл и вернуть найденные записи."""
    # utf-8-sig поддерживает файлы и с BOM, и без него.
    return find_snils(path.read_text(encoding="utf-8-sig"))


def main() -> None:
    """Обработать одно действие, выбранное пользователем."""
    print("1 — проверить СНИЛС")
    print("2 — найти СНИЛС в текстовом файле")
    choice = input("Выберите действие: ").strip()

    if choice == "1":
        value = input("Введите СНИЛС: ")
        if is_valid_snils(value):
            print("Формат СНИЛС корректен.")
        else:
            print("Формат СНИЛС некорректен.")
    elif choice == "2":
        path = Path(input("Путь к файлу: ").strip().strip('"'))
        try:
            matches = search_in_file(path)
        except UnicodeDecodeError:
            print("Сохраните файл в кодировке UTF-8.")
            return
        except OSError as error:
            print(f"Не удалось прочитать файл: {error}")
            return

        if matches:
            print(f"Найдено совпадений: {len(matches)}")
            for match in matches:
                print(match)
        else:
            print("Совпадений не найдено.")
    else:
        print("Введите 1 или 2.")


if __name__ == "__main__":
    main()