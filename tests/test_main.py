"Тесты чтения файлов и обработки действий в меню."

import io
import runpy
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from main import main, search_in_file


class MainTest(unittest.TestCase):
    def setUp(self):
        directory = TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.path = Path(directory.name) / "пример данных.txt"

    def run_menu(self, *answers):
        output = io.StringIO()
        with patch("builtins.input", side_effect=answers):
            with redirect_stdout(output):
                main()
        return output.getvalue()

    def test_search_in_utf8_file_with_bom(self):
        self.path.write_text("000-000-000 01\n", encoding="utf-8-sig")
        self.assertEqual(search_in_file(self.path), ["000-000-000 01"])

    def test_manual_valid_input(self):
        self.assertIn(
            "Формат СНИЛС корректен.",
            self.run_menu("1", "000-000-000 01"),
        )

    def test_manual_invalid_input(self):
        self.assertIn(
            "Формат СНИЛС некорректен.",
            self.run_menu("1", "000-000-000 1"),
        )

    def test_file_with_matches(self):
        self.path.write_text("СНИЛС: 000-000-000-02", encoding="utf-8")
        output = self.run_menu("2", f'"{self.path}"')
        self.assertIn("Найдено совпадений: 1", output)
        self.assertIn("000-000-000-02", output)

    def test_file_without_matches(self):
        self.path.write_text("Пустой список.", encoding="utf-8")
        self.assertIn(
            "Совпадений не найдено.",
            self.run_menu("2", str(self.path)),
        )

    def test_missing_file(self):
        self.assertIn(
            "Не удалось прочитать файл:",
            self.run_menu("2", str(self.path)),
        )

    def test_invalid_file_encoding(self):
        self.path.write_bytes(b"\xff")
        self.assertIn(
            "Сохраните файл в кодировке UTF-8.",
            self.run_menu("2", str(self.path)),
        )

    def test_unknown_menu_option(self):
        self.assertIn("Введите 1 или 2.", self.run_menu("9"))

    def test_script_entry_point(self):
        output = io.StringIO()
        with patch("builtins.input", side_effect=["1", "000-000-000-02"]):
            with redirect_stdout(output):
                runpy.run_module("main", run_name="__main__")
        self.assertIn("Формат СНИЛС корректен.", output.getvalue())