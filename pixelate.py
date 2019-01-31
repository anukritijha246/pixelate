from PIL import Image
import operator
from collections import defaultdict
import re
input_path = 'input.jpg'
output_path = 'output.png'
size = (4,4)
palette = [
    (45,  50,  50),  #black
    (240, 68,  64),  #red
    (211, 223, 223), #white
    (160, 161, 67),  #green
    (233, 129, 76),  #orange
]
while len(palette) < 256:
    palette.append((0, 0, 0))
flat_palette = reduce(lambda a, b: a+b, palette)
assert len(flat_palette) == 768
palette_img = Image.new('P', (1, 1), 0)
palette_img.putpalette(flat_palette)
multiplier=8
img = Image.open(input_path)
img = img.resize((size[0] * multiplier, size[1] * multiplier), Image.BICUBIC)
img = img.quantize(palette=palette_img) #reduce the palette
img = img.convert('RGB')
out = Image.new('RGB', size)
for x in range(size[0]):
    for y in range(size[1]):
        #sample at get average color in the corresponding square
        histogram = defaultdict(int)
        for x2 in range(x * multiplier, (x + 1) * multiplier):
            for y2 in range(y * multiplier, (y + 1) * multiplier):
                histogram[img.getpixel((x2,y2))] += 1
        color = max(histogram.iteritems(), key=operator.itemgetter(1))[0]
        out.putpixel((x, y), color)
out=out.resize((1000,1000))
out.save(output_path)
