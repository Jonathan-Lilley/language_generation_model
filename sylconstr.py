'''     SYLLABLE CONSTRUCTOR       '''
import sys
from IPA import IPA, Valid

class SylConst:
    def __init__(self,direct):
        self.direct = direct
        self.IPAf = IPA(direct)

        try:
            self.phonemes = (' '.join([line.strip() for line in open(direct + "/inputs/phonemes.txt")
                                       if line.strip() != ''])).split(' ')
        except IOError:
            print("Phonemes file not found")

        try:
            self.sylrules = [line.strip().split('|') for line in open(direct + "/inputs/sylstructs.txt")
                             if line.strip() != '']
        except IOError:
            print("Syllable rule file not found")

        self.rules = list()
        self.syls = set()

    def generateRules(self,rule):

        onsets = rule[0].split(';')
        nucleus = rule[1].split(';')
        codas = rule[2].split(';')
        allparts = [onsets,nucleus,codas]

        for part in range(len(allparts)):
            for r in range(len(allparts[part])):
                partrule = allparts[part][r]
                validity = self.IPAf.validPhonemeSet(partrule)
                if validity == Valid.INVFEAT:
                    print("Warning: Invalid feature.",partrule,"will be ignored")
                    allparts[part].remove([r])
                elif validity == Valid.INVSET:
                    print("Warning: Phoneme set", r, "in the rule contains features from both consonants and vowels."
                          " This rule will be ignored.")
                    allparts[part].remove([r])
                elif validity == Valid.VAL and IPA.checkConflict(partrule):
                    print("Warning: Phoneme set", allparts[part][r], "contains contradicting features. This rule will "
                          "be ignored.")
                    allparts[part].remove([r])

        rules = [[[[ons,nuc,cod] for ons in onsets] for nuc in nucleus] for cod in codas]
        self.rules = [Lthree for Lone in rules for Ltwo in Lone for Lthree in Ltwo]


    def sylsFromRule(self,rule):

        phonsets = []
        rule = rule.split(' ')
        for sylele in rule:
            phonset = self.IPAf.filterPhonemes(self.phonemes, self.IPAf.findSet(sylele))
            if len(phonset) == 0:
                print("Error: No phonemes in set", sylele + ".")
                continue
            phonsets.append(phonset)

        syls = [[[[ons,nuc,cod] for ons in phonsets[0]] for nuc in phonsets[1]] for cod in phonsets[2]]
        self.syls = self.syls.union(set([Lthree for Lone in syls for Ltwo in Lone for Lthree in Ltwo]))

        # Constructs all syllables given input phonemes and rule file and writes to output file
    def constructSyls(self):
        outfile = self.direct + "/outputs/syllables.txt"

        abort = False
        if self.phonemes == ['']:
            print("No phoneme set.")
            abort = True
        if len(self.sylrules) == 0:
            print("No syllable rules.")
            abort = True
        if abort:
            sys.exit()

        for rule in self.sylrules:
            self.generateRules(rule)

        for rule in self.rules:
            self.sylsFromRule(rule)

        sylset = list(self.syls)
        out = open(outfile, 'w')
        out.write('\n'.join(sylset))
        out.close()

if __name__ == "__main__":
    constructor = SylConst("L3")
    constructor.constructSyls()