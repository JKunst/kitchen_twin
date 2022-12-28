import math
import random
import pandas as pd
from typing import List

from PIL import Image, ImageDraw

random.seed(12)
CANVAS_WIDTH = 5000
CANVAS_HEIGHT = 2400
color_map = {0: '#f4f4f4', 1: '#c7c3c0', 2: '#a3a8ae', 3: '#d4beb1', 4: '#80736c'}


# white grey blue pink bronze

class Tile:
    '''Argumenten breedte (cm), hoogte (cm), vorm en kleur'''

    def __init__(self, t_width, t_height, shape='Triangle', color='White'):
        self.width = t_width
        self.height = t_height
        self.color = color
        self.shape = shape


class Wall:
    '''Stuk wand met breedte (cm), hoogte (cm) en tegels uit class Tile, met kleur verdeling'''

    def __init__(self, wall_w, wall_h, tile, dist):
        self.wall_width = wall_w
        self.wall_height = wall_h
        self.tile = tile
        self.distribution = dist
        self.row_multiplicator = 2 if tile.shape == 'Triangle' else 1
        self.n_tiles_per_row = math.ceil(self.wall_width / tile.width) * self.row_multiplicator
        self.n_rows = math.ceil(self.wall_height / tile.height)
        self.n_tiles = self.n_tiles_per_row * self.n_rows
        self.COUNTER = [[0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0]]
        self.beschikbaar = pd.DataFrame([[13*30,3*30,3*30,3*30,1*30]],index=['Beschikbaar'],
                                        columns=['Wit', 'Grijs', 'Blauw', 'Roze', 'Brons'])

    def create_ranges(self, row):
        ranges = []
        temp_dist = 0
        for i in range(0, len(self.distribution[row])):
            temp_dist += self.distribution[row][i]
            ranges.append(temp_dist / sum(self.distribution[row]))
        return ranges

    def draw_tile_color(self, row):
        draw = random.random()
        color = 0
        distribution_range = self.create_ranges(row)
        while draw > distribution_range[color]:
            color += 1
        self.COUNTER[row][color]+=1
        return color

    def create_row(self):
        'obsolete'
        result_row = [self.draw_tile_color() for _ in range(self.n_tiles_per_row)]

        return result_row

    def scale_coordinates(self, generator):
        tile = self.tile
        for coords in generator(int(self.n_tiles_per_row / 2), self.n_rows):
            # Get the row to apply color distribution
            row_number = round(coords[2][1] * math.sin(math.pi / 3) * 4 / 3) % len(self.distribution) - 1

            yield ([(x * tile.width, y * tile.width) for (x, y) in coords], color_map[self.draw_tile_color(row_number)])

    def generate_unit_triangles(self, tiles_per_row, rows):
        h = math.sin(math.pi / 3)

        for x in range(0, tiles_per_row):
            for y in range(int(rows / h)):
                # Add a horizontal offset on odd numbered rows
                x_ = x if (y % 2 == 0) else x + 0.5

                yield [(x_, y * h), (x_ + 1, y * h), (x_ + 0.5, (y + 1) * h)]
                yield [(x_ + 1, y * h), (x_ + 1.5, (y + 1) * h), (x_ + 0.5, (y + 1) * h)]

    def generate_triangles(self, *args, **kwargs):
        """Generate coordinates for a tiling of triangles."""
        return self.scale_coordinates(self.generate_unit_triangles, *args, **kwargs)

    def draw_tiling(self, filename):
        """
        Given a coordinate generator and a filename, render those coordinates
        in a new image and save them to the file.
        """

        im = Image.new('RGB', size=(CANVAS_WIDTH, CANVAS_HEIGHT))
        for (shape, color) in self.generate_triangles():
            ImageDraw.Draw(im).polygon(shape, fill=color, outline='grey')
        self.wall_summary = pd.DataFrame(self.COUNTER, columns=['Wit', 'Grijs', 'Blauw', 'Roze', 'Brons'])
        print(filename)
        print('Tegels per rij: ', str(self.n_tiles_per_row), 'geeft aantal cm: ', str(self.n_tiles_per_row*tile.width/10/2),
              'met hoogte: ',str(self.n_rows),' * ' , str(tile.height/10),'= ',str(self.n_rows * tile.height/10))
        self.wall_summary.loc['Totaal'] = self.wall_summary.sum(axis=0)
        self.wall_summary.loc['Beschikbaar'] = [13*30,3*30,3*30,3*30,1*30]
        self.wall_summary.loc['Overblijvend'] = self.wall_summary.loc['Beschikbaar'] - self.wall_summary.loc['Totaal']
        #assert self.wall_summary['Overblijvend'].min()<0
        print(self.wall_summary)
        im.save(filename)



    # if __name__ == '__main__':
    #     # draw_tiling(generate_squares,   filename='squares.png')
    #     draw_tiling(filename='first_wall.png')
    #     # draw_tiling(generate_hexagons,  filename='hexagons.png')

tile = Tile(132, 114)

SCHEMA = [[1, 0, 0, 0, 0],
          [0, 1, 0, 0, 0],
          [0, 0, 1, 0, 0],
          [0, 0, 0, 1, 0],
          [0, 0, 0, 0, 1],
          [13, 3, 3, 3, 1],
          [1, 1, 1, 1, 1]]


first_wall = Wall(3000, 7 * 114, tile, SCHEMA)
first_wall.draw_tiling(filename='first_wall.png')

SCHEMA2 = [[1, 0, 0, 0, 0],
           [0.90, 0.01, 0.02, 0.02, 0.05],
           [0.80, 0.05, 0.05, 0.05, 0.05],
           [0.75, 0.05, 0.075, 0.075, 0.05],
           [0.65, 0.10, 0.10, 0.10, 0.05],
           [0.55, 0.10, 0.15, 0.15, 0.05],
           [0.45, 0.15, 0.15, 0.15, 0.10]
           ]
second_wall = Wall(3000, 6 * 114, tile, SCHEMA2)
second_wall.draw_tiling(filename='second_wall.png')

SCHEMA3 = [
    [0.90, 0.01, 0.02, 0.02, 0.05],
    [0.80, 0.05, 0.05, 0.05, 0.05],
    [0.75, 0.05, 0.075, 0.075, 0.05],
    [0.65, 0.10, 0.10, 0.10, 0.05],
    [0.55, 0.10, 0.15, 0.15, 0.05],
    [0.45, 0.20, 0.15, 0.15, 0.05],
    [0.30, 0.25, 0.20, 0.20, 0.05]
]
third_wall = Wall(3000, 6 * 114, tile, SCHEMA3)
third_wall.draw_tiling(filename='third_wall.png')
save_aantallen = third_wall.wall_summary.loc['Overblijvend']

SCHEMA4 = [
    [0.65, 0.10, 0.10, 0.10, 0.05],
    [0.65, 0.10, 0.10, 0.10, 0.05],
    [0.65, 0.10, 0.10, 0.10, 0.05],
    [0.65, 0.10, 0.10, 0.10, 0.05],
    [0.45, 0.15, 0.15, 0.20, 0.05],
    [0.30, 0.20, 0.25, 0.20, 0.05],
    [0.20, 0.25, 0.30, 0.20, 0.05],
    [0.20, 0.25, 0.20, 0.30, 0.05],
    [0.20, 0.30, 0.25, 0.20, 0.05],
    [0.10, 0.25, 0.30, 0.30, 0.05],
    [0.10, 0.30, 0.25, 0.30, 0.05]
]
korte_wall = Wall(1000, 10 * 114, tile, SCHEMA4)
korte_wall.draw_tiling(filename='korte_wall.png')
print(save_aantallen)
class Test_wall:
    def __init__(self, test_wall, test_tile):
        assert test_wall.n_rows == 1
        assert test_wall.n_tiles_per_row == 2
        assert test_wall.n_tiles == 2


test_wall = Test_wall(Wall(13.2, 11.4, Tile(13.2, 11.4), [1, 1, 1, 1, 1]), Tile(13.2, 11.4))
# t.create_row()
