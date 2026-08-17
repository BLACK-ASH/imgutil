import click

from . import __version__


@click.group()
@click.version_option(__version__, prog_name="imgutil")
def main():
    """imgutil — multi-utility image processing tool."""


from .remove import main as remove_cmd
from .upscale import main as upscale_cmd
from .deblur import main as deblur_cmd
from .enhance import main as enhance_cmd

main.add_command(remove_cmd, "remove")
main.add_command(upscale_cmd, "upscale")
main.add_command(deblur_cmd, "deblur")
main.add_command(enhance_cmd, "enhance")


if __name__ == "__main__":
    main()
