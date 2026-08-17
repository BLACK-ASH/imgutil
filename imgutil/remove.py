from pathlib import Path

import click
from rembg import remove
from PIL import Image
from tqdm import tqdm

from .utils import list_images, save_image_pil


def remove_background(input_path: Path, output_path: Path, fmt: str) -> None:
    input_image = Image.open(input_path)
    output_image = remove(input_image)
    save_image_pil(output_path, output_image, fmt.upper())


@click.command()
@click.argument("input", type=click.Path(exists=True, file_okay=False, path_type=Path))
@click.argument("output", type=click.Path(file_okay=False, path_type=Path))
@click.option("-f", "--format", "fmt", default="png", help="Output format (default: png)")
def main(input: Path, output: Path, fmt: str):
    """Remove backgrounds from all images in INPUT and save to OUTPUT."""
    images = list_images(input)
    if not images:
        click.echo(f"No supported images found in {input}")
        raise SystemExit(1)

    output.mkdir(parents=True, exist_ok=True)

    ok = 0
    for img_path in tqdm(images, desc="Removing backgrounds", unit="img"):
        out_path = output / f"{img_path.stem}.{fmt.lower()}"
        try:
            remove_background(img_path, out_path, fmt)
            ok += 1
        except Exception as e:
            click.echo(f"\n  {img_path.name} failed: {e}", err=True)

    click.echo(f"Done: {ok}/{len(images)} succeeded.")


if __name__ == "__main__":
    main()
