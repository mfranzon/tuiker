from textual.containers import Vertical, VerticalScroll
from textual.widgets import Label, Input, Button, Static


class ShellTab(Vertical):
    """Tab to provide shell access."""

    def __init__(self, container_name, docker_client, id=None):
        super().__init__(id=id)
        self.container_name = container_name
        self.docker_client = docker_client
        self.output = ""

    def compose(self):
        yield Label(f"Shell into: {self.container_name}")
        yield Input(placeholder="Enter command here", id="command-input")
        yield Button("Execute", id="execute-button")
        yield VerticalScroll(Static(self.output, id="shell-output", expand=True))

    def execute_command(self, command):
        try:
            container = self.docker_client.containers.get(self.container_name)
            result = container.exec_run(command, stdout=True, stderr=True)
            return result.output.decode("utf-8")
        except Exception as e:
            return f"Error executing command: {str(e)}"

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "execute-button":
            input_box = self.query_one("#command-input", Input)
            command = input_box.value.strip()
            if command:
                output = self.execute_command(command)
                self.output += f"$ {command}\n{output}\n"
                output_box = self.query_one("#shell-output", Static)
                output_box.update(self.output)
