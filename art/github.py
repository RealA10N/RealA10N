from PIL import Image, ImageFont, ImageDraw
from pathlib import Path
from . import DynamicBanner

THIS = Path(__file__)
REPO = THIS.parents[1]


class GitHubBanner(DynamicBanner):

    base: Image.Image = Image.open(
        REPO / 'assets' / 'images' / 'base-banner.png')

    class fonts:
        path = str(REPO / 'assets' / 'fonts' / 'MADE TOMMY Black.otf')

        h1 = ImageFont.truetype(path, size=50)
        h2 = ImageFont.truetype(path, size=40)
        regular = ImageFont.truetype(path, size=25)

    class colors:
        main = '#fff'
        bold = '#d11c1c'

    def __call__(self):

        # TODO: maybe can copy the image at the end of the previous request
        img = self.base.copy()
        draw = ImageDraw.Draw(img)

        # Title
        # TODO: static info can be generated once and not every time.
        draw.multiline_text(
            xy=(img.width // 2, 150),
            text='\n'.join(('Welcome to my', 'GitHub profile!')),
            fill=self.colors.main,
            font=self.fonts.h1,
            anchor='ms',
            align='center',
            spacing=0,
        )

        # Visitor counter
        draw.text(
            (img.width // 2, 280),
            text=f"{self.db.data['visitors']} people",
            fill=self.colors.bold,
            font=self.fonts.h2,
            anchor='ms',
            align='center',
        )

        draw.multiline_text(
            (img.width // 2, 310),
            text='\n'.join(('have visited this page', 'before you did.')),
            font=self.fonts.regular,
            fill=self.colors.main,
            anchor='ms',
            align='center',
            spacing=0,
        )

        return img
