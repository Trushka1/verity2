import re

SNILS_FORMAT = r"[0-9]{3}-[0-9]{3}-[0-9]{3}[ -][0-9]{2}"
VALIDATION_PATTERN = re.compile(SNILS_FORMAT)
SEARCH_PATTERN = re.compile(rf"(?<!\w){SNILS_FORMAT}(?!\w)")

"Проверка формата всей строки"
def is_valid_snils(value: str) -> bool:
    return VALIDATION_PATTERN.fullmatch(value) is not None

def find_snils(text: str) -> list[str]:
    "Вернуть совпадения в порядке появления в тексте"
    return SEARCH_PATTERN.findall(text)



"Проверка формата СНИЛС и поиск номеров в тексте"