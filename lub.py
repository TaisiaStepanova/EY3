from nltk.corpus import wordnet
import json
import docx
import re
import pymorphy2


def read_from_doc(doc_name):  # с docx считать все обзацы
    doc = docx.Document(doc_name)
    text = []
    for paragraph in doc.paragraphs:
        for i in re.split("\.|!|\?| |,|:", paragraph.text):
            if len(i) < 2:
                continue
            text.append(i)
    return text


def save_dict(data):  # храним в json, надеюсь так можно
    with open('dict.json', 'w') as file:
        json.dump(data, file)


def read_dict():
    with open('dict.json', 'r') as file:
        dict = json.load(file)
        return dict


def create_dict(word):
    word_dict = {}
    synonyms = []
    antonyms = []
    for syn in wordnet.synsets(word):
        for l in syn.lemmas():
            synonyms.append(l.name())
            if l.antonyms():
                antonyms.append(l.antonyms()[0].name())

    hyponyms = []
    for syn in wordnet.synsets(word):
        for h in syn.hyponyms():
            hyponyms.append(h.name()[0:h.name().index('.')])

    hypernyms = []
    for syn in wordnet.synsets(word):
        for h in syn.hypernyms():
            hypernyms.append(h.name()[0:h.name().index('.')])

    synsets = wordnet.synsets(word)
    meronyms = []
    for synset in synsets:
        for meronym in synset.part_meronyms():
            for lemma in meronym.lemmas():
                meronyms.append(lemma.name())

    holonyms = []  # получаем холонимы
    for synset in synsets:
        for holonym in synset.member_holonyms():
            for lemma in holonym.lemmas():
                holonyms.append(lemma.name())

    word_dict['word'] = word
    word_dict['syn'] = synonyms
    word_dict['ant'] = antonyms
    word_dict['hypon'] = hyponyms
    word_dict['hyper'] = hypernyms
    word_dict['meron'] = meronyms
    word_dict['holon'] = holonyms

    return word_dict


def find_in_main_dict(main_dict, word):
    for dict in main_dict:
        if dict['word'] == word:
            return dict
    return False


def remove_from_main_dict(main_dict, word):
    for dict in main_dict:
        if dict['word'] == word:
            main_dict.remove(dict)
            return main_dict


def change_word_dict(main_dict,old_w ,param, new_w):  # param = ключ, значение
    for dict in main_dict:
        if dict['word'] == old_w:
            for i in range(len(dict[param[0]])):
                if dict[param[0]][i] == param[1]:
                    dict[param[0]][i] = new_w
                    return main_dict


def analize(main_dict, file):
    text = read_from_doc(file)
    for t in text:
        morph = pymorphy2.MorphAnalyzer()
        word = morph.parse(t)[0].normal_form
        if find_in_main_dict(main_dict, word) == False:
            main_dict.append(create_dict(word))

    main_dict = sorted(main_dict, key=lambda k: k['word'])
    return main_dict


# if __name__ == '__main__':
#     main_dict = []
#     main_dict = analize(main_dict)
#     print(main_dict)
#     save_dict(main_dict)