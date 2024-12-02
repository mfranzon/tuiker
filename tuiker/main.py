import docker
from typing import Optional
from textual.app import App, ComposeResult
from textual.containers import Vertical, Horizontal, VerticalScroll
from textual.widgets import Button, Label, ContentSwitcher, Static, Input, Header
from textual.screen import Screen


class LogsTab(VerticalScroll):
    """Tab to display container logs."""

    def __init__(self, logs: str, id: Optional[str] = None) -> None:
        super().__init__(id=id)
        self.logs = logs

    def compose(self) -> ComposeResult:
        yield Label("Logs:")
        yield Static(self.logs, id="logs-content")


class ResourcesTab(VerticalScroll):
    """Tab to display container resource usage."""

    def __init__(self, resources: str, id: Optional[str] = None) -> None:
        super().__init__(id=id)
        self.resources = resources

    def compose(self) -> ComposeResult:
        yield Label("Resources:")
        yield VerticalScroll(Static(self.resources, id="resources-content"))


class ShellTab(Vertical):
    """Tab to provide shell access."""

    def __init__(
        self,
        container_name: str,
        docker_client: docker.DockerClient,
        id: Optional[str] = None,
    ) -> None:
        super().__init__(id=id)
        self.container_name = container_name
        self.docker_client = docker_client
        self.output = ""

    def compose(self) -> ComposeResult:
        yield Label(f"Shell into: {self.container_name}")
        yield Input(placeholder="Enter command here", id="command-input")
        yield Button("Execute", id="execute-button")
        yield VerticalScroll(Static(self.output, id="shell-output", expand=True))

    def execute_command(self, command: str) -> str:
        """Execute a command in the container and return the output."""
        try:
            container = self.docker_client.containers.get(self.container_name)
            result = container.exec_run(command, stdout=True, stderr=True)
            return result.output.decode("utf-8")
        except Exception as e:
            return f"Error executing command: {str(e)}"

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press events."""
        if event.button.id == "execute-button":
            input_box = self.query_one("#command-input", Input)
            command = input_box.value.strip()
            if command:
                output = self.execute_command(command)
                self.output += f"$ {command}\n{output}\n"
                output_box = self.query_one("#shell-output", Static)
                output_box.update(self.output)


class ContainerDetailsScreen(Screen):
    """A screen to display multiple tabs for a container's details."""

    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]

    def __init__(
        self,
        container_name: str,
        logs: str,
        resources: str,
        docker_client: docker.DockerClient,
    ) -> None:
        super().__init__()
        self.container_name = container_name
        self.logs = logs
        self.resources = resources
        self.docker_client = docker_client

    def compose(self) -> ComposeResult:
        yield Vertical(
            Label(f"Details for container: {self.container_name}", id="header"),
            ContentSwitcher(
                LogsTab(self.logs, id="logs-tab"),
                ResourcesTab(self.resources, id="resources-tab"),
                ShellTab(self.container_name, self.docker_client, id="shell-tab"),
                id="content-switcher",
            ),
            Horizontal(
                Button("Logs", id="logs-button"),
                Button("Resources", id="resources-button"),
                Button("Shell", id="shell-button"),
            ),
            Button("Go Back", id="back-button"),
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle tab switching and back navigation."""
        if event.button.id == "back-button":
            self.app.pop_screen()
        else:
            # Map button IDs to ContentSwitcher IDs
            tab_map = {
                "logs-button": "logs-tab",
                "resources-button": "resources-tab",
                "shell-button": "shell-tab",
            }
            if event.button.id in tab_map:
                switcher = self.query_one("#content-switcher", ContentSwitcher)
                switcher.current = tab_map[event.button.id]


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
            resources = f"CPU Usage: 10%\nMemory Usage: 256MB\nPorts: {container.attrs['NetworkSettings']['Ports']}"
            self.push_screen(
                ContainerDetailsScreen(
                    container.name, logs, resources, self.docker_client
                )
            )
        except Exception as e:
            print(f"Error fetching details for container {button_id}: {e}")


if __name__ == "__main__":
    app = DockerContainerApp()
    app.run()

