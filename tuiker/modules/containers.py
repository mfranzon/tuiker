from textual.containers import VerticalScroll
from textual.widgets import DataTable
from tuiker.utils.docker_utils import get_containers


class BaseContainersWidget(VerticalScroll):
    """Base class for container widgets to enable shared behavior."""

    def on_data_table_row_selected(self, message: DataTable.RowSelected):
        """Handle selection of a container row."""
        container_name = message.data_table.get_row_at(message.cursor_row)[0]
        logs_widget = self.app.query_one("ContainerLogsWidget")
        logs_widget.display_logs(container_name)


class RunningContainersWidget(BaseContainersWidget):
    BORDER_TITLE = "Running Containers"

    def compose(self):
        yield DataTable(header_height=2, cursor_type="row")

    def on_mount(self):
        table = self.query_one(DataTable)
        table.add_columns("Name", "Status")
        running_containers = get_containers(status="running")
        table.add_rows([(c.name, c.status) for c in running_containers])


class ExitedContainersWidget(BaseContainersWidget):
    BORDER_TITLE = "Exited Containers"

    def compose(self):
        yield DataTable(header_height=2, cursor_type="row")

    def on_mount(self):
        table = self.query_one(DataTable)
        table.add_columns("Name", "Status")
        exited_containers = get_containers(status="exited")
        table.add_rows([(c.name, c.status) for c in exited_containers])

