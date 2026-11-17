"Тесты регулярного выражения для СНИЛС"

import unittest

from snils import find_snils, is_valid_snils


class SnilsTest(unittest.TestCase):
    def test_valid_formats(self):
        for value in ("000-000-000 01", "000-000-000-02"):
            with self.subTest(value=value):
                self.assertTrue(is_valid_snils(value))

    def test_invalid_formats(self):
        values = (
            "",
            "00000000001",
            "00-000-000 01",
            "000-000-000 1",
            "000-000-000 001",
            "000 000 000 01",
            "000/000/000 01",
            "000-000-000  01",
            "000-000-000\t01",
            "000-000-000\n01",
            "000-000-000\u00a001",
            "000–000–000 01",
            "０００-000-000 01",
            "000-000-000 О1",
            " 000-000-000 01",
            "000-000-000 01\n",
            "СНИЛС: 000-000-000 01",
        )
        for value in values:
            with self.subTest(value=value):
                self.assertFalse(is_valid_snils(value))

    def test_search_preserves_order_and_repetitions(self):
        text = "Начало: (000-000-000-02),\n000-000-000 01; 000-000-000-02"
        self.assertEqual(
            find_snils(text),
            ["000-000-000-02", "000-000-000 01", "000-000-000-02"],
        )

    def test_search_at_text_boundaries(self):
        self.assertEqual(find_snils("000-000-000 01"), ["000-000-000 01"])

    def test_search_rejects_parts_of_words_and_numbers(self):
        for text in (
            "А000-000-000 01",
            "000-000-000 01Б",
            "1000-000-000 01",
            "000-000-000 012",
            "_000-000-000-02",
            "000-000-000-02_",
            "000-000-000\t01",
            "000-000-000\n01",
        ):
            with self.subTest(text=text):
                self.assertEqual(find_snils(text), [])

    def test_search_returns_empty_list(self):
        for text in ("", "В этом тексте нет номеров"):
            with self.subTest(text=text):
                self.assertEqual(find_snils(text), [])