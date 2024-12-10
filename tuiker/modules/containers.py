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
        table.add_columns("Name", "Status", "Ports", "Volumes", "Image", "Uptime")
        running_containers = get_containers(status="running")
        table.add_rows(
            [self._get_container_row(container) for container in running_containers]
        )

    def _get_container_row(self, container):
        """Format container details for the table row."""
        return (
            container.name,
            container.status,
            self._format_ports(container.attrs["NetworkSettings"]["Ports"]),
            self._format_volumes(container.attrs["Mounts"]),
            container.image.tags[0] if container.image.tags else "N/A",
            self._format_uptime(container.attrs["State"]["StartedAt"]),
        )

    def _format_ports(self, ports):
        """Format the container ports."""
        return ", ".join(
            f"{host['HostPort']}->{port}"
            for port, mappings in ports.items()
            for host in mappings or []
        )

    # def _format_volumes(self, mounts):
    #     """Format the container volumes."""
    #     return ", ".join(mount["Source"] for mount in mounts)
    #
    def _format_volumes(self, mounts: list) -> str:
        """Filter and format volumes that are host mount points."""
        return (
            ", ".join(
                f"{mount['Source']}:{mount['Destination']}"
                for mount in mounts
                if mount.get("Type") == "bind"  # Check if it's a host mount point
            )
            or "None"
        )

    def _format_uptime(self, started_at):
        """Calculate and format the container uptime."""
        from datetime import datetime, timezone

        started_time = datetime.fromisoformat(started_at.replace("Z", "+00:00"))
        uptime = datetime.now(timezone.utc) - started_time
        return str(uptime).split(".")[0]  # Strip microseconds


class ExitedContainersWidget(BaseContainersWidget):
    BORDER_TITLE = "Exited Containers"

    def compose(self):
        yield DataTable(header_height=2, cursor_type="row")

    def on_mount(self):
        table = self.query_one(DataTable)
        table.add_columns("Name", "Status", "Ports", "Volumes", "Image", "Uptime")
        exited_containers = get_containers(status="exited")
        table.add_rows(
            [self._get_container_row(container) for container in exited_containers]
        )

    def _get_container_row(self, container):
        """Format container details for the table row."""
        return (
            container.name,
            container.status,
            "N/A",  # No ports for exited containers
            self._format_volumes(container.attrs["Mounts"]),
            container.image.tags[0] if container.image.tags else "N/A",
            "N/A",  # No uptime for exited containers
        )

    def _format_volumes(self, mounts):
        """Format the container volumes."""
        return ", ".join(mount["Source"] for mount in mounts)

