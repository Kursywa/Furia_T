import pygame as pg

class Ribosome(pg.sprite.Sprite):
    
    def __init__(self, name, width, height, width_of_window, height_of_window):
        """
        Create Surface object of the ribosome and its Rect object
        """
        pg.sprite.Sprite.__init__(self)
        ribosome = pg.image.load(name).convert()
        pg.Surface.set_colorkey(ribosome, "white")
        self.image = pg.transform.scale(ribosome, (width,height))
        self.rect = self.image.get_rect()
        self.rect.center = (int(width_of_window // 2), int((height_of_window//5) *4 ))