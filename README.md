# 🐍 Snake Game (Curses-based) <!-- omit in toc -->

A classic Snake game implemented in **Python** using the `curses` library.
Supports **colors, keyboard controls (WASD/Arrow keys), scoring, restart, and game-over screen**.

## Table of Contents <!-- omit in toc -->

- [Installation](#installation)
- [Usage](#usage)
- [Development Notes](#development-notes)

---

## Installation

-   From PyPi

    ```bash
    pip install snakify
    ```

-   From Source :

    ```bash
    git clone https://github.com/bhatishan2003/snakify.git
    cd snakify
    pip install .
    ```

## Usage

Run the following command in the terminal to play the game.

```bash
snakify
```

![Snake Game Demo](assets/demo.gif)

## Development Notes

-   For development (editable mode), do following installation:

    ```bash
    pip install -e .
    ```

-   Pre-commit

    We use pre-commit to automate linting of our codebase.

    -   Install hooks:
        ```bash
        pre-commit install
        ```
    -   Run Hooks manually (optional):
        ```bash
        pre-commit run --all-files
        ```

-   Ruff:

    -   Lint and format:
        ```bash
        ruff check --fix
        ruff format
        ```
