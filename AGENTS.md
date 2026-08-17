# AGENTS.md

## Overview

Python CLI multi-utility image tool. Four subcommands: background removal (rembg), upscaling, deblurring, and enhancement (Real-ESRGAN). Installable via pip with `imgutil` and `remove-bg` entry points.

## Install

```bash
pip install -e .
```

This installs `imgutil` (all commands) and `remove-bg` (alias for background removal). A `.venv/` exists at the repo root — use it.

## Usage

```bash
imgutil <subcommand> <input_folder> <output_folder> [options]
```

### Subcommands

| Command | What it does | Key options |
|---------|-------------|-------------|
| `remove` | Remove backgrounds (U²-Net) | `-f webp` (output format) |
| `upscale` | Upscale images | `-s 2` or `-s 4` (default: 4) |
| `deblur` | Deblur/denoise | `-s 0.7` (strength 0.0-1.0) |
| `enhance` | Sharpen + denoise (same dimensions) | — |

### Examples

```bash
imgutil remove photos/ processed/ -f webp
imgutil upscale photos/ upscaled/ -s 4
imgutil deblur blurry/ fixed/ -s 0.8
imgutil enhance photos/ enhanced/

# Backward-compatible alias (same as imgutil remove)
remove-bg photos/ processed/
```

## Project Structure

- `imgutil/cli.py` — Click group with subcommand registration
- `imgutil/remove.py` — Background removal logic + `remove-bg` entry point
- `imgutil/upscale.py` — Real-ESRGAN upscaling (2x/4x)
- `imgutil/deblur.py` — Real-ESRGAN deblur using DNI blend
- `imgutil/enhance.py` — Real-ESRGAN 1x enhancement (4x inference + downscale)
- `imgutil/utils.py` — Shared image I/O (PIL and OpenCV)
- `pyproject.toml` — Build config and entry points

## Conventions

- `.gitignore` contains `.remove` (legacy rembg cache directory).
- No linting, formatting, or type-checking is configured.
- No tests exist.
- First run downloads models into `~/.rembg/models/` (~1 GB for rembg, ~65-100 MB each for Real-ESRGAN).
- All Real-ESRGAN operations use OpenCV (BGR numpy arrays) internally, with PIL used only for rembg output.
- Tiling (`tile=400`) is enabled by default to avoid GPU OOM on large images.
- `__init__.py` patches `torchvision.transforms.functional_tensor` for basicsr compatibility with torchvision >=0.17. Do not remove this shim.
