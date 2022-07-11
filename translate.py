from googletrans import Translator

translator = Translator()


def to_en(words):
    translate = translator.translate(words, src='ru', dest='en')
    return translate.text


def to_de(words):
    translate = translator.translate(words, src='ru', dest='de')
    return translate.text


def to_pl(words):
    translate = translator.translate(words, src='ru', dest='pl')
    return translate.text


def to_es(words):
    translate = translator.translate(words, src='ru', dest='es')
    return translate.text


def to_fr(words):
    translate = translator.translate(words, src='ru', dest='fr')
    return translate.text


languages = ["English", "German", "Polish", "Spanish", "French"]
