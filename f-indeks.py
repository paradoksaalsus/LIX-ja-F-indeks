from estnltk import Text

file = open("fail.txt", "r", encoding="utf-8")

fileText = []

for x in file:
    fileText.append(x)

corpus = [Text(t).tag_layer(['morph_analysis']) for t in fileText]

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

for text in corpus:
    for word in text.morph_analysis:
        for iterable in word.annotations:
            dict.update({iterable.partofspeech: dict[iterable.partofspeech] + 1})
print(dict)