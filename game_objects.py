from math import floor
import pygame as pg
import time
import yaml

with open("./settings.yaml", "r") as file:
    images_dictionary = yaml.safe_load(file)


aa_dictionary = {
    'AUU': images_dictionary['ISOLEUCINE'], 'AUC': images_dictionary['ISOLEUCINE'], \
    'AUA': images_dictionary['ISOLEUCINE'], 'AUG': images_dictionary['METHIONINE'], \
    'ACU': images_dictionary['THREONINE'], 'ACC': images_dictionary['THREONINE'], \
    'ACA': images_dictionary['THREONINE'], 'ACG': images_dictionary['THREONINE'], \
    'AAU': images_dictionary['ASPARAGINE'], 'AAC': images_dictionary['ASPARAGINE'], \
    'AAA': images_dictionary['LYSINE'], 'AAG': images_dictionary['LYSINE'], \
    'AGU': images_dictionary['SERINE'], 'AGC': images_dictionary['SERINE'], \
    'AGA': images_dictionary['ARGININE'], 'AGG': images_dictionary['ARGININE'], \
    'CUU': images_dictionary['LEUCINE'], 'CUC': images_dictionary['LEUCINE'], \
    'CUA': images_dictionary['LEUCINE'], 'CUG': images_dictionary['LEUCINE'], \
    'CCU': images_dictionary['PROLINE'], 'CCC': images_dictionary['PROLINE'], \
    'CCA': images_dictionary['PROLINE'], 'CCG': images_dictionary['PROLINE'], \
    'CAU': images_dictionary['HISTIDINE'], 'CAC': images_dictionary['HISTIDINE'], \
    'CAA': images_dictionary['GLUTAMINE'], 'CAG': images_dictionary['GLUTAMINE'], \
    'CGU': images_dictionary['ARGININE'], 'CGC': images_dictionary['ARGININE'], \
    'CGA': images_dictionary['ARGININE'], 'CGG': images_dictionary['ARGININE'], \
    'GUU': images_dictionary['VALINE'], 'GUC': images_dictionary['VALINE'], \
    'GUA': images_dictionary['VALINE'], 'GUG': images_dictionary['VALINE'], \
    'GCU': images_dictionary['ALANINE'], 'GCC': images_dictionary['ALANINE'], \
    'GCA': images_dictionary['ALANINE'], 'GCG': images_dictionary['ALANINE'], \

    # change if aspartic_acid.png is added
    # 'GAU': images_dictionary['ASPARTIC_ACID'], 'GAC': images_dictionary['ASPARTIC_ACID'], \
    'GAU': images_dictionary['GLUTAMIC_ACID'], 'GAC': images_dictionary['GLUTAMIC_ACID'], \
    
    'GAA': images_dictionary['GLUTAMIC_ACID'], 'GAG': images_dictionary['GLUTAMIC_ACID'], \
    'GGU': images_dictionary['GLYCINE'], 'GGC': images_dictionary['GLYCINE'], \
    'GGA': images_dictionary['GLYCINE'], 'GGG': images_dictionary['GLYCINE'], \
    'UUU': images_dictionary['PHENYLALANINE'], 'UUC': images_dictionary['PHENYLALANINE'], \
    'UUA': images_dictionary['LEUCINE'], 'UUG': images_dictionary['LEUCINE'], \
    'UCU': images_dictionary['SERINE'], 'UCC': images_dictionary['SERINE'], \
    'UCA': images_dictionary['SERINE'], 'UCG': images_dictionary['SERINE'], \
    'UAU': images_dictionary['TYROSINE'], 'UAC': images_dictionary['TYROSINE'], \
    'UGU': images_dictionary['CYSTEINE'], 'UGC': images_dictionary['CYSTEINE'], \
    'UGG': images_dictionary['TRYPTOPHAN']
}

# list of motion vectors for aminoacid in polypeptide chain
polypeptide_position = [(-25, -30),(-25, -30),(-25, -30),(-30, -30),  \
(-20,-40), (-20,-40),(-20,-40),(-40,-40), (-40, -40), (-40, -40), (-50, -30), (-50, -30) ]



class Ribosome(pg.sprite.Sprite):
    
    def __init__(self, name,  width_of_window, height_of_window):
        """
        Create Surface object of the ribosome and its Rect object
        """
        super().__init__()
        self.image = pg.image.load(name).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (int(width_of_window // 2), int((height_of_window//5) *4 ))



def makenucleotide(nt):
    """
    Load an image of given nucleotide and create Rect object for it
    nt - a letter for nucleotide 
    """
    nucleotide = pg.image.load(images_dictionary[f'{nt}_NORMAL']).convert_alpha()
    rect = nucleotide.get_rect()
    return nucleotide, rect

def create_triplet(sequence):
    """
    Create and return Surface object with given nucleotides

    """
    list_of_positions = [(10,70), (70,70), (130,70)]
    image = pg.Surface((180,70), pg.SRCALPHA)
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
        self.status - informs if Codon can move
        self.distance - how far it has already moved
        """
        super().__init__()
        triplet = create_triplet(sequence)
        rect_triplet = triplet.get_rect()
        backbone = pg.image.load(images_dictionary['MRNA']).convert_alpha()
        rect_backbone = backbone.get_rect()
        image = pg.Surface([180, 80], pg.SRCALPHA)
        image.blit(backbone, (0, 60))
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
        """
        Methos moves codon by 5px to the left.
        if codon has moved by its own width, its status will be changed.
        """
        if self.status == self.MOVING:
            self.rect.move_ip(-5,0)
            self.distance += 5
            if self.distance == 180:
                self.status = self.STILL
                self.distance = 0


# this class is created to work with sprite.Group of codons
class OrderedGroup(pg.sprite.Group):
    def __init__(self):
        super().__init__()
        # store the last added sprite
        self.last_sprite = None
    
    def add(self, *sprite):
        """
        Method adds new sprite to group and keep information of last added sprite.
        """
        super().add(*sprite)
        if sprite:
            self.last_sprite = sprite[-1]
    
    def add_new(self, sequence):
        """
        Methods adds new codon if last_sprite wasn't the last codon 
        in the sequence.

        sequence - list of sequence's codons
        """
        if self.last_sprite.number != (len(sequence) -1):
            c = Codon(sequence[self.last_sprite.number + 1], self.last_sprite.number + 1, self.last_sprite.rect.bottomright)
            self.add(c)
    
    def update_status(self):
        """
        Method performs .update_status() on every codon in group
        """
        for sprite in self.sprites():
            sprite.update_status()

class Cap(pg.sprite.Sprite):
    STILL = 'still'
    MOVING = 'moving'
    def __init__(self, position):
        """
        self.status - informs if Codon can move
        self.distance - how far it has already moved
        """
        super().__init__()
        self.image = pg.image.load(images_dictionary['MRNA_CAP']).convert_alpha()
        self.rect = self.image.get_rect(bottomright=position)
        self.rect.move_ip(0, 5)
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
        """
        Methos moves codon by 5px to the left.
        if cap has moved by codon's width, its status will be changed.
        """
        if self.status == self.MOVING:
            self.rect.move_ip(-5,0)
            self.distance += 5
            if self.distance == 180:
                self.status = self.STILL
                self.distance = 0


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


class Aminoacid(pg.sprite.Sprite):
    def __init__(self, sequence):
        super().__init__()
        self.image = pg.image.load(aa_dictionary[sequence]).convert_alpha()
        self.rect = self.image.get_rect()
        self.withtrna = True
        # informs about position in polypeptide position
        self.position_in_chain = -1
    
    def set_position_relative_to_trna(self, position_of_trna):
        """ method ensures that aa is next to tRNA """
        self.rect.bottomright = (position_of_trna.right -10, position_of_trna.top + 20)

    def update(self):
        """ method changes position in polypeptide chain """
        if not self.withtrna:
            self.position_in_chain += 1
            self.rect.move_ip(polypeptide_position[self.position_in_chain][0], polypeptide_position[self.position_in_chain][1])

        


class TRNA(pg.sprite.Sprite):
    START = 'start'
    MOVING = 'moving'
    MOVED = 'moved'
    SITETOSITE = 'sitetosite'
    EXIT = 'exit'
    FIRST = 'first'

    def __init__(self, sequence, position, aa):
        """
        create tRNA object 
        
        sequence - codon on the basis of which the anticodon is to be created
        position - the starting position
        aa - Sprite object of aminoacid for this tRNA

        """
        super().__init__()
        image_tRNA = pg.image.load(images_dictionary['TRNA']).convert_alpha()
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
        # status start (tRNA at starting position) / moving (user drags tRNA) / 
        # moved (tRNA is in ribosome) / site to site (tRNA is moving to the next side ) / exit 
        self.status = self.START
        # keep topleft coordinate of starting position
        self.startingposition = self.rect.topleft # 
        self.aminoacid = aa
        self.aminoacid.set_position_relative_to_trna(self.rect)

    def update(self):
        """
        Update position of the codon. If it is still in starting position, 
        it will be killed with its aminoacid
        """
        if self.status == self.START:
            self.kill()
            self.aminoacid.kill()
        elif self.status == self.MOVED:
            self.status = self.SITETOSITE
              
    def update_move(self, leftE, leftP):  
        """
        Method handles the movement of tRNA from one site to another and 
        leaving the ribosome
        """

        # if tRNA is at the site E, it starts leaving ribosome and disappearing
        if self.status == self.EXIT:
            self.rect.move_ip(-5,-2)
            self.image.set_alpha( self.image.get_alpha() - 5)
            if self.rect.left < leftE - 500:
                self.kill() 
        elif self.status == self.SITETOSITE:
            if self.aminoacid :
                if self.rect.left == leftP:                    
                    self.aminoacid.withtrna = False
                    self.aminoacid.update()
                    self.aminoacid = None
                else:                   
                    self.aminoacid.rect.move_ip(-5,0)
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
                self.aminoacid.set_position_relative_to_trna(self.rect) 
                self.aminoacid.withtrna = False
                self.aminoacid = None    
        # instructions for another tRNAs   
        else:
            if small_ribosome.siteA.colliderect(self.rect):
                self.rect.bottomleft = (small_ribosome.siteA.left, small_ribosome.siteP.bottom - 60)
                self.status = self.MOVED
                small_ribosome.siteA_good = True
                small_ribosome.create_new_trna = True
                small_ribosome.codon_to_consider += 1
                self.aminoacid.set_position_relative_to_trna(self.rect) 
                

        

   
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
            self.elapsed_time += time.time() - self.start_time
            self.is_running = False

    def reset_watch(self):
        self.elapsed_time = 0
        self.is_running = False

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
        minutes = floor(in_time/60)
        seconds = in_time % 60
        
        # a  bit hardcoded
        font = pg.font.SysFont('cambria', 50)
        timer_text = font.render(f"Czas: {minutes:02d}:{seconds:02d}", True, "black")
        timer_rect = timer_text.get_rect()
        timer_rect.top = 0
        timer_rect.left = 0
        surface.blit(timer_text, timer_rect)

class Button():
    def __init__(self,  pos, text_input, image = None, font = None,
                base_color = pg.Color(('#FFFFFF')), hovering_color = pg.Color(('#66ff66'))):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        if self.font is None:
            self.font = pg.font.SysFont(None,50)
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def check_for_input(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and \
        position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def change_color(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and \
            position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)
