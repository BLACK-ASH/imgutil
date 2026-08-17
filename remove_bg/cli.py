from pathlib import Path

import click
from rembg import remove
from PIL import Image

SUPPORTED = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff", ".tif"}


def process_image(input_path: Path, output_path: Path) -> bool:
    try:
        input_image = Image.open(input_path)
        output_image = remove(input_image)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_image.save(output_path, "PNG")
        click.echo(f"  {input_path.name} -> {output_path}")
        return True
    except Exception as e:
        click.echo(f"  {input_path.name} failed: {e}", err=True)
        return False


@click.command()
@click.argument("input", type=click.Path(exists=True, file_okay=False, path_type=Path))
@click.argument("output", type=click.Path(file_okay=False, path_type=Path))
@click.option("-f", "--format", "fmt", default="png", help="Output format (default: png)")
def main(input: Path, output: Path, fmt: str):
    """Remove backgrounds from all images in INPUT and save to OUTPUT."""
    images = sorted(f for f in input.iterdir() if f.suffix.lower() in SUPPORTED)

    if not images:
        click.echo(f"No supported images found in {input}")
        raise SystemExit(1)

    output.mkdir(parents=True, exist_ok=True)
    click.echo(f"Processing {len(images)} image(s)...")

    ok = 0
    for img_path in images:
        out_path = output / f"{img_path.stem}.{fmt.lower()}"
        if process_image(img_path, out_path):
            ok += 1

    click.echo(f"Done: {ok}/{len(images)} succeeded.")


if __name__ == "__main__":
    main()
