import io
from PIL import Image

image = Image.open('example.jpg')

imgByteArr = io.BytesIO()
image.save(imgByteArr, format=image.format)
imgByteArr = imgByteArr.getvalue()
print(imgByteArr)
print(imgByteArr.find(b'\xff\xd8'))
