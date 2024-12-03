import argparse


class DependencyVisualizer:
    def __init__(self, graphviz_path, package_name, output_file, max_depth, repository_url):
        self.graphviz_path = graphviz_path
        self.package_name = package_name
        self.output_file = output_file
        self.max_depth = max_depth
        self.repository_url = repository_url.rstrip('/')
        self.dependencies = {}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("graphviz")
    parser.add_argument("package")
    parser.add_argument("output")
    parser.add_argument("max_depth", type=int)
    parser.add_argument("repository")
    args = parser.parse_args()

    visualizer = DependencyVisualizer(args.graphviz, args.package, args.output, args.max_depth, args.repository)


if __name__ == "__main__":
    main()
