from math import floor
import pygame as pg
import time


class Ribosome(pg.sprite.Sprite):
    
    def __init__(self, name, width, height, width_of_window, height_of_window):
        """
        Create Surface object of the ribosome and its Rect object
        """
        pg.sprite.Sprite.__init__(self)
        ribosome = pg.image.load(name).convert_alpha()
        self.image = pg.transform.scale(ribosome, (width,height))
        self.rect = self.image.get_rect()
        self.rect.center = (int(width_of_window // 2), int((height_of_window//5) *4 ))



def makenucleotide(nt, size_of_image=(40,70)):
    """
    Load an image of given nucleotide and create Rect object for it
    nt - a letter for nucleotide 
    size_of_image - a size of returned Surface object
    """
    nucleotide = pg.image.load(f"./images/{nt.lower()}_nucleo.png").convert_alpha()
    nucleotide = pg.transform.scale(nucleotide, size_of_image)
    rect = nucleotide.get_rect()
    return nucleotide, rect

def create_triplet(sequence, size_of_image=(180,70)):
    """
    Create and return Surface object with given nucleotides

    size_of_image - a size of returned Surface object
    """
    list_of_positions = [(10,70), (70,70), (130,70)]
    image = pg.Surface(size_of_image, pg.SRCALPHA)
    for i in range(3):
        nucleotide, rect = makenucleotide(sequence[i])
        rect.bottomleft = list_of_positions[i]
        image.blit(nucleotide, rect)
    return image



class Codon(pg.sprite.Sprite):
    STILL = 'still'
    MOVING = 'moving'
    def __init__(self, sequence,number, position_bottomleft):
        """
        Create codon with given nucleotides.
        self.image - Surface object that is drawn
        self.rect - Rect object with coordinates for self.image
        self.number - which triplet is it in the sequence
        """
        super().__init__()
        triplet = create_triplet(sequence)
        rect_triplet = triplet.get_rect()
        backbone = pg.image.load("./images/mRNA.png").convert_alpha()
        backbone = pg.transform.scale(backbone, (180,20))
        rect_backbone = backbone.get_rect()
        image = pg.Surface([180, 80], pg.SRCALPHA)
        image.blit(backbone, (0, 70))
        image.blit(triplet, (0, 0))
        self.image = image
        self.rect = self.image.get_rect(bottomleft=position_bottomleft)
        self.number = number
        self.status = self.STILL
        self.distance = 0

    def update_status(self):
        """
        Update position of the codon. If it is beyond to Pygame screen, it will be killed
        """
        if self.status == self.STILL:
            self.status = self.MOVING
        if self.rect.right < 0:
            self.kill()
    
    def update(self):
        if self.status == 'moving':
            self.rect.move_ip(-5,0)
            self.distance += 5
            if self.distance == 180:
                self.status = 'still'
                self.distance = 0

class OrderedGroup(pg.sprite.Group):
    def __init__(self):
        super().__init__()
        self.last_sprite = None
    
    def add(self, *sprite):
        super().add(*sprite)
        if sprite:
            self.last_sprite = sprite[-1]
    
    def add_new(self, sequence):
        if self.last_sprite.number != (len(sequence) -1):
            c = Codon(sequence[self.last_sprite.number + 1], self.last_sprite.number + 1, self.last_sprite.rect.bottomright)
            self.add(c)
    
    def update_status(self):
        for sprite in self.sprites():
            sprite.update_status()



def add_new_sprite_codons(codons, sequence, sequence_lenght, width_of_window):
    """
    Add new Codon objects to Group (codons)  
    """
    if codons:
        while True:
            last_sprite = codons.sprites()[-1]
            # check if there is space between last Codon and right side of the pygame screen
            # and if last_sprite is not the last codon in sequence
            if last_sprite.rect.left < width_of_window and last_sprite.number  != (sequence_lenght-1):
                new_codon = Codon(sequence[last_sprite.number + 1 ], last_sprite.number + 1, last_sprite.rect.bottomright)
                codons.add(new_codon)
            else:
                break

def complementary_sequence(sequence):
    """
    Function returns a complementary sequence to a given sequence
    """
    s = ""
    for i in sequence:
        if i == "A":
            s += "U"
        elif i == "U":
            s += "A"
        elif i == "G":
            s += "C"
        else:
            s +=  "G"
    return s



class TRNA(pg.sprite.Sprite):
    START = 'start'
    MOVING = 'moving'
    MOVED = 'moved'
    SITETOSITE = 'sitetosite'
    EXIT = 'exit'
    FIRST = 'first'

    def __init__(self, sequence, position):
        """
        create tRNA object 
        """
        super().__init__()
        image_tRNA = pg.image.load("./images/trna.png").convert_alpha()
        complementary = complementary_sequence(sequence)
        image_anticodon = create_triplet(complementary)
        image_anticodon = pg.transform.flip(image_anticodon, False, True)
        image = pg.Surface([360,300], pg.SRCALPHA)
        image.blit(image_tRNA, (0,0))
        image.blit(image_anticodon, (0, 230))
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = position 
        self.codon = sequence
        #status start (tRNA at starting position) / moving (user drags tRNA) / moved (tRNA is in ribosome) / site to site / exit. 
        self.status = self.START
        self.lastposition = self.rect.topleft # position before changing it

    def update(self):
        if self.status == self.START:
            self.kill()
        elif self.status == self.MOVED:
            self.status = self.SITETOSITE
              
    def update_move(self, leftE, leftP):  
        # if tRNA is at the site E, it starts leaving ribosome and disappearing
        if self.status == self.EXIT:
            self.rect.move_ip(-5,-2)
            self.image.set_alpha( self.image.get_alpha() - 5)
            if self.rect.left < leftE - 500:
                self.kill() 
        elif self.status == self.SITETOSITE:
            self.rect.move_ip(-5,0)
            if self.rect.left == leftE or self.rect.left == leftP:
                if self.rect.left == leftE:
                    self.status = self.EXIT
                else:
                    self.status = self.MOVED

    def checkcollision(self, small_ribosome, group_of_trna):
    # check collision of trna and siteA or site P, if True, trna.status will be changed
        # instructions when first tRNA is dragged
        if small_ribosome.first_tRNA:
            if small_ribosome.siteP.colliderect(self.rect):
                self.rect.bottomleft = (small_ribosome.siteP.left, small_ribosome.siteP.bottom - 60)
                self.status = self.FIRST
                small_ribosome.first_tRNA = False
                small_ribosome.codon_to_consider = 1
                small_ribosome.create_new_trna = True
                group_of_trna.update()
                self.status = self.MOVED
        # instructions for another tRNAs   
        else:
            if small_ribosome.siteA.colliderect(self.rect):
                self.rect.bottomleft = (small_ribosome.siteA.left, small_ribosome.siteP.bottom - 60)
                self.status = self.MOVED
                small_ribosome.siteA_good = True
                small_ribosome.create_new_trna = True
                small_ribosome.codon_to_consider += 1

        

   
class Stopwatch:
    ''' class made for handling a stopwatch. Should be used mainly in core 
    gameloop to track player's time spent on a given sequence or level'''

    def __init__(self):
        self.start_time = None
        self.elapsed_time = 0
        self.is_running = False
    
    def start_watch(self):
        if not self.is_running:
            self.start_time = time.time()
            self.is_running = True

    def stop_watch(self):
        if self.is_running:
            self.elapsed_time = time.time() - self.start_time
            self.is_running = False

    def reset_watch(self):
        self.elapsed_time = 0
        self.is_running = 0

    def get_current_elapsed_time(self):
        '''method returns current elapsed time'''
        total_time = self.elapsed_time
        if self.is_running:
            total_time += time.time() - self.start_time
        return round(total_time)

    def display_current_spent_time(self, surface, in_time = None):
        '''method draws current elapsed time on a surface provided as argument in the top-left corner of the screen'''
        if in_time is None:
            in_time = self.get_current_elapsed_time()
        # need to refactor this bit
        minutes = floor(in_time/60)
        if minutes < 10:
            minutes = "0" + str(minutes) #conversion of 'minutes' variable from int to string might cause issues
            # - using both variable types???
        seconds = in_time % 60
        if seconds < 10:
            seconds = "0" + str(seconds)
        
        # a  bit hardcoded
        font = pg.font.SysFont('cambria', 50)
        timer_text = font.render(f"Czas: {minutes}:{seconds}", True, "black")
        timer_rect = timer_text.get_rect()
        timer_rect.top = 0
        timer_rect.left = 0
        surface.blit(timer_text, timer_rect)