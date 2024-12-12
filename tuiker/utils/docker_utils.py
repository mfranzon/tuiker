import docker

client = docker.from_env()


def get_container_logs(container_name: str) -> str:
    """Fetch logs for a specific container."""
    try:
        container = client.containers.get(container_name)
        return container.logs(tail=100).decode(
            "utf-8"
        )  # Get the last 100 lines of logs
    except Exception as e:
        return f"Error fetching logs: {e}"


def get_docker_client():
    """Get a Docker client instance."""
    return docker.from_env()


def get_containers(status=None):
    """Retrieve containers by status."""
    client = get_docker_client()
    if status:
        return [c for c in client.containers.list(all=True) if c.status == status]
    return client.containers.list(all=True)


def execute_command(container_name, command):
    """Execute a command inside a container."""
    client = get_docker_client()
    try:
        container = client.containers.get(container_name)
        result = container.exec_run(command, stdout=True, stderr=True)
        return result.output.decode("utf-8")
    except Exception as e:
        return f"Error executing command: {str(e)}"


def stop_container(container_name: str) -> None:
    """Stop a container by name."""
    try:
        container = client.containers.get(container_name)
        container.stop()
        print(f"Container {container_name} stopped successfully.")
    except Exception as e:
        print(f"Error stopping container {container_name}: {e}")


def remove_container(container_name: str) -> None:
    """Remove a container by name."""
    try:
        container = client.containers.get(container_name)
        container.remove()
        print(f"Container {container_name} removed successfully.")
    except Exception as e:
        print(f"Error removing container {container_name}: {e}")
