import pygame as pg

def makenucleotide(nt):
    """
    Load an image of a nucleotide and create Rect object for it
    """
    nucleotide = pg.image.load(f"./images/{nt.lower()}_nucleo.png").convert_alpha()
    nucleotide = pg.transform.scale(nucleotide, (40,70))
    rect = nucleotide.get_rect()
    return nucleotide, rect

def create_triplet(sequence, size_of_image=(180,70)):
    """
    Create Surface with given nucleotides

    list_of_nucleotide_Rect - a list of tuples with position of bottomleft
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
    
    def __init__(self, sequence,number):
        """
        Create codon  with given nucleotides.
        self.image - Surface object that is drawn
        self.rect - Rect object with coordinates for self.image
        self.number - which triplet is it in the sequence
        """
        super().__init__()
        self.image = create_triplet(sequence)
        self.rect = self.image.get_rect()
        self.number = number

    
    def update(self):
        """
        Update position of the codon. If it is beyond to Pygame screen, it will be killed
        """
        self.rect.move_ip(-180, 0)
        if self.rect.right < 0:
            self.kill()



class RNABackbone(pg.sprite.Sprite):
    def __init__(self, name, small_ribosome):
        super().__init__()
        self.image = pg.image.load(name).convert()
        self.image = pg.transform.scale(self.image, (540,20))
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (small_ribosome.siteP.left - 10, small_ribosome.rect.top)
    
    def update(self):
        self.rect.move_ip(-180, 0)


def add_new_sprite_codons(codons, sequence, sequence_lenght, width_of_window):
    """
    Add new Codon objects to Group (codons)  
    """
    if codons:
        while True:
            last_sprite = codons.sprites()[-1]
            # check if there is space between last Codon and right side of the pygame screen
            # and if sequence is not finished
            if last_sprite.rect.left < width_of_window and (last_sprite.number * 3) != sequence_lenght:
                new_codon = Codon(sequence[3 * last_sprite.number +3: 3 * last_sprite.number + 6], last_sprite.number + 1)
                new_codon.rect.bottomleft = last_sprite.rect.bottomright
                codons.add(new_codon)
            else:
                break



def complementary_sequence(sequence):
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

    def __init__(self, sequence):
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
        self.rect.topleft = (1500, 200)
        self.codon = sequence
        #status start / moving / moved / site to site / empty
        self.status = 'start'
        self.startposition = self.rect.topleft

    def update(self):
        self.rect.move_ip(-180, 0)

