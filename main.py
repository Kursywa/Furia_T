import pygame as pg
import ctypes
ctypes.windll.user32.SetProcessDPIAware() # workaround for windows, makes pg.display.set_mode apply 
#correct pixel ratio of the screen in windowed mode

pg.init()
width_of_window = 1920
height_of_window = 1000
main_window = pg.display.set_mode((width_of_window,height_of_window), pg.HWSURFACE|pg.DOUBLEBUF|pg.RESIZABLE)
# window = main_window.copy()
# main_window.blit(pg.transform.scale(window, window.get_rect().size), (0, 0))
# pg.display.update()

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
    # screen.blit(pg.transform.scale(window, window.get_rect().size), (0, 0))
    pg.display.update()

def create_btn():
    pass

if __name__ == "__main__":
    main()

