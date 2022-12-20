import math

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
    self.n_tiles_per_row = math.ceil(self.wall_width/tile.width)*self.row_multiplicator
    self.n_rows = math.ceil(self.wall_height/tile.height)
    self.n_tiles = self.n_tiles_per_row*self.n_rows
    


    

tile = Tile(13.2,11.4)
t = Wall(300,70,tile, [1,3,3,3,3])
class Test_wall:
    def __init__(self,  Wall(13.2,11.4,Tile(13.2,11.4),[1,1,1,1,1]), Tile(13.2,11.4))

        print(t.n_rows)
        print(t.n_tiles_per_row)
        print(t.n_tiles)
        test = Wall(13.2,11.4,tile,[1,1,1,1,1])
        print(test.n_tiles)
