from textual.containers import VerticalScroll
from textual.widgets import RichLog
from textual.timer import Timer
from tuiker.utils.docker_utils import get_container_logs


class ContainerLogsWidget(VerticalScroll):
    """Widget to display and refresh logs for a selected container."""

    BORDER_TITLE = "Container Logs"

    def compose(self):
        yield RichLog(wrap=True)

    def on_mount(self):
        """Set up a timer for refreshing logs."""
        self.log_timer: Timer | None = None

    def display_logs(self, container_name: str):
        """Display logs for the selected container."""
        self.selected_container = container_name
        self.refresh_logs()  # Immediately fetch logs
        if self.log_timer:
            self.log_timer.stop()
        self.log_timer = self.set_interval(2, self.refresh_logs)

    def refresh_logs(self):
        """Fetch and display logs for the selected container."""
        if hasattr(self, "selected_container") and self.selected_container:
            logs = get_container_logs(self.selected_container)
            log_widget = self.query_one(RichLog)
            log_widget.clear()  # Clear old logs
            log_widget.write(logs)

    def stop_refresh(self):
        """Stop the log refresh timer."""
        if self.log_timer:
            self.log_timer.stop()

