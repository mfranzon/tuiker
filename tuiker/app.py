from textual.app import App, ComposeResult
from textual.containers import Container, VerticalGroup
from textual.widgets import Footer, DataTable
from tuiker.modules.containers import RunningContainersWidget, ExitedContainersWidget
from tuiker.modules.logs import ContainerLogsWidget
from tuiker.modules.commands import ContainerCommandsWidget
from tuiker.utils.docker_utils import stop_container, remove_container, get_containers


class DockerApp(App):
    """Main Application for Docker Management"""

    CSS_PATH = "static/styles.tcss"

    BINDINGS = [
        ("ctrl+r", "refresh()", "Refresh Containers"),
        ("ctrl+s", "stop_container()", "Stop Selected Container"),
        ("ctrl+x", "remove_all_exited()", "Remove Exited Container"),
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

    def action_stop_container(self) -> None:
        """Stop the selected container"""
        table = self.query_one(DataTable)
        if table.cursor_row is not None:
            try:
                selected_row = table.get_row_at(table.cursor_row)
                container_name = selected_row[
                    0
                ]  # Assuming the first column is the container name
                stop_container(container_name)
                self.refresh(recompose=True)
            except Exception:
                self.refresh(recompose=True)

    def action_remove_all_exited(self) -> None:
        """Remove all exited containers."""
        containers = get_containers()
        exited_containers = [c.name for c in containers if c.status == "exited"]

        for container_name in exited_containers:
            remove_container(container_name)

        self.refresh(recompose=True)  # Refresh tables after removal
        self.log(f"Removed all exited containers: {', '.join(exited_containers)}")


def main():
    app = DockerApp()
    app.run()


if __name__ == "__main__":
    DockerApp().run()
