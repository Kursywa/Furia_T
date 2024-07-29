import pygame as pg
import ctypes
import ribosome as r
import RNA 

ctypes.windll.user32.SetProcessDPIAware() # workaround for windows, makes pg.display.set_mode apply 
#correct pixel ratio of the screen in windowed mode

pg.init()
width_of_window = 1920
height_of_window = 1000
main_window = pg.display.set_mode((width_of_window,height_of_window), pg.HWSURFACE|pg.DOUBLEBUF|pg.RESIZABLE)

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

    # flip() the display to put your work on screen
    pg.display.flip()

    clock.tick(60)  # limits FPS to 60


# game_status = "main page" / "instruction" / "game" / "result"
game_status = "game"
clock = pg.time.Clock()
running = True


width_of_nucleotide = 40
width_of_codon = 180

# create a small ribosome and scopes of APE sites
small_ribosome = r.Ribosome("./images/ribosome.png", 560, 200)
small_ribosome.siteP = (small_ribosome.rect.center[0] - (width_of_codon/2), small_ribosome.rect.center[0] + (width_of_codon/2))
small_ribosome.siteA = (small_ribosome.siteP[1], small_ribosome.siteP[1] + width_of_codon)
small_ribosome.siteE = (small_ribosome.siteP[0] - width_of_codon, small_ribosome.siteP[0])
small_ribosome.siteP

# create a large ribosome
large_ribosome = r.Ribosome("./images/ribosome.png", 600, 400)
large_ribosome.rect.move_ip(0, -200)

# get sequence TODO create fasta file with sequences and the header is the name of image of the structure
sequence = "ACGCGCGCAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
sequence_lenght = len(sequence)

# create a mRNA backbone
mRNA = RNA.RNABackbone("./images/mRNA.png", small_ribosome)

# Create a sprite.Group with first codon and set its position at the site P of small ribosome
codons = pg.sprite.Group()
AUG = RNA.Codon(sequence[:3], 0)
AUG.rect.bottomleft = (small_ribosome.siteP[0], small_ribosome.rect.top -10)
codons.add(AUG)

trna_object = RNA.TRNA("AUG")
        

while running:
    window.fill(window_color)

    for event in pg.event.get():  
        if event.type == pg.QUIT:  
           running = False
    
    if game_status == "game":
        # draw a ribosome
        window.blit(large_ribosome.image, large_ribosome.rect)
        window.blit(small_ribosome.image, small_ribosome.rect)
        # draw missing codons
        RNA.add_new_sprite_codons(codons,sequence, sequence_lenght, width_of_window)
        # draw mRNA and codons
        window.blit(mRNA.image, mRNA.rect)  
        codons.draw(window)
        # update position of mRNA and codons
        if False:
            mRNA.update()
            codons.update()
        
        pg.draw.line(window, (0 , 0, 255), (small_ribosome.siteP[0], small_ribosome.rect.center[1]), (small_ribosome.siteP[1], small_ribosome.rect.center[1]), 2)
        window.blit(trna_object.image, (805, 340))

    main_window.blit(pg.transform.scale(window, window.get_rect().size), (0, 0))
    pg.display.update()
    clock.tick(1)

def create_btn():
    pass

# if __name__ == "__main__":
#     main()

    # clock.tick(60)  # limits FPS to 60


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
    # screen.blit(pg.transform.scale(window, window.get_rect().size), (0, 0))
    pg.display.update()

def create_button(screen, x, y, button_width, button_height, font_size, button_text):
    pass

if __name__ == "__main__":
    main()


