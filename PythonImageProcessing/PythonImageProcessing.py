from PIL import Image
from ImageZoomer import FullImageZoomer

img = Image.new( 'RGB', (250,250), "black")
pixels = img.load()

for i in range(img.size[0]):
    for j in range(img.size[1]):
        pixels[i,j] = (i, j, 100)

for p in reversed(range(1,3)):
    print(p)

x = FullImageZoomer(img, 4)
x.ZoomKTimes();
x.image.show()


