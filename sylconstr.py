'''     SYLLABLE CONSTRUCTOR       '''

# Imports and sets up IPA information from IPA.py
import IPA
import helpers
import sys

# Reads in phonemes file and rules file
def readInRules(phonemefile, rulesfile):
    IPA_info = IPA.readInIPA()[:4]
    abort = False
    try:
        phonemes = (' '.join([line.strip() for line in open(phonemefile) if line.strip() != ''])).split(' ')
    except IOError:
        print("Phonemes file not found")
        abort = True
    try:
        sylrules = [line.strip().split('|') for line in open(rulesfile) if line.strip() != '']
    except IOError:
        print("Syllable rule file not found")
        abort = True
    if abort == True:
        sys.exit()
    return phonemes, sylrules, IPA_info

def generateRules(rule,IPA_info):
    rules = []
    # Sets up onset, nucelus, and coda lists
    onsets = rule[0].split(';')
    nucleus = rule[1].split(';')
    codas = rule[2].split(';')
    # Sets up indexes for loop, see increment in helpers.py for loop explanation
    indexes = [0,0,0]
    maxindexes = [len(onsets)-1, len(nucleus)-1, len(codas)-1]
    max = False
    while not max:
        ignoreRule = False
        newrule = ''
        if len(onsets[indexes[0]]) > 0:
            newrule += onsets[indexes[0]]+' '
        newrule += nucleus[indexes[1]]
        if len(codas[indexes[2]]) > 0:
            newrule += ' '+codas[indexes[2]]
        # Checks if rules are both valid and noncontradicting
        for item in newrule.split(' '):
            isvalid = helpers.validPhonemeSet(item,IPA_info)
            if isvalid == 2:
                print("Rule",newrule,"will be ignored.")
                ignoreRule = True
            elif isvalid == 1:
                print("Warning: Phoneme set",item,"in rule",newrule,"contains features from both consonants and vowels."
                                                                    " This rule will be ignored.")
                ignoreRule = True
            elif isvalid == 0 and helpers.checkConflict(item):
                print("Warning: Phoneme set",item,"in rule",newrule,"contains contradicting features. This rule will "
                                                                    "be ignored.")
                ignoreRule = True
        if not ignoreRule:
            rules.append(newrule)
        indexes, max = helpers.increment(indexes,maxindexes)
    return rules

# Generates all possible instances of rules from phoneme set and rules
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
        # Gives error message if no phonemes found for rule element
        if len(phonset) == 0:
            print("Error: No phonemes in set",sylele+".")
            return ["EMPTY"]
        phonsets.append(phonset)
    # Creates index arrays to keep track of phoneme set indexes
    for sylele in phonsets:
        indexes.append(0)
        maxindexes.append(len(sylele)-1)
    # Iterates through all possible combinations of syllables based on phoneme sets and order, using indexes array to
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
    abort = False
    if phonemes == ['']:
        print("No phoneme set.")
        abort = True
    if len(sylrules) == 0:
        print("No syllable rules.")
        abort = True
    if abort:
        sys.exit()
    sylset = set()
    newrules = []
    for rule in sylrules:
        newrules += generateRules(rule,IPA_info)
    for rule in newrules:
        sylstoadd = sylsFromRule(phonemes,rule,IPA_info)
        for syl in sylstoadd:
            sylset.add(syl)
        if "EMPTY" in sylset:
            sylset = []
    sylset = list(sylset)
    out = open(outfile,'w')
    out.write('\n'.join(sylset))
    out.close()