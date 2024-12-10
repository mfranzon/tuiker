from textual.app import App, ComposeResult
from textual.containers import Container, VerticalGroup
from textual.widgets import Footer
from tuiker.modules.containers import RunningContainersWidget, ExitedContainersWidget
from tuiker.modules.logs import ContainerLogsWidget
from tuiker.modules.commands import ContainerCommandsWidget


class DockerApp(App):
    """Main Application for Docker Management"""

    CSS_PATH = "static/styles.tcss"

    BINDINGS = [
        ("ctrl+r", "refresh()", "Refresh Containers"),
    ]

    def compose(self) -> ComposeResult:
        yield Container(
            VerticalGroup(RunningContainersWidget(), id="running"),
            VerticalGroup(ExitedContainersWidget(), id="exited"),
            VerticalGroup(ContainerLogsWidget(), id="logs"),
            VerticalGroup(ContainerCommandsWidget(), id="commands"),
        )
        yield Footer()

    def action_refresh(self) -> None:
        """Refresh the app."""
        self.refresh(recompose=True)


def main():
    app = DockerApp()
    app.run()


if __name__ == "__main__":
    DockerApp().run()

