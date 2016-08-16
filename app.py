#!/usr/bin/env python

from __future__ import with_statement, division

import sys

from PIL import Image, ImageChops


def fill(img, size, background_color):
    img.thumbnail(size)
    if img.size == size:
        return img # No need to fill
    x = max(int((size[0] - img.size[0]) / 2.0), 0)
    y = max(int((size[1] - img.size[1]) / 2.0), 0)
    background_img = Image.new(mode="RGB", size=size, color=background_color)
    background_img.paste(img, (x, y))
    return background_img

def trim(img, size, background_color):
    bg = Image.new(img.mode, img.size, img.getpixel((0, 0)))
    diff = ImageChops.difference(img, bg)
    diff = ImageChops.add(diff, diff, 2.0, -10)

    bbox = diff.getbbox()
    if bbox:
        w, h = img.size
        borderx, bordery = int(size[0] * 0.02), int(size[1] * 0.025)
        img = img.crop((
            bbox[0] - borderx if bbox[0] > borderx else bbox[0],
            bbox[1] - bordery if bbox[1] > bordery else bbox[1],
            bbox[2] + borderx if bbox[2] + borderx < w else w,
            bbox[3] + bordery if bbox[3] + bordery < h else h)
        )

    img = fill(img, size, background_color)

    return img

def main():
    filename_in = '/tmp/origin.jpg'
    filename_out = '/tmp/cropped.jpg'
    square_size = (500,500)
    background_color = (255, 255, 255)

    #  copy origin image from stdin to temp file
    with open(filename_in, 'wb') as f:
        f.write(sys.stdin.read())

    cropped_im = trim(Image.open(filename_in), square_size, background_color)
    cropped_im.save(filename_out)

    # copy squared image from temp file to stdout
    with open(filename_out, 'rb') as f:
        sys.stdout.write(f.read())

if __name__ == "__main__":
    main()

