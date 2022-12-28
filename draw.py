#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Generate regular tilings of the plane with Pillow.

Diagrams and background to this code are on my blog:
http://alexwlchan.net/2016/10/tiling-the-plane-with-pillow/
"""

from __future__ import division

import math

from PIL import Image, ImageDraw, ImageColor

CANVAS_WIDTH  = 500
CANVAS_HEIGHT = 100


def _scale_coordinates(generator, image_width, image_height, side_length=13.2):
    scaled_width = 16# int(image_width / side_length)
    scaled_height = 3 #int(image_height / side_length)

    for coords in generator(scaled_width, scaled_height):
        yield [(x * side_length, y * side_length) for (x, y) in coords]


def generate_unit_triangles(image_width, image_height):
    """Generate coordinates for a tiling of unit triangles."""
    # Our triangles lie with one side parallel to the x-axis.  Let s be
    # the length of one side, and h the height of the triangle.
    #
    # The for loops (x, y) gives the coordinates of the top left-hand corner
    # of a pair of triangles:
    #
    #           (x, y) +-----+ (x + 1, y)
    #                   \   / \
    #                    \ /   \
    #    (x + 1/2, y + h) +-----+ (x + 3/2, y + h)
    #
    # where h = sin(60°) is the height of an equilateral triangle with
    # side length 1.
    #
    # On odd-numbered rows, we translate by (s/2, 0) to make the triangles
    # line up with the even-numbered rows.
    #
    # To avoid blank spaces on the edge of the canvas, the first pair of
    # triangles on each row starts at (-1, 0) -- one width before the edge
    # of the canvas.
    h = math.sin(math.pi / 3)

    for x in range(2, image_width):
        for y in range(2,int(image_height / h)):

            # Add a horizontal offset on odd numbered rows
            x_ = x if (y % 2 == 0) else x + 0.5

            yield [(x_, y * h), (x_+1, y * h), (x_+0.5, (y+1) * h)]
            yield [(x_+1, y * h), (x_+1.5, (y+1) * h), (x_+0.5, (y+1) * h)]

def generate_triangles(*args, **kwargs):
    """Generate coordinates for a tiling of triangles."""
    return _scale_coordinates(generate_unit_triangles, *args, **kwargs)


def draw_tiling(coord_generator, filename):
    """
    Given a coordinate generator and a filename, render those coordinates
    in a new image and save them to the file.
    """
    im = Image.new('RGB', size=(CANVAS_WIDTH, CANVAS_HEIGHT))
    for shape in coord_generator(500, 500):
        ImageDraw.Draw(im).polygon(shape,fill ="orange", outline='white')
    im.save(filename)


if __name__ == '__main__':
    #draw_tiling(generate_squares,   filename='squares.png')
    draw_tiling(generate_triangles, filename='triangles.png')
    #draw_tiling(generate_hexagons,  filename='hexagons.png')