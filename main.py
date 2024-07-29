import pygame as pg
import ctypes
import ribosome as r
import RNA 

ctypes.windll.user32.SetProcessDPIAware() # workaround for windows, makes pg.display.set_mode apply 
#correct pixel ratio of the screen in windowed mode

pg.init()

# main_window.blit(pg.transform.scale(window, window.get_rect().size), (0, 0))
# pg.display.update()


def main():
    width_of_window = 1920
    height_of_window = 1000
    main_window = pg.display.set_mode((width_of_window,height_of_window), pg.HWSURFACE|pg.DOUBLEBUF|pg.RESIZABLE)
    window = main_window.copy()
    window_color = (230, 230 , 2)
    clock = pg.time.Clock()

    # game_status = "main page" / "instruction" / "game" / "result"
    game_status = "game"
    running = True


    width_of_nucleotide = 40
    width_of_codon = 180

    # create a small ribosome and scopes of APE sites
    small_ribosome = r.Ribosome("./images/ribosome.png", 560, 200)
    small_ribosome.siteP = (small_ribosome.rect.center[0] - (width_of_codon/2), small_ribosome.rect.center[0] + (width_of_codon/2))
    small_ribosome.siteA = (small_ribosome.siteP[1], small_ribosome.siteP[1] + width_of_codon)
    small_ribosome.siteE = (small_ribosome.siteP[0] - width_of_codon, small_ribosome.siteP[0])

    # create a large ribosome
    large_ribosome = r.Ribosome("./images/ribosome.png", 600, 400)
    large_ribosome.rect.move_ip(0, -200)

    # create a mRNA backbone
    mRNA = RNA.RNABackbone("./images/mRNA.png", small_ribosome)

    # get sequence TODO create fasta file with sequences and the header is the name of image of the structure
    sequence = "ACGCGCGCAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
    sequence_lenght = len(sequence)

    # Create a sprite.Group with first codon and set its position at the site P of small ribosome
    codons = pg.sprite.Group()
    AUG = RNA.Codon(sequence[:3], 0)
    AUG.rect.bottomleft = (small_ribosome.siteP[0], small_ribosome.rect.top -10)
    codons.add(AUG)

    while running:
        window.fill(window_color)

        for event in pg.event.get():  
            if event.type == pg.QUIT:  
                running = False
        
        if game_status == "game":
            
            window.blit(large_ribosome.image, large_ribosome.rect)
            window.blit(small_ribosome.image, small_ribosome.rect)
            mRNA.update()
            window.blit(mRNA.image, mRNA.rect)  
            codons.update()
            RNA.add_new_sprite_codons(codons,sequence, sequence_lenght, width_of_window)
            codons.draw(window)
            print(codons)
            pg.draw.line(window, (0 , 0, 255), (small_ribosome.siteP[0], small_ribosome.rect.center[1]), (small_ribosome.siteP[1], small_ribosome.rect.center[1]), 2)

        main_window.blit(pg.transform.scale(window, window.get_rect().size), (0, 0))
        pg.display.update()
        clock.tick(1)


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





        
def create_btn():
    pass

if __name__ == "__main__":
    main()