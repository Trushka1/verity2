import re

SNILS_FORMAT = r"[0-9]{3}-[0-9]{3}-[0-9]{3}[ -][0-9]{2}"
VALIDATION_PATTERN = re.compile(SNILS_FORMAT)

"Проверка формата всей строки"
def is_valid_snils(value: str) -> bool:
    return VALIDATION_PATTERN.fullmatch(value) is not None



"Проверка формата СНИЛС"