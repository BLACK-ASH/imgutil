# AGENTS.md

## Overview

Python CLI tool that removes image backgrounds in bulk using `rembg` (wraps U²-Net). Installable via pip with a `remove-bg` entry point.

## Install

```bash
pip install -e .
```

This installs the `remove-bg` CLI command and all dependencies (`rembg`, `Pillow`, `click`).

## Usage

```bash
remove-bg <input_folder> <output_folder>
```

Processes all images (jpg, jpeg, png, webp, bmp, tiff) in the input folder and writes results to the output folder. Output format defaults to PNG; override with `-f webp` etc.

```bash
remove-bg photos/ processed/ -f webp
```

## Project Structure

- `remove_bg/cli.py` — CLI entry point (`main()` click command) and core `process_image()` logic
- `remove_bg/__init__.py` — package version
- `pyproject.toml` — build config and `[project.scripts]` entry point

## Conventions

- `.gitignore` contains `.remove` (rembg cache directory).
- No linting, formatting, or type-checking is configured.
- No tests exist.
- First run downloads a PyTorch model (~170 MB) into `.remove/`.
