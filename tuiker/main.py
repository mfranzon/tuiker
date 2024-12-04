from app import DockerContainerApp


def main():
    """Entry point for the application."""
    app = DockerContainerApp()
    app.run()


if __name__ == "__main__":
    main()
