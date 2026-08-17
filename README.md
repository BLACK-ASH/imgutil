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

Global options: `-h` (help), `-v` (version)

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

## Use Cases

| Task | Best command | Example |
|------|-------------|---------|
| E-commerce product photos | `remove` | Clean white background |
| Old/low-res photos | `upscale` | Restore detail for printing |
| Blurry phone photos | `deblur` | Fix motion blur, missed focus |
| Dark/grainy photos | `enhance` | Improve without changing size |

## Limitations

- **No GPU = slow**: CPU inference takes ~3-5 min/image for upscale/deblur/enhance. A GPU drops this to seconds.
- **No batch size control**: Processes one image at a time sequentially.
- **Fixed tile size**: Tiling (400px) prevents GPU OOM but may produce visible seams on very large images.
- **Model downloads on first run**: ~1 GB for rembg, ~65-100 MB each for Real-ESRGAN models. Requires internet on first use.
- **No recursive folder processing**: Only processes images in the top-level input folder, not subfolders.
- **No image preview/compare**: Results are written to disk only.

## Notes

- Output folder is created automatically.
- All models are cached after first download.
- Progress bar shown during processing (tqdm).
