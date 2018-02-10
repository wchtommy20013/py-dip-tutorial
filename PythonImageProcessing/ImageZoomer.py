from PIL import Image
import numpy as np
import itertools

class FullImageZoomer:
    def __init__(self, image, zoom_factor):
        self.image = image
        self.K = zoom_factor

    """description of class""" 
    def PixelReplication(self):
        img = Image.new( 'RGB', (self.image.size[0] * self.K, self.image.size[1] * self.K)) 
        pixels = img.load() 
        original_pixels = self.image.load()
    
        for i in range(img.size[0]):
            for j in range(img.size[1]):
                pixels[i,j] = original_pixels[i / self.K, j / self.K]
        self.image.close()
        self.image = img

    def ZoomTwice(self):
        if not is_power_of_two(self.K):
            raise ValueError("K is not power of 2")

        zoom_factor = self.K
        while zoom_factor != 1:
            img = Image.new( 'RGB', (self.image.size[0] * 2 - 1, self.image.size[1] * 2 - 1))
            pixels = img.load()

            original_pixels = self.image.load()

            #Row-wise operation
            for i in range(img.size[0]):
                for j in range(0, img.size[1], 2):
                    if i % 2 == 1:
                        pixels[i,j] = tuple_avg(original_pixels[i / 2 - 1, j/2], original_pixels[i / 2 + 1, j/2])
                    else:
                        pixels[i,j] = original_pixels[i/2, j/2]

            #Column-wise operation
            for i in range(img.size[0]):
                for j in range(1, img.size[1], 2):
                    pixels[i,j] = tuple_avg(original_pixels[i / 2, j/2 - 1], original_pixels[i / 2, j/2 + 1])

            zoom_factor = zoom_factor / 2
            self.image = img

    def ZoomKTimes(self):
        # Must > 1x1
        img = Image.new( 'RGB', ((self.image.size[0] - 1) * self.K + 1, (self.image.size[1] - 1) * self.K + 1)) 
        pixels = img.load() 
        original_pixels = self.image.load()

        #Row-wise operation
        for i in range(self.image.size[0]):
            for j in range(self.image.size[1]):
                pixels[i * self.K ,j * self.K] = original_pixels[i,j]
                if i < self.image.size[0] - 1: 
                    diffx = tuple_diff(original_pixels[i,j], original_pixels[i + 1, j])
                    for p in range(0, self.K):
                        if original_pixels[i,j] < original_pixels[i+1,j]:
                          smallerx = original_pixels[i,j]
                          x_pt = i * self.K + p
                        else:
                          smallerx = original_pixels[i + 1,j]
                          x_pt = (i + 1) * self.K - p
                        if p in range(1, self.K):
                            pixels[x_pt, j * self.K] = tuple_add(smallerx ,tuple_div_mul(diffx, self.K, self.K - p - 1))
                        
                        if j > 0 :
                            diffy = tuple_diff(pixels[x_pt,j * self.K], pixels[x_pt, (j-1) * self.K])
                            for q in range(1, self.K):
                                if pixels[x_pt,j * self.K] < pixels[x_pt, (j-1) * self.K]:
                                    smallery = pixels[x_pt,j * self.K]
                                    y_pt = j * self.K - q
                                else:
                                    smallery = pixels[x_pt, (j-1) * self.K]
                                    y_pt = (j - 1) * self.K + q
                                pixels[x_pt, y_pt] = tuple_add(smallery, tuple_div_mul(diffy, self.K, self.K-q-1 ))
                elif j > 0:
                    
                    diffy = tuple_diff(original_pixels[i,j], original_pixels[i, j-1])
                    for q in range(1, self.K):
                        if original_pixels[i,j] < original_pixels[i, j-1]:
                            smallery = original_pixels[i, j]
                            y_pt = j * self.K - q
                        else:
                            smallery = original_pixels[i, j-1]
                            y_pt = (j - 1) * self.K + q
                        pixels[i * self.K, y_pt] = tuple_add(smallery, tuple_div_mul(diffy, self.K, self.K-q-1 ))

        self.image = img

def is_power_of_two(num):
	return num != 0 and ((num & (num - 1)) == 0)

def tuple_avg(xs,ys):
     return tuple(int((x + y) / 2) for x, y in zip(xs, ys))

def tuple_div_mul(xs, K, M):
     return tuple(int((x / K) * M) for x in xs)

def tuple_div(xs, K):
     return tuple(int(x / K) for x in xs)
 
def tuple_diff(xs,ys):
     return tuple(abs(x - y) for x, y in zip(xs, ys))
 
def tuple_add(xs,ys):
     return tuple(x + y for x, y in zip(xs, ys))
