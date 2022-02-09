'''                 SOUND CHANGE                    '''
'''
    A little context for part of this for computer scientists who aren't as familiar with linguistics:
    
    There are several functions dedicated to "alphas". In sound change processes in phonology, there's a concept called
        "alpha values". When a sound changes in the context of other sounds, it usually changes to either another 
        specific sound or another class of sounds, but it can also assimilate to the *place* of a context
        The way I model this in this program is with alpha values. When there is a rule, when there are two alpha values
        in a single rule, they will generate a set of rules where they are always the same value. This way, when the 
        rules are generated, the alpha values are parallel as they are intended to be.
        
'''
import re, os, time
from LangGen.IPA import IPA, Valid


class SoundChanger:
    def __init__(self,direct,IPAf,inpwords):
        self.direct = direct
        self.IPAf = IPAf
        self.start = 0
        self.words = [inpwords]
        self.rules = [list()]
        self.soundchanges = [[line.strip() for line in open(self.direct+"/inputs/"+file)]
                             for file in os.listdir(self.direct+"/inputs") if "changes" in file]
        self.outfiles = [self.direct+'/outputs/words'+str(i)+'.txt' for i in range(1,len(self.soundchanges)+1)]
        self.phonsets = [list(set(''.join(inpwords)))]

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

    def subAlpha(self,rule,alphas,alpha):
        for a in alphas[alpha]:
            rule = re.sub(alpha,a,rule)
        return rule

    def replaceAlpha(self,rule):
        alphas = self.IPAf.getAlphas()
        rules = []
        for alpha in alphas:
            if alpha in rule:
                rules = self.subAlpha(rule,alphas,alpha)
        if type(rule) == str:
            rules = [rules]
        if not any(rules):
            rules = [rule]
        return rules

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
                if item not in self.IPAf.getPhons() + ['0']:
                    print(f"Warning: rule {rule} contains an invalid phoneme {item}. This rule will be ignored")
                return False
        if iphon == ophon:
            print(f"Warning: rule {rule} contains equivalent input and output. This rule will be ignored.")
            return False
        for item in contx:
            if not self.checkValid(rule,item):
                if item not in self.IPAf.getPhons() + ['','_','#']:
                    print(f"Warning: rule {rule} contains an invalid phoneme {item}. This rule will be ignored")
                return False
        return True

    def generateRules(self,inrule,phonset,idx):
        alphas = [alpha for alpha in self.replaceAlpha(inrule) if alpha]
        rules = []
        for rule in alphas:
            if not self.checkValidParts(rule):
                continue
            iphonset, ophonset, contx = self.parseRule(rule)
            # This filters the set of phonemes found by the phonemes for the input words because this will significantly
            #   reduce the number of rules generated, making it run faster
            iphons = IPA.filterPhonemes(self.IPAf.findSet(iphonset),phonset)
            ophons = self.IPAf.findSet(ophonset)
            contexts = self.generateEnvirons(contx)
            rules = [iphons]+[ophons]
            temprules = []
            for context in contexts:
                temprule = rules+[[context]]
                temprules += temprule
            rules = temprules
        fullrules = []
        for i in rules[0]:
            for o in rules[1]:
                for c in rules[2]:
                    fullrules.append(i+'>'+o+'/'+c)
        self.rules[idx] += fullrules

    def changeWord(self,word,rule):
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
        return word

    def changeSounds(self,idx):
        print(f"Changing {len(self.words[idx])} words.")
        for word in self.words[idx]:
            print(f"Elapsed time = {round((time.time()-self.start),2)} ... Generating word {word}",end="\r")
            for rule in self.rules[idx]:
                word = self.changeWord(word,rule)
            self.words[idx+1].append(word)

    def genChanges(self):
        self.start = time.time()
        if not self.words:
            print("No words were generated")
            return
        if not self.soundchanges:
            print("No soundchange files found")
            return
        for i in range(len(self.soundchanges)):
            currchanges = self.soundchanges[i]
            self.words.append(list())
            self.rules.append(list())
            for changes in currchanges:
                self.generateRules(changes,self.phonsets[i],i+1)
            self.changeSounds(i)
            self.phonsets.append(list(set(''.join(self.words[i+1]))))
            with open(self.outfiles[i],'w') as f:
                f.write('\n'.join(self.words[i+1]))