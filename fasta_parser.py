
def _parse_file(file_name):
    '''function parsing a fasta file, where multiple fasta sequences are located.
    acts as a genererator that yields tuple of current sequence title and its nucleotide sequence'''
    
    with open(file_name , "rt", encoding = 'utf-8') as parser_file:
        sequence_title = ''
        sequence_data = ''
        for line in parser_file:
            line = line.strip()
            if line.startswith('>'):
                if sequence_title:
                    yield (sequence_title, sequence_data)
                    sequence_data = ''
                sequence_title = line  
            else:
                sequence_data = sequence_data + line
        yield (sequence_title, sequence_data)



def _parse_into_codons(sequence):
    ''' function parsing string sequences to a list of three letter codons'''

    codon_sequence = []
    x = 0
    while x < len(sequence):
        codon = ''
        for i in range(3):
            codon += sequence[x + 1]
        codon_sequence.append(codon)
        x += 3
    return codon_sequence


def get_sequence_data(file_name):
    ''' input -> file name in fasta format ; output -> a list of tuples, where each tuple consists
    of title and a list of codons. Referencing a single nucleotide in the sequence can be done via
    unpacking the tuple, and then iterating the list of codons as in 2d array. ex:
    for title, data in output:
        print(data[0][0])
        print(data[1][2])
    ^code above prints the first nucleotide in the sequence, and then the 5th one'''  

    sequence = []
    for title, data in _parse_file(file_name):
        sequence.append((title,_parse_into_codons(data)))
    return sequence     

__all__ = ['get_sequence_data']
