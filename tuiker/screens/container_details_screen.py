from textual.screen import Screen
from textual.containers import Vertical, Horizontal
from textual.widgets import Label, Button, ContentSwitcher
from tuiker.tabs.logs_tab import LogsTab
from tuiker.tabs.resources_tab import ResourcesTab
from tuiker.tabs.shell_tab import ShellTab


class ContainerDetailsScreen(Screen):
    """A screen to display multiple tabs for a container's details."""

    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]

    def __init__(self, container_name, logs, resources, docker_client):
        super().__init__()
        self.container_name = container_name
        self.logs = logs
        self.resources = resources
        self.docker_client = docker_client

    def compose(self):
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
        if event.button.id == "back-button":
            self.app.pop_screen()
        else:
            tab_map = {
                "logs-button": "logs-tab",
                "resources-button": "resources-tab",
                "shell-button": "shell-tab",
            }
            if event.button.id in tab_map:
                switcher = self.query_one("#content-switcher", ContentSwitcher)
                switcher.current = tab_map[event.button.id]
