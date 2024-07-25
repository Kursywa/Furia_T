import pygame as pg

<<<<<<< HEAD
pg.init()

width_of_window = 1920
height_of_window = 1000
window = pg.display.set_mode((width_of_window,height_of_window), pg.HWSURFACE|DOUBLEBUF|RESIZABLE)
fake_window = window.copy()
window_color = (230, 230 , 250)

def show_menu():

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    # color pallette
    title_color = (220, 220, 160)
    background_color = "white"

    #button init
    start_btn = pg.rect(100,100,400,60)
    instruction_btn = pg.rect(100,200,400,60)
    highscore_btn = pg.rect(100,300,400,60)
    quit_btn = pg.rect(100,400,400,60)

    pic = pg.sys_font(None,50).render('Nowa gra', True, title_color, background_color)
    pic.set_colorkey((background_color))
    position = ((self.screen_size - pic.get_size()) / 2).astype(int)
    screen.blit(pic, start_btn)


    # RENDER YOUR GAME HERE

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60
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
    






=======

>>>>>>> a46c4f2 (adding menu)
