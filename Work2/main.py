import argparse
import requests


class DependencyVisualizer:
    def __init__(self, graphviz_path, package_name, output_file, max_depth, repository_url):
        self.graphviz_path = graphviz_path
        self.package_name = package_name
        self.output_file = output_file
        self.max_depth = max_depth
        self.repository_url = repository_url.rstrip('/')
        self.dependencies = {}

    def fetch_package_json(self, package_name):
        url = f"{self.repository_url}/{package_name}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if "versions" in data:
                latest_version = data["dist-tags"]["latest"]
                return data["versions"][latest_version]
        return None


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
