from textual.containers import VerticalScroll
from textual.widgets import RichLog
from tuiker.utils.docker_utils import get_docker_client


class ContainerLogsWidget(VerticalScroll):
    BORDER_TITLE = "Container Logs"

    def compose(self):
        yield RichLog(wrap=True, id="log-view")

    def display_logs(self, container_name):
        """Fetch and display logs for the selected container."""
        log_view = self.query_one("#log-view", RichLog)
        log_view.clear()
        try:
            client = get_docker_client()
            container = client.containers.get(container_name)
            logs = container.logs(tail=50).decode("utf-8")  # Show the last 50 lines
            log_view.write(logs)
        except Exception as e:
            log_view.write(f"Error fetching logs: {e}")

