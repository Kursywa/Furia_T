import pygame as pg

pg.init()

width_of_window = 1920
height_of_window = 1000
window = pg.display.set_mode((width_of_window,height_of_window), pg.HWSURFACE|DOUBLEBUF|RESIZABLE)
fake_window = window.copy()
window_color = (230, 230 , 250)

# game_status = "main page" / "instruction" / "game" / "result"
game_status = "game"

running = True


while running:
    window.fill(window_color)

    for event in pg.event.get():  
        if event.type == pg.QUIT:  
           running = False

    
    window.blit(pygame.transform.scale(fake_window, window.get_rect().size), (0, 0))
    pg.display.update()
    






