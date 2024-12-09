import unittest
from unittest.mock import patch, Mock
from main import DependencyVisualizer


class TestDependencyVisualizer(unittest.TestCase):
    def setUp(self):
        self.graphviz_path = "/graphviz/dot"
        self.package_name = "test-package"
        self.output_file = "output.dot"
        self.max_depth = 2
        self.repository_url = "https://repository.com/npm"
        self.visualizer = DependencyVisualizer(self.graphviz_path, self.package_name, self.output_file, self.max_depth, self.repository_url)

    @patch("main.requests.get")
    def test_fetch_package_json_success(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "dist-tags": {"latest": "1.0.0"},
            "versions": {"1.0.0": {"dependencies": {"dep1": "1.0.0"}}},
        }
        mock_get.return_value = mock_response
        package_json = self.visualizer.fetch_package_json(self.package_name)
        self.assertEqual(package_json, {"dependencies": {"dep1": "1.0.0"}})
        mock_get.assert_called_once_with(f"{self.repository_url}/{self.package_name}")

    @patch("main.requests.get")
    def test_fetch_package_json_failure(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        package_json = self.visualizer.fetch_package_json(self.package_name)
        self.assertIsNone(package_json)
        mock_get.assert_called_once_with(f"{self.repository_url}/{self.package_name}")

    @patch("main.DependencyVisualizer.fetch_package_json")
    def test_fetch_dependencies(self, mock_fetch_package_json):
        def mock_fetch(pkg):
            packages = {
                "test-package": {"dependencies": {"dep1": "1.0.0"}},
                "dep1": {"dependencies": {"dep2": "1.0.0"}},
                "dep2": {"dependencies": {}},
            }
            return packages.get(pkg)

        mock_fetch_package_json.side_effect = mock_fetch
        self.visualizer.fetch_dependencies("test-package")
        expected_dependencies = {
            "test-package": {"dep1": "1.0.0"},
            "dep1": {"dep2": "1.0.0"},
            "dep2": {},
        }
        self.assertEqual(self.visualizer.dependencies, expected_dependencies)

    @patch("main.DependencyVisualizer.fetch_package_json")
    def test_fetch_dependencies_max_depth(self, mock_fetch_package_json):
        self.visualizer.max_depth = 2

        def mock_fetch(package_name):
            packages = {
                "test-package": {"dependencies": {"dep1": "1.0.0"}},
                "dep1": {"dependencies": {"dep2": "1.0.0"}},
                "dep2": {"dependencies": {"dep3": "1.0.0"}},
                "dep3": {"dependencies": {}},
            }
            return packages.get(package_name, {"dependencies": {}})

        mock_fetch_package_json.side_effect = mock_fetch
        self.visualizer.fetch_dependencies("test-package")
        expected_dependencies = {
            "test-package": {"dep1": "1.0.0"},
            "dep1": {"dep2": "1.0.0"},
            "dep2": {"dep3": "1.0.0"},
        }
        self.assertEqual(self.visualizer.dependencies, expected_dependencies)

    def test_generate_dot_code(self):
        self.visualizer.dependencies = {
            "test-package": {"dep1": "1.0.0", "dep2": "1.0.0"},
            "dep1": {"dep3": "1.0.0"},
            "dep2": {},
            "dep3": {},
        }
        dot_code = self.visualizer.generate_dot_code()
        expected_dot_code = """digraph G {
  "test-package" -> "dep1";
  "test-package" -> "dep2";
  "dep1" -> "dep3";
}"""
        self.assertEqual(dot_code.strip(), expected_dot_code.strip())


if __name__ == "__main__":
    unittest.main()
