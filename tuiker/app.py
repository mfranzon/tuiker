import docker
from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.widgets import Header, Label, Button
from tuiker.screens.container_details_screen import ContainerDetailsScreen


class DockerContainerApp(App):
    """The main application to display running Docker containers."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.docker_client = docker.from_env()

    def compose(self) -> ComposeResult:
        """Create the main user interface."""
        yield Header()
        if not self.docker_client.containers.list():
            yield Label("No running Docker containers found.")
        else:
            yield Vertical(
                Label("Click on a container to view its details:"),
                *[
                    Button(f"{container.name} - {container.status}", id=container.name)
                    for container in self.docker_client.containers.list()
                ],
            )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button clicks."""
        button_id = event.button.id
        try:
            container = self.docker_client.containers.get(button_id)
            logs = container.logs().decode("utf-8")
            resources = (
                f"CPU Usage: 10%\nMemory Usage: 256MB\nPorts: "
                f"{container.attrs['NetworkSettings']['Ports']}"
            )
            self.push_screen(
                ContainerDetailsScreen(
                    container.name, logs, resources, self.docker_client
                )
            )
        except Exception as e:
            print(f"Error fetching details for container {button_id}: {e}")


def main():
    """Entry point for the application."""
    app = DockerContainerApp()
    app.run()


if __name__ == "__main__":
    main()
