from PIL import Image
from ImageZoomer import FullImageZoomer

img = Image.new( 'RGB', (150, 150), "black")
#img = Image.open('TestData/480x320hand.jpg')
#img = Image.open('RGB','TestData/512x512google.png')
img = Image.open('TestData/150x150_3.jpg')
pixels = img.load()

#for i in range(img.size[0]):
#    for j in range(img.size[1]):
#        pixels[i,j] = (i, j, 100)


x = FullImageZoomer(img, 4)
x.ZoomTwice();
x.image.show()


