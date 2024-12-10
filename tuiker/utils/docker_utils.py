import docker


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
