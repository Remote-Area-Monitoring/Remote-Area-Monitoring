from source.util.settings import Settings
from source.util.database import Database
from source.util.timekeeper import Timestamps
import plotly.express as px
from PIL import Image as pil
import io
from dash import dcc, html


class Image:
    def __init__(self):
        self.config = Settings('general.config')
        self.db = Database(self.config.get_setting('databases', 'images_database_path'))
        self.ts = Timestamps()

    def validate_pixel_data(self, pixels):
        length = len(pixels)
        results = list()
        results.append(pixels[0] == 255)
        results.append(pixels[1] == 216)
        results.append(pixels[length-2] == 255)
        results.append(pixels[length-1] == 217)
        if False in results:
            return False
        return True

    def get_all_images(self):
        pass

    def test_image(self):
        images = self.db.get_all()
        print(len(images))
        if images is None:
            return None
        image = images[-1]
        pixels = image['pixels']
        jpg = bytearray(pixels)
        buf = io.BytesIO(jpg)
        img = pil.open(buf)
        fig = px.imshow(img)
        fig.show()

    def get_test_image_div(self):
        images = self.db.get_all()
        print(len(images))
        if images is None:
            return None
        image = images[-1]
        pixels = image['pixels']
        jpg = bytearray(pixels)
        buf = io.BytesIO(jpg)
        img = pil.open(buf)
        fig = px.imshow(img)
        div = html.Div([
            dcc.Graph(figure=fig)
            ],
            style={'display': 'flex', 'justifyContent': 'center'}
        )
        return div

def main():
    img = Image()
    img.test_image()


if __name__ == '__main__':
    main()

