# remove-bg

Remove image backgrounds in bulk.

## Install

```bash
pip install -e .
```

## Usage

```bash
remove-bg <input_folder> <output_folder>
```

All supported images in `input_folder` will be processed and saved to `output_folder`.

### Examples

```bash
# Basic usage — outputs PNG files
remove-bg photos/ processed/

# Output as WebP instead of PNG
remove-bg photos/ processed/ -f webp

# Process a small batch for testing
remove-bg test_imgs/ test_out/ -f png
```

### Supported input formats

`.jpg`, `.jpeg`, `.png`, `.webp`, `.bmp`, `.tiff`, `.tif`

### Options

| Flag | Description |
|------|-------------|
| `-f`, `--format` | Output format: `png` (default), `webp`, etc. |

### Notes

- Output filenames match input filenames with the chosen extension.
- The output folder is created automatically if it doesn't exist.
- First run downloads a ~170 MB PyTorch model into `.remove/`.
- Supported input formats are case-insensitive.
