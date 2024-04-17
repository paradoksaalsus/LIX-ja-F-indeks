import re

import docx
from estnltk import Text
from estnltk.taggers import SentenceTokenizer, VabamorfTagger


def main(path: str):
    # Load document
    doc = docx.Document(path);
    
    # Read text from paragraphs
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + " "
    text = text.strip()

    # Populate dictionary
    dict = {
        "A": 0,
        "C": 0,
        "D": 0,
        "G": 0,
        "H": 0,
        "I": 0,
        "J": 0,
        "K": 0,
        "N": 0,
        "O": 0,
        "P": 0,
        "S": 0,
        "U": 0,
        "V": 0,
        "X": 0,
        "Y": 0,
        "Z": 0,
    }

    corpus = Text(text).tag_layer(['words', 'sentences'])
    morph_tagger = VabamorfTagger()
    morph_tagger.tag(corpus)
    for t in corpus.morph_analysis:
        for iterable in t.annotations:
            dict.update({iterable.partofspeech: dict[iterable.partofspeech] + 1})

    print(path)
    print('---')
    getLIXIndex(text)
    getFormalityIndex(dict)
    getNomenclatureRatio(dict)
    print()

# LIX = A / B + (C x 100) / A
# A = sõnade arv
# B = lausete arv
# C = pikkade sõnade arv
def getLIXIndex(text):
    words = text
    words = re.sub(r'[(),0-9“.„:;§\-\–/”¹]', '', words, flags=re.MULTILINE) # Remove symbols and numbers from text
    words = Text(words).tag_layer(['words', 'tokens', 'compound_tokens'])
    A = len(words.words)
    print("A =", A);

    sentences = Text(text).tag_layer(['words'])
    sentences = SentenceTokenizer().tag(sentences)
    B = len(sentences.sentences)
    print("B =", B)

    long_words = {x for x in words.words.text if (len(x) >= 7)}
    C = len(long_words)
    print("C =", C)

    print("LIX =", A / B + (C * 100) / A)

# F = [(N + ADJ + ADP) - (V + ADV + INT + PRON) + 100] / 2
# N = nimisõnade sagedus        - S
# ADJ = omadussõnade sagedus    - A,C
# ADP = kaassõnade sagedus      - K
# V = tegusõnade sagedus        - V
# ADV = määrsõnade sagedus      - D
# INT = hüüdsõnade sagedus      - I
# PRON = asesõnade sagedus      - P
def getFormalityIndex(dict):
    N = dict['S']
    ADJ = dict['A'] + dict['C']
    ADP = dict['K']
    V = dict['V']
    ADV = dict['D']
    INT = dict['I']
    PRON = dict['P']

    print("N =", N)
    print("ADJ =", ADJ)
    print("ADP =", ADP)
    print("V =", V)
    print("ADV =", ADV)
    print("INT =", INT)
    print("PRON =", PRON)

    firstClause = N + ADJ + ADP
    secondClause = V + ADV + INT + PRON
    thirdClause = firstClause - secondClause + 100
    F = thirdClause / 2

    print("F =", F)

# N : V
# N = noomen - nimisõna
# V = verb   - tegusõna
def getNomenclatureRatio(dict):
    N = dict['S']
    V = dict['V']
    print("N : V =", N, ":", V)

main('kaustanimi/fail.laiend')
