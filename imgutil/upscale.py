from pathlib import Path

import click
import cv2
from basicsr.archs.rrdbnet_arch import RRDBNet
from realesrgan import RealESRGANer

from .utils import list_images, load_image_cv2, save_image_cv2

MODEL_URLS = {
    2: "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.1/RealESRGAN_x2plus.pth",
    4: "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth",
}


def get_upsampler(scale: int, device: str = "auto") -> RealESRGANer:
    model = RRDBNet(
        num_in_ch=3, num_out_ch=3, num_feat=64,
        num_block=23, num_grow_ch=32, scale=4,
    )
    half = device != "cpu"
    return RealESRGANer(
        scale=4,
        model_path=MODEL_URLS[scale],
        model=model,
        tile=400,
        tile_pad=10,
        pre_pad=0,
        half=half,
    )


def upscale_image(input_path: Path, output_path: Path, scale: int) -> None:
    upsampler = get_upsampler(scale)
    img = load_image_cv2(input_path)
    output, _ = upsampler.enhance(img, outscale=scale)
    save_image_cv2(output_path, output)
    click.echo(f"  {input_path.name} ({scale}x) -> {output_path}")


@click.command()
@click.argument("input", type=click.Path(exists=True, file_okay=False, path_type=Path))
@click.argument("output", type=click.Path(file_okay=False, path_type=Path))
@click.option("-s", "--scale", type=click.Choice(["2", "4"]), default="4", help="Upscale factor (default: 4)")
def main(input: Path, output: Path, scale: str):
    """Upscale all images in INPUT and save to OUTPUT."""
    images = list_images(input)
    if not images:
        click.echo(f"No supported images found in {input}")
        raise SystemExit(1)

    output.mkdir(parents=True, exist_ok=True)
    click.echo(f"Processing {len(images)} image(s) at {scale}x...")

    ok = 0
    for img_path in images:
        out_path = output / f"{img_path.stem}_{scale}x.png"
        try:
            upscale_image(img_path, out_path, int(scale))
            ok += 1
        except Exception as e:
            click.echo(f"  {img_path.name} failed: {e}", err=True)

    click.echo(f"Done: {ok}/{len(images)} succeeded.")


if __name__ == "__main__":
    main()
