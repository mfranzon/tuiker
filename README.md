# Tuiker: A Docker TUI Application

**Tuiker** is a Terminal User Interface (TUI) application for managing Docker containers. It allows users to view logs, monitor resource usage, and interact with running containers through a shell—all within an intuitive terminal-based interface.

## Features

- **View Docker Container Logs**  
  Access live logs for running containers.

- **Monitor Resource Usage**  
  View details about CPU, GPU, volumes, and port usage.

- **Interactive Shell**  
  Execute shell commands directly inside the container.

- **Keyboard Navigation**  
  Navigate the UI using arrow keys and shortcuts.

## Requirements

- Python 3.12 or later
- Docker Engine installed and running
- Poetry for dependency management

## Installation

1. Clone the repository:

```bash
   git clone https://github.com/yourusername/tuiker.git
   cd tuiker
```
## Install dependencies using Poetry

```bash
poetry install
```

## Usage

Run the following command to start the app:

```bash
poetry run tuiker
```

# Contributing
1. Fork the repository.

2. Create a feature branch:

```bash
git checkout -b feature/your-feature
```

3, Commit your changes:

```bash
git commit -m 'Add a new feature'
```
4. Push to the branch:

```bash
git push origin feature/your-feature
```

5. Open a pull request.
