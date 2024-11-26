import yaml
import argparse
import re


class ConfigParser:
    def __init__(self, input_file):
        self.input_file = input_file
        self.constants = {}

    def read_input_file(self):
        with open(self.input_file, 'r') as file:
            for line in file:
                self.process_line(line.strip())

    def process_line(self, line):
        if line.startswith('!'):
            pass
        elif line.startswith('def '):
            self.process_def(line)

    def process_def(self, line):
        initialization = line[4:]
        if initialization.count('=') == 1:
            name, value = initialization.split("=")
            name = name.strip()
            value = value.strip()
            if re.fullmatch(r'[A-Z]+', name):
                value = self.get_value(value)
                if value is None:
                    print(f'Ошибка: {line}. Константа задана некорректно')
                else:
                    self.constants[name] = value
            else:
                print(f'Ошибка: {line}. Некорректное имя константы')
        elif initialization.count('=') > 1:
            print(f'Ошибка: {line}. Несколько знаков =')
        else:
            print(f'Ошибка: {line}. Нет инициализации')

    def is_number(self, value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    def get_value(self, value):
        if value.startswith('[') and value.endswith(']'):
            return self.process_arr(value[1:-1])
        if value.startswith('q(') and value.endswith(')'):
            return value[2:-1]
        elif value.startswith('@{') and value.endswith('}'):
            if value[2:-1] in self.constants:
                return self.constants[value[2:-1]]
        elif self.is_number(value):
            value = float(value)
            if value.is_integer():
                return int(value)
            else:
                return value
        else:
            return None

    def process_arr(self, value):
        elements = []
        buffer = ""
        nested_level = 0

        for char in value:
            if char == ';' and nested_level == 0:
                elements.append(self.get_value(buffer.strip()))
                buffer = ""
            else:
                if char == '[':
                    nested_level += 1
                elif char == ']':
                    nested_level -= 1
                buffer += char

        if buffer:
            elements.append(self.get_value(buffer.strip()))
        return elements

    def print_yaml(self):
        yaml_data = yaml.dump(self.constants)
        print(yaml_data)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file')
    args = parser.parse_args()
    config_parser = ConfigParser(args.input_file)
    config_parser.read_input_file()
    config_parser.print_yaml()


if __name__ == "__main__":
    main()
