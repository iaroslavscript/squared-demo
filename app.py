#!/usr/bin/env python

from __future__ import with_statement

import sys

from PIL import Image, ImageChops


def crop(img, size):
    bg = Image.new(img.mode, img.size, img.getpixel((0, 0)))
    diff = ImageChops.difference(img, bg)
    diff = ImageChops.add(diff, diff, 2.0, -10)

    bbox = diff.getbbox()
    if bbox:
        w, h = img.size
        borderx, bordery = int(size[0] * 0.02), int(size[1] * 0.025)
        result_img = img.crop((
            bbox[0] - borderx if bbox[0] > borderx else bbox[0],
            bbox[1] - bordery if bbox[1] > bordery else bbox[1],
            bbox[2] + borderx if bbox[2] + borderx < w else w,
            bbox[3] + bordery if bbox[3] + bordery < h else h)
        )

    return result_img

def main():
    filename_in = '/tmp/origin.jpg'
    filename_out = '/tmp/cropped.jpg'

    with open(filename_in, 'wb') as f:
        f.write(sys.stdin.read())

    origin_im = Image.open(filename_in)
    cropped_im = crop(origin_im, (500,500))
    cropped_im.save(filename_out)

    with open(filename_out, 'rb') as f:
        sys.stdout.write(f.read())

if __name__ == "__main__":
    main()
