import pygame as pg

pg.init()

width_of_window = 1920
height_of_window = 1000
main_window = pg.display.set_mode((width_of_window,height_of_window), pg.HWSURFACE|pg.DOUBLEBUF|pg.RESIZABLE)
window = main_window.copy()
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


class SzkieletmRNA():
    def __init__(self):
        self.image = pg.image.load("./images/mRNA.png").convert()
        self.rect = self.image.get_rect()
        self.rect.topleft = 700, 800 


class Ribosome(pg.sprite.Sprite):
    def __init__(self, name, width, height):
        pg.sprite.Sprite.__init__(self)
        ribosome = pg.image.load(name).convert()
        pg.Surface.set_colorkey(ribosome, "white")
        self.image = pg.transform.scale(ribosome, (width,height))
        self.rect = self.image.get_rect()
        self.rect.center = (int(main_window.get_width() // 2), int((main_window.get_height()//4) *3 ))


def run_game(window, mRNA):
    mRNA.rect.left -= 20
    window.blit(mRNA.image, mRNA.rect)
    x, y = mRNA.rect.topleft


small_ribosome = Ribosome("./images/ribosome.png", 400, 200)
mRNA = SzkieletmRNA()
while running:
    window.fill(window_color)

    for event in pg.event.get():  
        if event.type == pg.QUIT:  
           running = False
    if game_status == "game":
        window.blit(small_ribosome.image, small_ribosome.rect)
        run_game(window, mRNA)
    
    main_window.blit(pg.transform.scale(window, window.get_rect().size), (0, 0))
    pg.display.update()
    






