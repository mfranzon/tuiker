from textual.widgets import Tree, DataTable
import yaml
import os


class DockerComposeTreeWidget(Tree):
    """Widget to display a tree of folders and select a `docker-compose.yaml` file."""

    def __init__(self) -> None:
        super().__init__(label="File System")

    def on_mount(self) -> None:
        self.root.label = ".."
        self.root.expand()
        self.build_tree(os.getcwd(), self.root)

    def build_tree(self, directory: str, parent) -> None:
        """Recursively build a tree of folders and files."""
        try:
            for entry in os.scandir(directory):
                if entry.is_dir():
                    dir_node = parent.add(
                        entry.name
                    )  # Removed the 'parent' keyword argument
                    self.build_tree(entry.path, dir_node)
                elif entry.is_file() and entry.name == "docker-compose.yaml":
                    parent.add(
                        entry.name, data=entry.path
                    )  # Add file directly with data
        except PermissionError:
            pass

    def on_tree_node_selected(self, message: Tree.NodeSelected) -> None:
        """Handle selection of a docker-compose.yaml file."""
        if message.node.data:
            self.app.query_one("#compose_services").update_services(message.node.data)


class DockerComposeServicesWidget(DataTable):
    """Widget to display services in the selected docker-compose.yaml."""

    def on_mount(self) -> None:
        self.add_columns("Service Name", "Image", "Ports", "Volumes")

    def update_services(self, compose_file: str) -> None:
        """Parse the docker-compose file and update the services table."""
        self.clear()
        try:
            with open(compose_file, "r") as file:
                compose_data = yaml.safe_load(file)
                services = compose_data.get("services", {})
                for service_name, attributes in services.items():
                    ports = ", ".join(attributes.get("ports", []))
                    volumes = ", ".join(attributes.get("volumes", []))
                    image = attributes.get("image", "N/A")
                    self.add_row(service_name, image, ports, volumes)
        except Exception as e:
            self.app.log(f"Error loading compose file: {e}")
