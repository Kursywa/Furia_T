import pygame as pg
import ctypes
ctypes.windll.user32.SetProcessDPIAware() # workaround for windows, makes pg.display.set_mode apply 
#correct pixel ratio of the screen in windowed mode

pg.init()
width_of_window = 1920
height_of_window = 1000
main_window = pg.display.set_mode((width_of_window,height_of_window), pg.HWSURFACE|pg.DOUBLEBUF|pg.RESIZABLE)
<<<<<<< HEAD
window = main_window.copy()
=======
# window = main_window.copy()
# main_window.blit(pg.transform.scale(window, window.get_rect().size), (0, 0))
# pg.display.update()

>>>>>>> 1e2cf0bac7b5a139d5f23c68ff6f154ed762ec0b
window_color = (230, 230 , 250)
def main():
    game_status = "game"

    running = True
    while running:
        show_menu()

        for event in pg.event.get():  
            if event.type == pg.QUIT:  
                running = False

def show_menu():

    # fill the screen with a color to wipe away anything from last frame
    main_window.fill("purple")

    # color pallette
    title_color = "red" #(220, 220, 160)
    background_color = "white"

    #button init
    start_btn = pg.Rect(300,100,400,60)
    instruction_btn = pg.Rect(100,200,400,60)
    highscore_btn = pg.Rect(100,300,400,60)
    quit_btn = pg.Rect(100,400,400,60)

    pic = pg.font.Font(None,50).render('Nowa gra', True, title_color, background_color)
    pic.set_colorkey((background_color))
    main_window.blit(pic, start_btn)


    # RENDER YOUR GAME HERE
<<<<<<< HEAD

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
=======
    # screen.blit(pg.transform.scale(window, window.get_rect().size), (0, 0))
>>>>>>> 1e2cf0bac7b5a139d5f23c68ff6f154ed762ec0b
    pg.display.update()

def create_btn():
    pass

if __name__ == "__main__":
    main()

<<<<<<< HEAD



=======
>>>>>>> 1e2cf0bac7b5a139d5f23c68ff6f154ed762ec0b
