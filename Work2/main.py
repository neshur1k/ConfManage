import yaml
import argparse


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
            self.constants[name] = value
        elif initialization.count('=') > 1:
            print(f'Ошибка: {line}. Несколько знаков =')
        else:
            print(f'Ошибка: {line}. Нет инициализации')

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
