import pygame as pg

class Codon(pg.sprite.Sprite):
    
    def makenucleotide(self, nt):
        nucleotide = pg.image.load(f"./images/{nt.lower()}.png").convert()
        nucleotide = pg.transform.scale(nucleotide, (40,70))
        rect = nucleotide.get_rect()
        return nucleotide, rect

    def __init__(self, sequence,number):
        super().__init__()
        n1, r1 = self.makenucleotide(sequence[0])
        r1.bottomleft = (10,70)
        n2, r2 = self.makenucleotide(sequence[1])
        r2.bottomleft = (70, 70)
        n3, r3 = self.makenucleotide(sequence[2])
        r3.bottomleft = (130,70)
        image = pg.Surface([180,70], pg.SRCALPHA)
        image.blit(n1, r1)
        image.blit(n2, r2)
        image.blit(n3, r3)
        pg.Surface.set_colorkey(image, "white")
        self.image = image
        self.rect = self.image.get_rect()
        self.number = number

    def update(self):
        self.rect.move_ip(-180, 0)
        if self.rect.right < 0:
            self.kill()



class RNABackbone(pg.sprite.Sprite):
    def __init__(self, name, small_ribosome):
        super().__init__()
        self.image = pg.image.load(name).convert()
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (small_ribosome.siteP[0] - 10, small_ribosome.rect.center[1])
    
    def update(self):
        self.rect.move_ip(-180, 0)


def add_new_sprite_codons(codons, sequence, sequence_lenght, width_of_window):
    if codons:
        while True:
            last_sprite = codons.sprites()[-1]
            if last_sprite.rect.left < width_of_window and (last_sprite.number * 3) != sequence_lenght:
                new_codon = Codon(sequence[3 * last_sprite.number : 3 * last_sprite.number + 3], last_sprite.number + 1)
                new_codon.rect.bottomleft = last_sprite.rect.bottomright
                codons.add(new_codon)
            else:
                break

