# imgutil

Multi-utility image processing CLI tool.

## Install

```bash
pip install -e .
```

## Quick Start

```bash
imgutil remove photos/ processed/          # remove backgrounds
imgutil upscale photos/ upscaled/ -s 4     # 4x upscale
imgutil deblur blurry/ fixed/ -s 0.8       # fix blurry photos
imgutil enhance photos/ enhanced/          # improve quality
```

## Commands

| Command | Description | Key options |
|---------|-------------|-------------|
| `imgutil remove` | Remove backgrounds (U²-Net) | `-f webp` (output format) |
| `imgutil upscale` | Upscale images (2x/4x) | `-s 2` or `-s 4` |
| `imgutil deblur` | Deblur/denoise | `-s 0.7` (strength 0.0-1.0) |
| `imgutil enhance` | Sharpen + denoise (same dimensions) | — |

Global options: `-h` (help), `-v` (version)

**Backward compatible:** `remove-bg photos/ out/` works too.

## Documentation

- [**User Manual**](MANUAL.md) — Full usage guide, examples, troubleshooting

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
