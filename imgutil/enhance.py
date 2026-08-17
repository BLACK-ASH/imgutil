from pathlib import Path

import click
from basicsr.archs.rrdbnet_arch import RRDBNet
from realesrgan import RealESRGANer

from .utils import list_images, load_image_cv2, save_image_cv2

MODEL_URL = "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth"


def get_enhancer() -> RealESRGANer:
    model = RRDBNet(
        num_in_ch=3, num_out_ch=3, num_feat=64,
        num_block=23, num_grow_ch=32, scale=4,
    )
    return RealESRGANer(
        scale=4,
        model_path=MODEL_URL,
        model=model,
        tile=400,
        tile_pad=10,
        pre_pad=0,
        half=True,
    )


def enhance_image(input_path: Path, output_path: Path) -> None:
    enhancer = get_enhancer()
    img = load_image_cv2(input_path)
    output, _ = enhancer.enhance(img, outscale=1.0)
    save_image_cv2(output_path, output)
    click.echo(f"  {input_path.name} -> {output_path}")


@click.command()
@click.argument("input", type=click.Path(exists=True, file_okay=False, path_type=Path))
@click.argument("output", type=click.Path(file_okay=False, path_type=Path))
def main(input: Path, output: Path):
    """Enhance all images in INPUT (sharpen + denoise, same dimensions)."""
    images = list_images(input)
    if not images:
        click.echo(f"No supported images found in {input}")
        raise SystemExit(1)

    output.mkdir(parents=True, exist_ok=True)
    click.echo(f"Processing {len(images)} image(s)...")

    ok = 0
    for img_path in images:
        out_path = output / f"{img_path.stem}.png"
        try:
            enhance_image(img_path, out_path)
            ok += 1
        except Exception as e:
            click.echo(f"  {img_path.name} failed: {e}", err=True)

    click.echo(f"Done: {ok}/{len(images)} succeeded.")


if __name__ == "__main__":
    main()
