'''     SYLLABLE CONSTRUCTOR       '''
import sys, os
from IPA import Valid

class SylConst:
    def __init__(self,direct,IPAf):
        self.direct = direct
        self.IPAf = IPAf

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
        self.syls = []

    def getSyls(self):
        return self.syls

    def checkValid(self,rulepart):
        subparts = rulepart.split()
        for subp in subparts:
            validity = self.IPAf.validPhonemeSet(subp)
            if validity == Valid.INVFEAT:
                print(f"Warning: Invalid feature, {subp} in {rulepart}. This rule  will be ignored")
                return validity
            elif validity == Valid.INVSET:
                print(f"Warning: Phoneme set {subp} in the rule contains features from both consonants and vowels."
                      " This rule will be ignored.")
                return validity
        return Valid.VAL



    def generateRules(self,rule):
        onsets = rule[0].split(';')
        nucleus = rule[1].split(';')
        codas = rule[2].split(';')
        allparts = [onsets,nucleus,codas]

        for part in range(len(allparts)):
            for r in range(len(allparts[part])):
                #print(allparts[part],len(allparts[part]),r)
                if self.checkValid(allparts[part][r]) != Valid.VAL:
                    allparts[part].remove(allparts[part][r])
                    r -= 1

        rules = [[[' '.join([ons,nuc,cod]) for ons in allparts[0]] for nuc in allparts[1]] for cod in allparts[2]]
        self.rules = [Lthree for Lone in rules for Ltwo in Lone for Lthree in Ltwo]


    def sylsFromRule(self,rule):
        phonsets = []
        rule = rule.split(' ')
        for sylele in rule:
            phonset = self.IPAf.filterPhonemes(self.phonemes, self.IPAf.findSet(sylele))
            if phonset == [''] and sylele != '':
                print(f"Warning: No phonemes in set {sylele}.")
                continue
            phonsets.append(phonset)

        syls = phonsets[0]
        for phonset in phonsets[1:]:
            newsyls = []
            for syl in syls:
                newsyls += [syl+p for p in phonset]
            syls = newsyls

        self.syls += syls


    def writeSyls(self):
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
        self.syls = list(set(self.syls)) # just in case there are duplicates

        if not os.path.exists(self.direct+"/outputs"):
            os.mkdir(self.direct+'/outputs')

        with open(self.direct + "/outputs/syllables.txt",'w') as out:
            out.write('\n'.join(self.syls))
            out.close()