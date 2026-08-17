from pathlib import Path

import click
from realesrgan import RealESRGANer
from realesrgan.archs.srvgg_arch import SRVGGNetCompact

from .utils import list_images, load_image_cv2, save_image_cv2

MODEL_BASE = "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/"
MODELS = {
    "denoise": f"{MODEL_BASE}realesr-general-x4v3.pth",
    "wavelet": f"{MODEL_BASE}realesr-general-wdn-x4v3.pth",
}


def get_deblurred_upsampler(strength: float) -> RealESRGANer:
    model = SRVGGNetCompact(
        num_in_ch=3, num_out_ch=3, num_feat=64,
        num_conv=32, upscale=4, act_type="prelu",
    )
    return RealESRGANer(
        scale=4,
        model_path=[MODELS["denoise"], MODELS["wavelet"]],
        dni_weight=[strength, 1.0 - strength],
        model=model,
        tile=400,
        tile_pad=10,
        pre_pad=0,
        half=True,
    )


def deblur_image(input_path: Path, output_path: Path, strength: float) -> None:
    upsampler = get_deblurred_upsampler(strength)
    img = load_image_cv2(input_path)
    output, _ = upsampler.enhance(img, outscale=1.0)
    save_image_cv2(output_path, output)
    click.echo(f"  {input_path.name} -> {output_path}")


@click.command()
@click.argument("input", type=click.Path(exists=True, file_okay=False, path_type=Path))
@click.argument("output", type=click.Path(file_okay=False, path_type=Path))
@click.option("-s", "--strength", type=float, default=0.7, help="Denoise strength 0.0-1.0 (default: 0.7)")
def main(input: Path, output: Path, strength: float):
    """Deblur/denoise all images in INPUT and save to OUTPUT."""
    images = list_images(input)
    if not images:
        click.echo(f"No supported images found in {input}")
        raise SystemExit(1)

    output.mkdir(parents=True, exist_ok=True)
    click.echo(f"Processing {len(images)} image(s) (strength={strength})...")

    ok = 0
    for img_path in images:
        out_path = output / f"{img_path.stem}.png"
        try:
            deblur_image(img_path, out_path, strength)
            ok += 1
        except Exception as e:
            click.echo(f"  {img_path.name} failed: {e}", err=True)

    click.echo(f"Done: {ok}/{len(images)} succeeded.")


if __name__ == "__main__":
    main()
