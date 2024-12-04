from textual.containers import VerticalScroll
from textual.widgets import Label, Static


class LogsTab(VerticalScroll):
    """Tab to display container logs."""

    def __init__(self, logs, id=None):
        super().__init__(id=id)
        self.logs = logs

    def compose(self):
        yield Label("Logs:")
        yield Static(self.logs, id="logs-content")
