#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Image

def sketch(img, threshold):
    '''
    素描
    param img: Image实例
    param threshold: 介于0到100
    '''
    if threshold < 0: threshold = 0
    if threshold > 100: threshold = 100
     
    width, height = img.size
    img = img.convert('L') # convert to grayscale mode
    pix = img.load() # get pixel matrix
 
    for w in xrange(width):
        for h in xrange(height):
            if w == width-1 or h == height-1:
                continue
             
            src = pix[w, h]
            dst = pix[w+1, h+1]
 
            diff = abs(src - dst)
 
            if diff >= threshold:
                pix[w, h] = 0
            else:
                pix[w, h] = 255
 
    return img

def pencil(img, threshold):
    '''
    铅笔画
    param img: instance of Image
    param threshold
    '''
    if threshold < 0: threshold = 0
    if threshold > 100: threshold = 100
 
    width, height = img.size
    dst_img = Image.new("RGBA", (width, height))
 
    if img.mode != "RGBA":
        img = img.convert("RGBA")
 
    pix = img.load()
    dst_pix = dst_img.load()
 
    for w in xrange(width):
        for h in xrange(height):
            if w == 0 or w == width - 1 \
               or h == 0 or h == height - 1:
                continue
 
            # 包括当前像素周围共9个像素点
            around_wh_pixels = [pix[i, j][:3] for j in xrange(h-1, h+2) for i in xrange(w-1, w+2)]
            # 排除当前像素点
            exclude_wh_pixels = tuple(around_wh_pixels[:4] + around_wh_pixels[5:])
            # 把各个像素点的各个分量求平均值          
            RGB = map(lambda l: int(sum(l) / len(l)), zip(*exclude_wh_pixels))
             
            cr_p = pix[i, j] # 当前像素点
 
            cr_draw = all([abs(cr_p[i] - RGB[i]) >= threshold for i in range(3)])
            
            if cr_draw:
                dst_pix[w, h] = 0, 0, 0, cr_p[3]
            else:
                dst_pix[w, h] = 255, 255, 255, cr_p[3]
 
    return dst_img

if __name__ == "__main__":
    import sys, os
 
    path = os.path.dirname(__file__) + os.sep.join(['', 'images', 'lam.jpg'])
    threshold = 15
     
    if len(sys.argv) == 2:
        try:
            threshold = int(sys.argv[1])
        except ValueError:
            path  = sys.argv[1]
    elif len(sys.argv) == 3:
        path = sys.argv[1]
        threshold = int(sys.argv[2])
 
    img = Image.open(path)
    #img = pencil(img, threshold)
    img = sketch(img, threshold)
    img.save(os.path.splitext(path)[0]+'.sketch.jpg', 'JPEG')
