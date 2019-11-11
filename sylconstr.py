'''     SYLLABLE CONSTRUCTOR       '''

# Imports and sets up IPA information from IPA.py
import IPA
import helpers

# Reads in phonemes file and rules file
def readInRules(phonemefile, rulesfile):
    phonemes = (' '.join([line.strip() for line in open(phonemefile)])).split(' ')
    sylrules = [line.strip().split('|') for line in open(rulesfile)]
    IPA_info = IPA.readInIPA()[:4]
    return phonemes, sylrules, IPA_info

def generateRules(rule):
    rules = []
    onsets = rule[0].split(';')
    nucleus = rule[1].split(';')
    codas = rule[2].split(';')
    indexes = [0,0,0]
    maxindexes = [len(onsets)-1, len(nucleus)-1, len(codas)-1]
    max = False
    while not max:
        newrule = ''
        if len(onsets[indexes[0]]) > 0:
            newrule += onsets[indexes[0]]+' '
        newrule += nucleus[indexes[1]]
        if len(codas[indexes[2]]) > 0:
            newrule += ' '+codas[indexes[2]]
        rules.append(newrule)
        indexes, max = helpers.increment(indexes,maxindexes)
    return rules

def sylsFromRule(phonemes,rule,IPA_info):
    # Sets up arrays
    syls = []
    phonsets = []
    indexes = []
    maxindexes = []
    max = False
    # Creates phoneme sets based on rules and input phonemes
    rule = rule.split(' ')
    for sylele in rule:
        allphons = IPA.findSet(sylele,IPA_info)
        phonset = IPA.filterPhonemes(phonemes,allphons)
        phonsets.append(phonset)
    # Creates index arrays to keep track of phoneme set indexes
    for sylele in phonsets:
        indexes.append(0)
        maxindexes.append(len(sylele)-1)
    # Iterates through all possib   le combinations of syllables based on phoneme sets and order, using indexes array to
    #       keep track of position within the phoneme sets
    while not max:
        syl = ''
        for l in range(len(phonsets)):
            syl += phonsets[l][indexes[l]]
        syls.append(syl)
        indexes, max = helpers.increment(indexes,maxindexes)
    return syls

# Constructs all syllables given input phonemes and rule file and writes to output file
def constructSyls(dir):
    outfile = dir + "/outputs/syllables.txt"
    phonemefile = dir + "/inputs/phonemes.txt"
    rulesfile = dir + "/inputs/sylstructs.txt"
    phonemes, sylrules, IPA_info = readInRules(phonemefile,rulesfile)
    sylset = []
    newrules = []
    for rule in sylrules:
        newrules += generateRules(rule)
    for rule in newrules:
        sylset += sylsFromRule(phonemes,rule,IPA_info)
    out = open(outfile,'w')
    out.write('\n'.join(sylset))
    out.close()


if __name__ == "__main__":
    constructSyls('L1')