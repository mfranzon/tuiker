from textual.containers import VerticalScroll
from textual.widgets import Input, Button, RichLog
from tuiker.utils.docker_utils import execute_command


class ContainerCommandsWidget(VerticalScroll):
    BORDER_TITLE = "Container Commands"

    def compose(self):
        yield Input(placeholder="Container Name", id="container-name")
        yield Input(placeholder="Command to execute", id="command")
        yield Button("Execute", id="execute-button")
        yield RichLog(wrap=True)

    def on_button_pressed(self, message):
        if message.button.id == "execute-button":
            container_name = self.query_one("#container-name", Input).value.strip()
            command = self.query_one("#command", Input).value.strip()
            if container_name and command:
                output = execute_command(container_name, command)
                self.query_one(RichLog).write(f"$ {command}\n{output}\n")
            else:
                self.query_one(RichLog).write(
                    "Error: Please provide container name and command."
                )
