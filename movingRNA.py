import pygame as pg

pg.init()

width_of_window = 1920
height_of_window = 1000
main_window = pg.display.set_mode((width_of_window,height_of_window), pg.HWSURFACE|pg.DOUBLEBUF|pg.RESIZABLE)
window = main_window.copy()
window_color = (230, 230 , 250)


# game_status = "main page" / "instruction" / "game" / "result"
game_status = "game"

running = True



class SzkieletmRNA():
    def __init__(self):
        self.image = pg.image.load("./images/mRNA.png").convert()
        self.rect = self.image.get_rect()
        self.rect.topleft = 700, 800 






def run_game(window, mRNA):
    
    mRNA.rect.left -= 20

    
    window.blit(mRNA.image, mRNA.rect)
    x, y = mRNA.rect.topleft



ribosome = pg.image.load("./images/ribosome.png").convert()
pg.Surface.set_colorkey(ribosome, "white")
ribosome = pg.transform.scale(ribosome, (300,200))
rect_ribosome = ribosome.get_rect()
rect_ribosome.center = (int(main_window.get_width() // 2), int((main_window.get_height()//4) *3 ))

kodon_anticodon = False
mRNA = SzkieletmRNA()


while running:
    window.fill(window_color)

    for event in pg.event.get():  
        if event.type == pg.QUIT:  
           running = False
    if game_status == "game":
        window.blit(ribosome, rect_ribosome)
        run_game(window, mRNA)
    
    main_window.blit(pg.transform.scale(window, main_window.get_rect().size), (0, 0))
    pg.display.update()
    pg.time.delay(300)
    






