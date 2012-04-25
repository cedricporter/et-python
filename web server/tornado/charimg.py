#!/usr/bin/env python
# author:  Hua Liang [ Stupid ET ]
# email:   et@everet.org
# website: http://EverET.org
#
import Image

color = 'MNHQ$OC?7>!:-;.'

def to_html(func):
    html_head = '''
            <html>
              <head>
                <style type="text/css">
                  body {font-family:Monospace; font-size:5px;}
                </style>
              </head>
            <body> '''
    html_tail = '</body></html>'

    def wrapper(img):
        pic_str = func(img)
        pic_str = ''.join(l + ' <br/>' for l in pic_str.splitlines())
        return html_head + pic_str + html_tail

    return wrapper

@to_html
def make_char_img(img):
    pix = img.load()
    pic_str = ''
    width, height = img.size
    for h in xrange(height):
        for w in xrange(width):
            pic_str += color[int(pix[w, h]) * 14 / 255] * 2
        pic_str += '\n'
    return pic_str

def preprocess(img_name):
    img = Image.open(img_name)

    w, h = img.size
    m = max(img.size)
    delta = m / 180.0 
    w, h = int(w / delta), int(h / delta)
    img = img.resize((w, h))
    img = img.convert('L')

    return img

def make_save_char_img(filename, outfilename):
    save_to_file(make_char_image(filename), outfilename)

def save_to_file(pic_str, filename):
    outfile = open(filename, 'w')
    outfile.write(pic_str)
    outfile.close()

def make_char_image(filename):
    img = preprocess(filename) 
    pic_str = make_char_img(img) 
    return pic_str

def main():
    pass


if __name__ == '__main__':
    main()
