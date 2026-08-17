# imgutil

Multi-utility image processing CLI tool.

## Install

```bash
pip install -e .
```

## Commands

| Command | Description |
|---------|-------------|
| `imgutil remove` | Remove backgrounds (U²-Net) |
| `imgutil upscale` | Upscale images (2x/4x) |
| `imgutil deblur` | Deblur/denoise (adjustable strength) |
| `imgutil enhance` | Sharpen + denoise (same dimensions) |

### Background Removal

```bash
imgutil remove photos/ processed/ -f webp
```

| Flag | Description |
|------|-------------|
| `-f`, `--format` | Output format: `png` (default), `webp`, etc. |

### Upscale

```bash
imgutil upscale photos/ upscaled/ -s 4
```

| Flag | Description |
|------|-------------|
| `-s`, `--scale` | Upscale factor: `2` or `4` (default: 4) |

### Deblur

```bash
imgutil deblur blurry/ fixed/ -s 0.8
```

| Flag | Description |
|------|-------------|
| `-s`, `--strength` | Denoise strength 0.0-1.0 (default: 0.7) |

### Enhance

```bash
imgutil enhance photos/ enhanced/
```

Sharpen and denoise without changing dimensions.

### Backward Compatibility

```bash
remove-bg photos/ processed/   # same as imgutil remove
```

## Supported Input Formats

`.jpg`, `.jpeg`, `.png`, `.webp`, `.bmp`, `.tiff`, `.tif`

## Notes

- Output folder is created automatically.
- First run downloads models: ~1 GB for rembg, ~65-100 MB each for Real-ESRGAN models.
- All models are cached for subsequent runs.
