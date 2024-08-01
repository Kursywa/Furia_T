from random import randint, shuffle
import ctypes
import numpy as np
import pygame as pg
from game_objects import Ribosome, Codon, Aminoacid, \
TRNA, add_new_sprite_codons, OrderedGroup, Stopwatch, \
Cap
from fasta_parser import get_sequence_data


def main():
    ctypes.windll.user32.SetProcessDPIAware() # workaround for windows, makes pg.display.set_mode apply 
    #correct pixel ratio of the screen in windowed mode
    pg.init()
    width_of_window = 1920
    height_of_window = 1080
    window_color = (230, 230 , 250)
    window = pg.display.set_mode((width_of_window,height_of_window), pg.HWSURFACE|pg.DOUBLEBUF|pg.RESIZABLE)
    timer = Stopwatch()
    
    # game_status = "main page" / "instruction" / "game" / "result"
    game_status = "game"
    clock = pg.time.Clock()
    running = True

    width_of_nucleotide = 40
    height_of_nucleotide = 70
    width_of_codon = 180

    # create a small ribosome
    small_ribosome = Ribosome("./images/small_ribosome.png", width_of_window, height_of_window)
    small_ribosome.siteP = pg.Rect(small_ribosome.rect.center[0] - (width_of_codon/2), small_ribosome.rect.center[1] - 300, width_of_codon, 300)
    small_ribosome.siteA = pg.Rect(small_ribosome.siteP.right, small_ribosome.rect.center[1] - 300, width_of_codon, 300)
    small_ribosome.siteE = pg.Rect(small_ribosome.siteP.left - width_of_codon, small_ribosome.rect.center[1] - 300, width_of_codon, 300) 
    small_ribosome.codon_to_consider = 0 #  index of the codon that is considered  
    small_ribosome.first_tRNA = True # informs that first tRNA is not at site P
    small_ribosome.create_new_trna = True 
    small_ribosome.siteA_good = False # informs whether the tRNA was correctly selected for the codon in site A

    # create a large ribosome and set its position relative to small_ribosome
    large_ribosome = Ribosome("./images/big_ribosome.png", width_of_window, height_of_window)
    large_ribosome.rect.bottom = small_ribosome.rect.top + 20



    # get seqences from file. list_of_sequences is a list of tuples. Each tuple contains a header and a list of codons
    list_of_sequences = get_sequence_data("./seq1.fasta")
    idx = randint(0, len(list_of_sequences) - 1)
    header, sequence = list_of_sequences[idx]
    sequence_lenght = len(sequence)

    # Create a sprite.Group with first codon and set its position at the site P of small ribosome
    codons = OrderedGroup()
    # mRNA = OrderedGroup()

    #create group of tRNA
    group_of_trna = pg.sprite.Group()
    group_of_aa = pg.sprite.Group()

    # level of the game, user choose
    # 0 = one tRNA, 1 = 3 tRNA
    game_level = 1

    do = True 


    while running:
        window.fill(window_color)

        for event in pg.event.get():  
            if event.type == pg.QUIT:  
                running = False
                timer.stop_watch() ###

            elif event.type == pg.MOUSEBUTTONDOWN:
                if game_status == 'game':
                    game_mousebuttondown(group_of_trna, event)                                   
            
            elif event.type == pg.MOUSEBUTTONUP:
                if game_status == 'game' and small_ribosome.codon_to_consider != sequence_lenght:
                    game_mousebuttonup(group_of_trna, small_ribosome, sequence[small_ribosome.codon_to_consider])                

            elif event.type == pg.MOUSEMOTION:
                if game_status == 'game':
                    game_mousemotion(group_of_trna, event)
        
        if game_status == "game":
            
            if not small_ribosome.first_tRNA:
                # if tRNA at site A is correct, change position of codons, mRNA and tRNAs
                if small_ribosome.siteA_good:                   
                    codons.add_new(sequence)
                    codons.update_status()
                    group_of_trna.update()
                    group_of_aa.update()
                    small_ribosome.siteA_good = False
            # should be done only once
            elif do:
                cap = Cap((small_ribosome.siteP[0], small_ribosome.rect.center[1]))
                codons.add(cap)
                c = Codon(sequence[0],0, (small_ribosome.siteP[0], small_ribosome.rect.center[1]))
                codons.add(c)
                add_new_sprite_codons(codons,sequence, sequence_lenght, width_of_window)
                do = False
                timer.start_watch() ###

            if small_ribosome.create_new_trna:
                # create new tRNA and add it to group_of_trna
                createtrna(sequence, sequence_lenght, small_ribosome, group_of_trna, game_level, group_of_aa)

            movetrna(group_of_trna, small_ribosome)
            
            codons.update()

            window.blit(large_ribosome.image, large_ribosome.rect)
            window.blit(small_ribosome.image, small_ribosome.rect)
            codons.draw(window)
            group_of_trna.draw(window)
            group_of_aa.draw(window)
            # update position of mRNA and codons
            timer.display_current_spent_time(window)

        pg.display.update()
        clock.tick(60)

def game_mousebuttondown(group_of_trna, event):
    # if user clicked on tRNA, which is at starting position, tRNA will be able to follow the cursor
    for trna in group_of_trna:
                if trna.rect.collidepoint(event.pos) and trna.status == 'start':
                    trna.status = 'moving'

def game_mousebuttonup(group_of_trna, small_ribosome, sequence):
    # check if tRNA was dragged to site P or A of small_ribosome
    for trna in group_of_trna:
                if trna.status == 'moving' and sequence == trna.codon:
                    trna.checkcollision(small_ribosome, group_of_trna)
                    # if trna is not at right site, it comes back to starting position
                if trna.status == 'moving': 
                    trna.rect.topleft = trna.startingposition
                    trna.status = 'start' 
                    trna.aminoacid.set_position_relative_to_trna(trna.rect) 
                                   

def game_mousemotion(group_of_trna, event):
    # change position of tRNA that is being dragged by player
    for trna in group_of_trna:
                if trna.status == 'moving':
                    trna.rect.move_ip(event.rel)
                    trna.aminoacid.rect.move_ip(event.rel)

def givestartingposition(game_level):
    # depending on game level, it returns list of starting position 
    # thanks to shuffle() right tRNA is not always in the same position
    positions = {0: [(1500, 200)], 1: [(1500, 50), (1150, 100), (1450, 350)]}
    shuffle(positions[game_level])
    return positions[game_level]

def randomcodongenerator(codon, game_level):
    # depending on game level, it returns a list of codons for additional tRNAs
    nt = ['A', 'G', 'U', 'C']
    lst_random = []
    stop_codons = ['UAA', 'UAG', 'UGA']
    count = 0
    if game_level == 1:
        count = 2
    for i in range(count):
        
        while True:
            random_codon = ''
            random_codon += nt[randint(0,3)]
            random_codon += nt[randint(0,3)]
            random_codon += nt[randint(0,3)]
            if random_codon != codon and random_codon not in lst_random and random_codon not in stop_codons:
                break
        lst_random.append(random_codon)
    return lst_random

def createtrna(sequence, sequence_lenght, small_ribosome, group_of_trna, game_level, group_of_aa):
    # Number of created tRNA is depending on the game level
    if small_ribosome.codon_to_consider != sequence_lenght: 
        trna_to_create = randomcodongenerator(sequence[small_ribosome.codon_to_consider], game_level)
        list_of_positions = givestartingposition(game_level)
        aa = Aminoacid(sequence[small_ribosome.codon_to_consider])
        t = TRNA(sequence[small_ribosome.codon_to_consider], list_of_positions[0],aa)
        group_of_trna.add(t)
        group_of_aa.add(aa)

        for i in range(len(trna_to_create)):
            aa = Aminoacid(trna_to_create[i])
            t = TRNA(trna_to_create[i], list_of_positions[i+1], aa)
            group_of_aa.add(aa)
            group_of_trna.add(t)
    small_ribosome.create_new_trna = False

def movetrna(group_of_trna, small_ribosome):
    for trna in group_of_trna:
        trna.update_move(small_ribosome.siteE.left, small_ribosome.siteP.left)





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



if __name__ == "__main__":
    main()