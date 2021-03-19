""" This script will generate and update the example decoration images. 
Right now, I use the `dsad` username to generate the examples, as it has
a default GitHub profile picture. """

import os
import click
from image import Decoration


@click.command()
@click.argument('gh-username')
@click.argument('filename', default='example.png', required=False)
def main(gh_username: str, filename: str):

    for dec_name in Decoration.avaliable_decorations():
        decoration = Decoration(dec_name)

        try:
            img = decoration.generate_github_image(gh_username)

        except ValueError as e:
            # If invalid github username
            click.echo(e)
            exit(20)

        saving_path = os.path.join(
            decoration.DECORATIONS_FOLDER,
            dec_name,
            filename,
        )

        img.save(saving_path)


if __name__ == "__main__":
    main()
