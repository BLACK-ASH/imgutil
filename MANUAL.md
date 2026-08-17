# imgutil User Manual

## Quick Start

```bash
# Install
pip install -e .

# Check version
imgutil -v

# Get help
imgutil -h
imgutil <command> -h
```

## Commands

### `imgutil remove` — Remove Backgrounds

Removes the background from all images in a folder using U²-Net AI model.

```bash
# Basic usage — outputs PNG
imgutil remove photos/ processed/

# Output as WebP
imgutil remove photos/ processed/ -f webp

# Output as JPEG
imgutil remove photos/ processed/ -f jpg
```

**Options:**
| Flag | Description | Default |
|------|-------------|---------|
| `-f`, `--format` | Output format (`png`, `webp`, `jpg`, etc.) | `png` |

**What happens:**
- Input: Folder containing `.jpg`, `.jpeg`, `.png`, `.webp`, `.bmp`, `.tiff`, `.tif`
- Output: Same filenames with new extension, transparent background
- First run downloads ~1 GB model to `~/.rembg/models/`
- Processing time: ~5-10 sec/image (CPU), ~0.5 sec/image (GPU)

**Example output:**
```
Removing backgrounds: 100%|████████████████| 3/3 [00:15<00:00,  5.12s/img]
Done: 3/3 succeeded.
```

---

### `imgutil upscale` — Upscale Images

Increases image resolution using Real-ESRGAN super-resolution model.

```bash
# 4x upscale (default)
imgutil upscale photos/ upscaled/

# 2x upscale
imgutil upscale photos/ upscaled/ -s 2
```

**Options:**
| Flag | Description | Default |
|------|-------------|---------|
| `-s`, `--scale` | Upscale factor: `2` or `4` | `4` |

**What happens:**
- Input: Any supported image format
- Output: PNG files with `_2x` or `_4x` suffix
- First run downloads ~65 MB model to `~/.rembg/models/`
- Processing time: ~3-5 min/image (CPU), ~2-5 sec/image (GPU)

**Example output:**
```
Upscaling 4x: 100%|████████████████| 2/2 [00:10<00:00,  5.03s/img]
Done: 2/2 succeeded.
```

---

### `imgutil deblur` — Deblur/Denoise Images

Removes blur and noise from images using Real-ESRGAN with DNI (Deep Network Interpolation).

```bash
# Default strength (0.7)
imgutil deblur blurry/ fixed/

# Light denoise (0.3)
imgutil deblur blurry/ fixed/ -s 0.3

# Maximum denoise (1.0)
imgutil deblur blurry/ fixed/ -s 1.0
```

**Options:**
| Flag | Description | Default |
|------|-------------|---------|
| `-s`, `--strength` | Denoise strength: `0.0` to `1.0` | `0.7` |

**Strength guide:**
| Value | Effect |
|-------|--------|
| `0.0` | Minimal denoise, preserves detail |
| `0.3` | Light denoise, subtle improvement |
| `0.5` | Balanced |
| `0.7` | Strong denoise (recommended) |
| `1.0` | Maximum denoise, may over-smooth |

**What happens:**
- Input: Any supported image format
- Output: PNG files (same dimensions as input)
- First run downloads ~130 MB (2 models) to `~/.rembg/models/`
- Processing time: ~3-5 min/image (CPU), ~2-5 sec/image (GPU)

---

### `imgutil enhance` — Sharpen + Denoise

Enhances image quality without changing dimensions. Good for dark, grainy, or low-quality photos.

```bash
imgutil enhance photos/ enhanced/
```

**Options:** None

**What happens:**
- Input: Any supported image format
- Output: PNG files (same dimensions as input)
- Uses 4x model internally, then downscales back to original size
- First run downloads ~65 MB model (same as upscale)
- Processing time: ~3-5 min/image (CPU), ~2-5 sec/image (GPU)

---

### `remove-bg` — Backward Compatible Alias

```bash
# Same as imgutil remove
remove-bg photos/ processed/ -f webp
```

**Options:**
| Flag | Description | Default |
|------|-------------|---------|
| `-f`, `--format` | Output format | `png` |

---

## Supported Formats

**Input:** `.jpg`, `.jpeg`, `.png`, `.webp`, `.bmp`, `.tiff`, `.tif`

**Output:** User-specified via `-f` flag or default (PNG)

---

## Models

| Command | Model | Size | Source |
|---------|-------|------|--------|
| `remove` | U²-Net (bria-rmbg) | ~1 GB | rembg |
| `upscale` | RealESRGAN_x4plus | ~65 MB | Real-ESRGAN |
| `deblur` | realesr-general-x4v3 + wdn | ~130 MB | Real-ESRGAN |
| `enhance` | RealESRGAN_x4plus | ~65 MB | Real-ESRGAN |

Models are cached in `~/.rembg/models/` after first download.

---

## GPU vs CPU

| Mode | Speed | VRAM Required |
|------|-------|---------------|
| GPU (CUDA) | 2-5 sec/image | 2-4 GB |
| CPU | 3-5 min/image | N/A |

The tool auto-detects GPU availability. No configuration needed.

---

## Troubleshooting

### "No supported images found"
- Check that input folder exists and contains supported formats
- File extensions are case-insensitive (.JPG = .jpg)

### "CUDA out of memory"
- Reduce image size before processing
- Tiling is enabled by default (400px) to prevent this

### Slow processing
- GPU is recommended for Real-ESRGAN commands
- CPU works but is 50-100x slower

### Model download fails
- Check internet connection
- Models are from GitHub releases (may be blocked in some regions)

---

## Examples

### Batch remove backgrounds for e-commerce
```bash
imgutil remove product_photos/ clean_products/ -f webp
```

### Upscale old family photos for printing
```bash
imgutil upscale old_photos/ print_ready/ -s 4
```

### Fix blurry phone photos
```bash
imgutil deblur phone_shots/ fixed/ -s 0.8
```

### Improve dark/grainy social media photos
```bash
imgutil enhance dark_photos/ improved/
```
