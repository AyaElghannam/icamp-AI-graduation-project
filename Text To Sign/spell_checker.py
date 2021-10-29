from ar_corrector.corrector import Corrector
corr = Corrector()

def spell_checker(sentence):
    sentence = corr.contextual_correct(sentence)
    return sentence