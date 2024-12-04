from textual.containers import VerticalScroll
from textual.widgets import Label, Static


class ResourcesTab(VerticalScroll):
    """Tab to display container resource usage."""

    def __init__(self, resources, id=None):
        super().__init__(id=id)
        self.resources = resources

    def compose(self):
        yield Label("Resources:")
        yield VerticalScroll(Static(self.resources, id="resources-content"))
