import Image, ImageDraw

im = Image.open('1.bmp')
draw = ImageDraw.Draw(im)
count = 0

for i in range(52):
    for j in range(51):
        count += 1
        if count % 2 == 0:
            draw.rectangle((i * 10, j * 10, (i+1) * 10, (j+1)*10),fill="#ffff00")

im.save('test.bmp')
