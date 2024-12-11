import unittest
from unittest.mock import patch, mock_open
from io import StringIO
from main import ConfigParser


class TestConfigParser(unittest.TestCase):
    def setUp(self):
        self.parser = ConfigParser("file")

    def test_server(self):
        self.parser.process_line("def HOST = q(127.0.0.1)")
        self.parser.process_line("def PORT = 8080")
        self.parser.process_line("def DEBUGMODE = 1")
        self.assertIn("HOST", self.parser.constants)
        self.assertIn("PORT", self.parser.constants)
        self.assertIn("DEBUGMODE", self.parser.constants)

    def test_robot(self):
        self.parser.process_line("def MAXSPEED = 1.5")
        self.parser.process_line("def ARMLENGTH = 1.2")
        self.assertIn("MAXSPEED", self.parser.constants)
        self.assertIn("ARMLENGTH", self.parser.constants)

    def test_finance(self):
        self.parser.process_line("def TAXRATE = 0.18")
        self.parser.process_line("def DISCOUNTRATE = 0.05")
        self.parser.process_line("def CURRENCY = q(USD)")
        self.assertIn("TAXRATE", self.parser.constants)
        self.assertIn("DISCOUNTRATE", self.parser.constants)
        self.assertIn("CURRENCY", self.parser.constants)

    @patch("builtins.open", new_callable=mock_open, read_data="def A = 42\ndef B = q(Hello)\n")
    def test_read_input_file(self, mock_file):
        self.parser.read_input_file()
        self.assertIn("A", self.parser.constants)
        self.assertIn("B", self.parser.constants)

    def test_process_line_comment(self):
        self.parser.process_line("! Comment")
        self.assertFalse(self.parser.error)

    def test_process_line_def(self):
        self.parser.process_line("def A = 123")
        self.assertIn("A", self.parser.constants)

    def test_process_line_final(self):
        self.parser.constants = {"A": 42}
        self.parser.process_line("[ @{A} ]")
        self.assertIn("A", self.parser.to_convert)

    def test_process_def_valid(self):
        self.parser.process_def("def A = 123")
        self.assertEqual(self.parser.constants["A"], 123)

    @patch("builtins.print")
    def test_process_def_invalid_name(self, mock_print):
        with patch("sys.stdout", new_callable=StringIO):
            self.parser.process_def("def a = 123")
        self.assertTrue(self.parser.error)

    @patch("builtins.print")
    def test_process_def_multiple_equals(self, mock_print):
        with patch("sys.stdout", new_callable=StringIO):
            self.parser.process_def("def A = 123 = 456")
        self.assertTrue(self.parser.error)

    def test_is_number(self):
        self.assertTrue(self.parser.is_number("123"))
        self.assertTrue(self.parser.is_number("123.45"))
        self.assertFalse(self.parser.is_number("abc"))

    def test_get_value_number(self):
        self.assertEqual(self.parser.get_value("123"), 123)
        self.assertEqual(self.parser.get_value("123.45"), 123.45)

    def test_get_value_array(self):
        result = self.parser.get_value("[123; 456]")
        self.assertEqual(result, [123, 456])

    def test_get_value_constant(self):
        self.parser.constants = {"A": 42}
        self.assertEqual(self.parser.get_value("@{A}"), 42)

    def test_get_value_invalid(self):
        self.assertIsNone(self.parser.get_value("invalid"))

    def test_process_arr_valid(self):
        result = self.parser.process_arr("123; 456; 789")
        self.assertEqual(result, [123, 456, 789])

    def test_process_arr_nested(self):
        result = self.parser.process_arr("[1; 2]; [3; 4]")
        self.assertEqual(result, [[1, 2], [3, 4]])

    def test_process_arr_invalid(self):
        result = self.parser.process_arr("123; invalid")
        self.assertIsNone(result)

    def test_process_arr_string_array(self):
        result = self.parser.process_arr("q(hello); q(world)")
        self.assertEqual(result, ["hello", "world"])

    @patch("builtins.print")
    def test_process_final_invalid(self, mock_print):
        with patch("sys.stdout", new_callable=StringIO):
            self.parser.process_final("invalid", "[ invalid ]")
        self.assertTrue(self.parser.error)

    @patch("yaml.dump")
    @patch("builtins.print")
    def test_print_yaml(self, mock_print, mock_yaml):
        self.parser.to_convert = {"A": 42}
        mock_yaml.return_value = "yaml_output"
        self.parser.print_yaml()
        mock_print.assert_called_once_with("yaml_output")


if __name__ == "__main__":
    unittest.main()
