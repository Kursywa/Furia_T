import pygame as pg
import ctypes
import ribosome as r
import RNA 

ctypes.windll.user32.SetProcessDPIAware() # workaround for windows, makes pg.display.set_mode apply 
#correct pixel ratio of the screen in windowed mode

pg.init()

def main():

    width_of_window = 1920
    height_of_window = 1000
    window_color = (230, 230 , 250)
    window = pg.display.set_mode((width_of_window,height_of_window), pg.HWSURFACE|pg.DOUBLEBUF|pg.RESIZABLE)
    
    
    # game_status = "main page" / "instruction" / "game" / "result"
    game_status = "game"
    clock = pg.time.Clock()
    running = True


    width_of_nucleotide = 40
    height_of_nucleotide = 70
    width_of_codon = 180

    # create a small ribosome and Rect objects forAPE sites
    small_ribosome = r.Ribosome("./images/ribosome.png", 560, 200, width_of_window, height_of_window)
    small_ribosome.siteP = pg.Rect(small_ribosome.rect.center[0] - (width_of_codon/2), small_ribosome.rect.top - 300, 180, 300)
    small_ribosome.siteA = pg.Rect(small_ribosome.siteP.right, small_ribosome.rect.top - 300, 180, 300)
    small_ribosome.siteE = pg.Rect(small_ribosome.siteP.left + 180, small_ribosome.rect.top - 300, 180, 300) 
    small_ribosome.nt_index_at_siteA = None
    small_ribosome.first_tRNA = True
    small_ribosome.create_new_trna = False
    small_ribosome.siteA_good = False

    # create a large ribosome
    large_ribosome = r.Ribosome("./images/ribosome.png", 600, 400,width_of_window, height_of_window)
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

    #create group of tRNA
    group_of_trna = pg.sprite.Group()
    group_of_trna.add(RNA.TRNA(sequence[:3]))
    


    def game_mousebuttondown(group_of_trna):
        for trna in group_of_trna:
                    if trna.rect.collidepoint(event.pos) and trna.status == 'start':
                        trna.status = 'moving'

    def checkcollision(trna, small_ribosome):
        # check collision of trna and siteA or site P
        if small_ribosome.first_tRNA:
            if small_ribosome.siteP.colliderect(trna.rect):
                trna.rect.bottomleft = (small_ribosome.siteP.left, small_ribosome.siteP.bottom - 70)
                trna.status = 'moved'
                small_ribosome.first_tRNA = False
                small_ribosome.nt_index_at_siteA = 3
                small_ribosome.create_new_trna = True
                
        else:
            if small_ribosome.siteA.colliderect(trna.rect):
                trna.rect.bottomleft = (small_ribosome.siteA.left, small_ribosome.siteP.bottom - 70)
                trna.status = 'moved'
                small_ribosome.siteA_good = True
                small_ribosome.create_new_trna = True


    def game_mousebuttonup(group_of_trna, small_ribosome):
        for trna in group_of_trna:
                    if trna.status == 'moving':
                        checkcollision( trna, small_ribosome)
                        # if trna is not at right site, it comes back to start position
                        if trna.status == 'moving': 
                            trna.rect.topleft = trna.startposition
                            trna.status = 'start'                       

    def game_mousemotion(group_of_trna):
        for trna in group_of_trna:
                    if trna.status == 'moving':
                        trna.rect.move_ip(event.rel)

        

    while running:
        window.fill(window_color)

        for event in pg.event.get():  
            if event.type == pg.QUIT:  
                running = False

            elif event.type == pg.MOUSEBUTTONDOWN:
                if game_status == 'game':
                    game_mousebuttondown(group_of_trna)                                   
            
            elif event.type == pg.MOUSEBUTTONUP:
                if game_status == 'game':
                    game_mousebuttonup(group_of_trna, small_ribosome)                

            elif event.type == pg.MOUSEMOTION:
                if game_status == 'game':
                    game_mousemotion(group_of_trna)
        
        if game_status == "game":
            
            #draw a ribosome
            window.blit(large_ribosome.image, large_ribosome.rect)
            window.blit(small_ribosome.image, small_ribosome.rect)
            # draw missing codons
            RNA.add_new_sprite_codons(codons,sequence, sequence_lenght, width_of_window)
            # draw mRNA and codons
            window.blit(mRNA.image, mRNA.rect)  
            codons.draw(window)
            group_of_trna.draw(window)
            # update position of mRNA and codons

            if small_ribosome.nt_index_at_siteA:
                
                if small_ribosome.create_new_trna:
                    group_of_trna.add(RNA.TRNA(sequence[small_ribosome.nt_index_at_siteA:small_ribosome.nt_index_at_siteA + 3]))
                    small_ribosome.create_new_trna = False
                    small_ribosome.nt_index_at_siteA += 3
                
                if small_ribosome.siteA_good:                   
                    mRNA.update()
                    codons.update()
                    group_of_trna.update()
                    small_ribosome.siteA_good = False
                
        # pg.draw.line(window, (0 , 0, 255), (small_ribosome.siteP[0], small_ribosome.rect.center[1]), (small_ribosome.siteP[1], small_ribosome.rect.center[1]), 2)   

        # main_window.blit(pg.transform.scale(window, window.get_rect().size), (0, 0))
        pg.display.update()
        clock.tick(60)


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