from random import randint, shuffle
import ctypes
import numpy as np
import yaml
'''needs to be installed -> in your environment use: >pip install pyyaml'''
import pygame as pg
from game_objects import Ribosome, Codon, Aminoacid, \
TRNA, add_new_sprite_codons, OrderedGroup, Stopwatch, \
Cap, Button, TextBox
from fasta_parser import get_sequence_data
from game import User, HighScores, Game


def main_menu():
    ctypes.windll.user32.SetProcessDPIAware() # workaround for windows, makes 
    # pg.display.set_mode apply correct pixel ratio of the screen in windowed mode
    pg.init()
    width_of_window = 1920
    height_of_window = 1080
    window = pg.display.set_mode((width_of_window,height_of_window),
     pg.HWSURFACE|pg.DOUBLEBUF|pg.RESIZABLE)

    screen_background_color = (230, 230 , 250)

    clock = pg.time.Clock()

    while True:
        window.fill(screen_background_color)
        menu_mouse_pos = pg.mouse.get_pos()

        play_btn = Button((width_of_window/2, height_of_window/4), "NOWA GRA")
        instruction_btn = Button((play_btn.x_pos, play_btn.y_pos + 100), "INSTRUKCJA GRY")
        highscores_btn = Button((play_btn.x_pos, play_btn.y_pos + 200), "NAJLEPSZE WYNIKI")
        settings_btn = Button((play_btn.x_pos, play_btn.y_pos + 300), "USTAWIENIA")
        quit_btn = Button((play_btn.x_pos, play_btn.y_pos + 400), "WYJŚCIE Z GRY")

        # drawing buttons
        for button in [play_btn, instruction_btn, highscores_btn, settings_btn, quit_btn]:
            button.change_color(menu_mouse_pos)
            button.update(window)

        # menu event handling
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if play_btn.check_for_input(menu_mouse_pos):
                    play_game(width_of_window, height_of_window, window, screen_background_color)
                if instruction_btn.check_for_input(menu_mouse_pos):
                    pass
                if highscores_btn.check_for_input(menu_mouse_pos):
                    pass
                if settings_btn.check_for_input(menu_mouse_pos):
                    pass
                if quit_btn.check_for_input(menu_mouse_pos):
                    pg.quit()
        pg.display.update()


def play_game(width_of_window, height_of_window, window, screen_background_color):

    width_of_nucleotide = 40
    height_of_nucleotide = 70
    width_of_codon = 180
    player_error_count = 0
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
    sequence_length = len(sequence)

    # Group that contains codons and utr5cap
    codons = OrderedGroup()

    #create groups for tRNAs and aminoacids
    group_of_trna = pg.sprite.Group()
    group_of_aa = pg.sprite.Group()

    # level of the game, user choose
    # 0 = one tRNA, 1 = 3 tRNA
    game_level = 1

    clock = pg.time.Clock()

    # start stopwatch
    timer = Stopwatch()
    # ensure that statement are done oly once in the first iteration of while loop
    do = True
    while True:
        window.fill(screen_background_color)
        if not small_ribosome.first_tRNA:
            # if tRNA at site A is correct, change position of codons,
            # tRNAs and aminoacids
            if small_ribosome.siteA_good:
                codons.add_new(sequence)
                codons.update_status()
                group_of_trna.update()
                group_of_aa.update()
                small_ribosome.siteA_good = False
                # only 7 codons can fit into the main screen, with the last one being on the site A,
                # so the loop breaks after reaching this number of codons in a sprite group
                if len(codons.sprites()) == 7:
                    timer.stop_watch()
                    save_highscore(timer.get_current_elapsed_time(),player_error_count,window, width_of_window, height_of_window)
                    break
        # should be done only once
        elif do:
            # Create cap and first codon. Time begins to be measured
            cap = Cap((small_ribosome.siteP[0], small_ribosome.rect.center[1]))
            codons.add(cap)
            c = Codon(sequence[0],0, (small_ribosome.siteP[0], \
                small_ribosome.rect.center[1]))
            codons.add(c)
            ####
            add_new_sprite_codons(codons,sequence, sequence_length, \
                width_of_window)
            do = False
            timer.start_watch() ###

        if small_ribosome.create_new_trna:
            # create new tRNA and add it to group_of_trna
            createtrna(sequence, sequence_length, small_ribosome, \
            group_of_trna, game_level, group_of_aa)
        # move tRNA from site to site or from  ribosome
        movetrna(group_of_trna, small_ribosome)
        # move codons
        codons.update()
        # draw game objects
        window.blit(large_ribosome.image, large_ribosome.rect)
        window.blit(small_ribosome.image, small_ribosome.rect)
        codons.draw(window)
        group_of_trna.draw(window)
        group_of_aa.draw(window)
        # update position of mRNA and codons
        # event handling
        for event in pg.event.get():
            if event.type == pg.QUIT:
                timer.reset_watch() ###
                pg.quit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                game_mousebuttondown(group_of_trna, event)
            elif event.type == pg.MOUSEBUTTONUP and \
                    small_ribosome.codon_to_consider != sequence_length:
                player_error_count = game_mousebuttonup(group_of_trna, small_ribosome,
                 sequence[small_ribosome.codon_to_consider], player_error_count)
            elif event.type == pg.MOUSEMOTION:
                game_mousemotion(group_of_trna, event)
        # updating screen
        timer.display_current_spent_time(window)
        display_player_error_count(window,player_error_count,width_of_window)
        clock.tick(60)
        pg.display.update()
    print("game ended")


def save_highscore(time,player_error_count,window,width_of_window,height_of_window):
    ''' functions draws onto the screen a final score screen which sums up player's
    points and prompts them to write their name. Name, current datetime and score is 
    saved to highscores.txt file'''
    highscores = HighScores()
    total_points = highscores.calculate_highscore(time,player_error_count)
    user_text = ' '
    running = True
    while running:
        window.fill('violet')
        save_highscores_mouse_pos = pg.mouse.get_pos()
        time_rect = Button((width_of_window/2,height_of_window/4), f"Twój czas: {time}", hovering_color = 'white')
        number_of_errors_rect = Button((time_rect.x_pos, time_rect.y_pos + 100), f"Twoja liczba błędów: {player_error_count}", hovering_color = 'white')
        total_score_rect = Button((time_rect.x_pos, time_rect.y_pos + 200), f"Punkty: {total_points}", hovering_color = 'white')
        accept_btn =  Button((width_of_window/1.25, height_of_window/1.5), f"OK")
        input_username = TextBox((time_rect.x_pos,time_rect.y_pos + 300), user_text)
        for button in [time_rect, number_of_errors_rect, total_score_rect, accept_btn]:
            button.change_color(save_highscores_mouse_pos)
            button.update(window)
        input_username.update_display(window)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if accept_btn.check_for_input(save_highscores_mouse_pos):
                    player = User(input_username.user_text)
                    highscores.check_and_add_highscore(total_points, player.username)
                    highscores.write_highscores()
                    main_menu()
                if input_username.check_collision(event.pos):
                    input_username.active = True
                else:
                    input_username.active = False
            if event.type == pg.KEYDOWN:
                # Check for backspace
                if event.key == pg.K_BACKSPACE:
                    # get text input from 0 to -1 i.e. end.
                    user_text = user_text[:-1]
                    input_username.update_text(user_text,window)
                # Unicode standard is used for string
                # formation
                else:
                    user_text += event.unicode
        pg.display.update()

def game_mousebuttondown(group_of_trna, event):
    # if user clicked on tRNA, which is at starting position, tRNA will be able to follow the cursor
    for trna in group_of_trna:
        if trna.rect.collidepoint(event.pos) and trna.status == 'start':
            trna.status = 'moving'


def game_mousebuttonup(group_of_trna, small_ribosome, sequence, player_error_count):
    # check if tRNA was dragged to site P or A of small_ribosome
    for trna in group_of_trna:
        if trna.status == 'moving':
            if sequence == trna.codon:
                trna.checkcollision(small_ribosome, group_of_trna)
            else:# incorrect position error handling
                if small_ribosome.siteA.colliderect(trna.rect):
                    # draw_error_message(window)
                    player_error_count += 1
            # if trna is not at right site, it comes back to starting position
        if trna.status == 'moving':
            trna.rect.topleft = trna.startingposition
            trna.status = 'start'
            trna.aminoacid.set_position_relative_to_trna(trna.rect)
    return player_error_count


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
            if random_codon != codon and random_codon not in lst_random \
                and random_codon not in stop_codons:
                break
        lst_random.append(random_codon)
    return lst_random


def createtrna(sequence, sequence_length, small_ribosome, group_of_trna, game_level, group_of_aa):
    # Number of created tRNA with aminoacid is depending on the game level
    if small_ribosome.codon_to_consider != sequence_length: 
        # return list of codons for additional tRNAS
        trna_to_create = randomcodongenerator(sequence[small_ribosome.codon_to_consider],
         game_level)
        # return list of positions for right and additional tRNAs
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


def draw_error_message(window):
    '''function draws big, red 'X' on the screen, which quickly fades.
    might add some error song'''


def display_player_error_count(surface, player_error_count,width_of_window):
    font = pg.font.SysFont('cambria', 50)
    error_text = font.render(f"Liczba błędów: {player_error_count}", True, "black")
    error_rect = error_text.get_rect()
    error_rect.topleft = (width_of_window/4,0)
    surface.blit(error_text, error_rect)


    
if __name__ == "__main__":
    pg.init()
    width_of_window = 1920
    height_of_window = 1080
    window = pg.display.set_mode((width_of_window,height_of_window),
     pg.HWSURFACE|pg.DOUBLEBUF|pg.RESIZABLE)
    save_highscore(time= 30,player_error_count = 3,window=window,width_of_window=width_of_window,height_of_window = height_of_window)
    #main_menu()
