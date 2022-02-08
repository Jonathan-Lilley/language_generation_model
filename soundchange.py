'''                 SOUND CHANGE                    '''

import os, re
from IPA import IPA, Valid


class SoundChanger:
    def __init__(self,direct,IPAf,inpwords):
        self.direct = direct
        self.IPAf = IPAf
        self.inpwords = inpwords
        self.rules = []
        self.words = []

    def parseRule(self,rule):
        rule = rule.split('>')
        inphon = rule[0]
        outphon, environment = rule[1].split('/')
        return inphon, outphon, environment

    def generateEnvirons(self,environment):
        phonsets = [self.IPAf.findSet(environ) for environ in environment.split()]
        environments = phonsets[0]
        for pset in phonsets[1:]:
            tempenv = []
            for e in environments:
                for p in pset:
                    tempenv = e+p
            environments = tempenv
        return environments

    def subAlpha(self,rules,alpha):
        replace = []
        while alpha in rules[0]:
            for r in range(len(rules)):
                for a in self.IPAf.geAlphas[alpha]:
                    replace.append(re.sub(alpha,a,rules[r],1))
            rules = replace
            replace = []

    def replaceAlpha(self,rule):
        rules = [rule]
        for alpha in self.IPAf.geAlphas:
            self.subAlpha(rules,alpha)
        return rules

    def generateAlpha(self,rule):


    def checkValid(self,rule,item):
        validity = self.IPAf.validPhonemeSet(item)
        conflict = IPA.checkConflict(item)
        if validity == Valid.INVFEAT:
            print(f"Warning: {rule} contains invalid feature {item}. This rule will be ignored.")
        elif validity == Valid.INVSET:
            print(f"Warning: Phoneme set {item} in rule {rule} contains features from both consonants and vowels."
                  " This rule will be ignored.")
        elif conflict:
            print(f"Warning: Phoneme set {item} in rule {rule} contains contradicting features. This rule will "
                  "be ignored.")
        if conflict or validity != Valid.VAL:
            return False
        return True

    def checkValidParts(self,rule):
        iphon, ophon, contx = self.parseRule(rule)
        contx = [c for c in contx.split() if c != '_']
        for item in [iphon,ophon]:
            if not self.checkValid(rule,item):
                return False
            if item not in self.IPAf.getPhons() + ['0']:
                print(f"Warning: rule {rule} contains an invalid phoneme {item}. This rule will be ignored")
                return False
        if iphon == ophon:
            print(f"Warning: rule {rule} contains equivalent input and output. This rule will be ignored.")
            return False
        for item in contx:
            if not self.checkValid(rule,item):
                return False
            if item not in self.IPAf.getPhons() + ['','_','#']:
                print(f"Warning: rule {rule} contains an invalid phoneme {item}. This rule will be ignored")
                return False
        return True

    def generateRules(self,inrule):
        arules = self.replaceAlpha(inrule)
        rules = []
        for rule in arules:
            if not self.checkValidParts(rule):
                continue
            iphonset, ophonset, contx = self.parseRule(rule)
            iphons, ophons = self.IPAf.findSet(iphonset), self.IPAf.findSet(ophonset)
            contexts = self.generateEnvirons(contx)
            rules = iphons
            for addit in [ophons,contexts]:
                temprules = []
                for rule in rules:
                    for item in addit:
                        temprules.append(rule+item)
                rules = temprules
        self.rules = [r[0]+'>'+r[1]+'/'+r[2] for r in rules]

    def changeWord(self,word):
        for rule in self.rules:
            iphon, ophon, contx = self.parseRule(rule)
            # epenthesis
            if iphon == '0':
                word = '0'+'0'.join(list(word))+'0'
                idx = contx.index('_')
                lcontx = list(contx)
                contx = '0'+'0'.join(lcontx[:idx])+'_'+'0'.join(lcontx[idx+1:])+'0'
            tosub = re.sub('_',iphon,contx)
            subwith = re.sub('_',ophon,contx)
            re.sub(tosub,subwith,word)
            re.sub('0','',word)
            re.sub('#','',word)
        self.words.append(word)

    def changeSound(self):
        for word in self.inpwords:
            self.changeWord(word)

    def genChanges(self):
        pass


# Implements all sound changes
def allChanges(dir):
    filelist = os.listdir(dir+'/inputs')
    IPA_info = IPA.readInIPA(dir)
    # Counts up number of "change" files in input directory, aka how many stages of sound change
    numchanges = 0
    for file in filelist:
        if "changes" in file:
            numchanges += 1
    # Goes through each soundchange file
    # i is important because it keeps track of which sound change and words file we're on
    if numchanges == 0:
        print("No soundchange files found")
        return
    for i in range(numchanges):
        # Gets soundchanges from file as a list
        soundchanges = [line.strip() for line in open(dir+"/inputs/changes"+str(i+1)+".txt")] # Sound change file
        # Gets all the words from the previous word file (starting at 0)
        try: # Works if words#.txt exists
            words = [line.strip() for line in open(dir+"/outputs/words"+str(i)+".txt")] # existing words file
        except IOError: # But if not, gives error statement and returns nothing
            print("No words0 file found")
            return
        # Generates list of phonemes
        # Used for rule creation (to limit number of rules made to save time by not running through every possible rule)
        phonemes = list(set(''.join(words))) # Sets up phonemes from existing words
        outfile = open(dir+"/outputs/words"+str(i+1)+".txt",'w') # output file
        for soundchange in soundchanges:
            newchange = generateRules(soundchange,phonemes,IPA_info)
            for change in newchange:
                words = changeSound(words, change)
        outfile.write('\n'.join(words)) # puts changed words into the output file for use in the next change iteration
        outfile.close()