from pathlib import Path

import click
from basicsr.archs.rrdbnet_arch import RRDBNet
from realesrgan import RealESRGANer
from tqdm import tqdm

from .utils import list_images, load_image_cv2, save_image_cv2, has_cuda

MODEL_URL = "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth"


def get_upsampler() -> RealESRGANer:
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
        half=has_cuda(),
    )


def upscale_image(input_path: Path, output_path: Path, scale: int) -> None:
    upsampler = get_upsampler()
    img = load_image_cv2(input_path)
    output, _ = upsampler.enhance(img, outscale=scale)
    save_image_cv2(output_path, output)


@click.command()
@click.help_option("-h", "--help")
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

    ok = 0
    for img_path in tqdm(images, desc=f"Upscaling {scale}x", unit="img"):
        out_path = output / f"{img_path.stem}_{scale}x.png"
        try:
            upscale_image(img_path, out_path, int(scale))
            ok += 1
        except Exception as e:
            click.echo(f"\n  {img_path.name} failed: {e}", err=True)

    click.echo(f"Done: {ok}/{len(images)} succeeded.")


if __name__ == "__main__":
    main()
