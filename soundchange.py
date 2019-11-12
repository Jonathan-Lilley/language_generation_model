'''                 SOUND CHANGE                    '''

import IPA
import helpers
import os

# Finds index of a substring within a string
def findSubstring(string, substring):
    i = 0
    j = 0
    while i < len(string):
        if string[i] == substring[j]:
            while j < len(substring) and i+j < len(string):
                if string[i+j] == substring[j]:
                    j += 1
                    if j == len(substring):
                        return i
                else:
                    break
            j = 0
        i += 1
    return -1

# Replaces all instances of substring with replstr (replacement string) in string
def replaceSubstring(string, substring, replstr):
    i = findSubstring(string, substring)
    while i != -1:
        string = string[:i] + replstr + string[i+len(substring):]
        i = findSubstring(string,substring)
    return string

# Replaces alpha features
def replaceAlpha(rule,IPA_info):
    pmvhbr = IPA_info[4] # places, manners, voicings, heights, backnesses, roudnings
    present = []
    rules = []
    replacements = []
    indexes = []
    maxindexes = []
    max = False
    if findSubstring(rule, "a") == -1:
        rules.append(rule)
    else:
        if findSubstring(rule, "PLACE:a") != -1:
            replacements.append(pmvhbr[0])
            present.append("PLACE:a")
        if findSubstring(rule, "MANNER:a") != -1:
            replacements.append(pmvhbr[1])
            present.append("MANNER:a")
        if findSubstring(rule, "VOICING:a") != -1:
            replacements.append(pmvhbr[2])
            present.append("VOICING:a")
        if findSubstring(rule, "HEIGHT:a") != -1:
            replacements.append(pmvhbr[3])
            present.append("HEIGHT:a")
        if findSubstring(rule, "BACKNESS:a") != -1:
            replacements.append(pmvhbr[4])
            present.append("BACKNESS:a")
        if findSubstring(rule, "ROUNDING:a") != -1:
            replacements.append(pmvhbr[5])
            present.append("ROUNDING:a")
        for aspect in replacements:
            indexes.append(0)
            maxindexes.append(len(aspect)-1)
        while not max:
            newrule = rule
            for aspect in range(len(replacements)):
                newrule = replaceSubstring(newrule,present[aspect],replacements[aspect][indexes[aspect]])
            rules.append(newrule)
            indexes, max = helpers.increment(indexes,maxindexes)
    return rules

# Expands environment rules to generate all possible environment rules
def generateEnvirons(environment,IPA_info):
    eles = environment.split(' ')
    environments = []
    phonsets = []
    indexes = []
    maxindexes = []
    max = False
    # Creates a phoneme set for each element of the environment
    for ele in eles:
        if len(ele) > 1:
            phonsets.append(IPA.findSet(ele,IPA_info[:4]))
        else:
            phonsets.append([ele])
    # Creates index arrays to keep track of phoneme set indexes
    for phonset in phonsets:
        indexes.append(0)
        maxindexes.append(len(phonset) - 1)
    # Iterates through all possible combinations of syllables based on phoneme sets and order, using indexes array to
    #       keep track of position within the phoneme sets
    if -1 in maxindexes:
        return []
    while not max:
        environ = ''
        for l in range(len(phonsets)):
            environ += phonsets[l][indexes[l]]
        environments.append(environ)
        indexes, max = helpers.increment(indexes, maxindexes)
    return environments

# Parses a rule into the input phoneme, the output phoneme, and the environment
def parseRule(rule):
    rule = rule.split('>')
    inphon = rule[0]
    outphon, environment = rule[1].split('/')
    return inphon, outphon, environment

# Generates all phoneme rules based on feature rules
def generateRules(rule,phonemes,IPA_info):
    info_short = IPA_info[:4]
    rules = []
    # Generates all rules with ASPECT:a replaced
    alpharules = replaceAlpha(rule,IPA_info)
    # Iterates through all generated rules
    for alpharule in alpharules:
        # Splits input, output, and environment
        inphonset, outphonset, environment = parseRule(alpharule)
        # Generates full set of input phonemes, output phonemes, and environments
        inphons = IPA.findSet(inphonset,info_short)
        outphons = IPA.findSet(outphonset,info_short)
        environments = generateEnvirons(environment,IPA_info)
        # Iterates through all parts of the rule
        # Rules are slightly filtered for speed
        for inphon in inphons:
            if inphon in phonemes: # Includes only rules with input phonemes in the original phoneme set
                for outphon in outphons:
                    if outphon != inphon: # Excludes identity rules
                        for environ in environments:
                            inphonemeset = True
                            for phon in environ:
                                if phon not in phonemes and phon not in '#_':
                                    inphonemeset = False
                            if inphonemeset == True:
                                rules.append(inphon+'>'+outphon+'/'+environ)
    return rules


# Changes the sounds in a single word
def changeWord(word, rule):
    # Adds end of word symbol
    word += '#'
    # Sets up input phoneme, output phoneme, and environment
    inphon, outphon, environ = parseRule(rule)
    # If epenthesis, insert 0 between every character to search for epenthesis context
    if inphon == '0':
        newword = '0'
        for letter in word:
            newword += letter+'0'
        word = newword
    # Creates a substring that is the environment to find in and a replacement substring
    findenviron = replaceSubstring(environ,'_',inphon)
    replacement = replaceSubstring(environ,'_',outphon)
    # Replaces environment with replacement environment
    while findSubstring(word,findenviron) != -1:
        word = replaceSubstring(word,findenviron,replacement)
    # Removes 0 and # (deletion and end of word symbols)
    while findSubstring(word,'0') != -1:
        word = replaceSubstring(word,'0','')
    while findSubstring(word,'#') != -1:
        word = replaceSubstring(word,'#','')
    return word

# Changes all the words with a given sound
def changeSound(words, rule):
    newWords = []
    for word in words:
        newWords.append(changeWord(word,rule))
    return newWords

# Implements all sound changes
def allChanges(dir):
    filelist = os.listdir(dir+'/inputs')
    IPA_info = IPA.readInIPA()
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
        soundchanges = [line.strip() for line in open(dir+"/inputs/changes"+str(i+1)+".txt")] # Sound change file
        try:
            words = [line.strip() for line in open(dir+"/outputs/words"+str(i)+".txt")] # existing words file
        except IOError:
            print("No words0 file found")
            return
        phonemes = list(set(''.join(words))) # Sets up phonemes from existing words
        outfile = open(dir+"/outputs/words"+str(i+1)+".txt",'w') # output file
        for soundchange in soundchanges:
            newchange = generateRules(soundchange,phonemes,IPA_info)
            for change in newchange:
                print(change)
                words = changeSound(words, change)
        outfile.write('\n'.join(words)) # puts changed words into the output file for use in the next iteration
        outfile.close()


if __name__ == "__main__":
    allChanges('L1')