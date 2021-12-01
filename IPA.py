'''                 IPA READER AND FUNCTIONS              '''

# Splits an input into a range set of values (list) and an axis value (int), then returns them
def splitter(rangeaxis):
    ra = rangeaxis.split(';')
    r = ra[0].split(',')
    axis = int(ra[1])
    ranges = [i for i in range(int(r[0]),int(r[1]))]
    return ranges, axis

# Reads in all the IPA files to create two sets of IPA matrices and two sets of IPA data lookups (consonants and vowels)
def readInIPA(dir):
    # Reads in IPAs
    # format: [[(string, string)],[(string, string)]]
    IPAC = [[pair.split(',') for pair in line.strip().split(' ')] for line in open(dir+"/IPA/IPAC.txt")]
    IPAV = [[pair.split(',') for pair in line.strip().split(' ')] for line in open(dir+"/IPA/IPAV.txt")]
    # Reads in IPA keys and sets up dictionaries
    ipackeylines = [line.strip().split(' ') for line in open(dir+"/IPA/IPACKEY.txt")]
    ipavkeylines = [line.strip().split(' ') for line in open(dir+"/IPA/IPAVKEY.txt")]
    IPACKEY = {line[0]:splitter(line[1]) for line in ipackeylines}
    IPAVKEY = {line[0]:splitter(line[1]) for line in ipavkeylines}
    # Sets up featuresets for future use
    # This section sets up feature sets by taking only the place/manner/voicing/etc features (lines) in the KEY files
    #   and it does so by only taking the features/lines in the KEY files with only one row/column/comma-place range
    #   for its index; e.g. BILB 0,1;0 will be selected but BILA 0,2;0 will not.
    # This is in order to select values for {X}:a replacement, and only the specific place/manner/voicing/etc features
    #   are really relevant for that. However, we cannot hard-code them in case a user decides to incorporate
    #   palato-alveolars, which is considered its own singular place of articulation, or something similar.
    places = ['+'+aspect for aspect in IPACKEY if len(IPACKEY[aspect][0]) == 1 and IPACKEY[aspect][1] == 0]
    manners = ['+'+aspect for aspect in IPACKEY if len(IPACKEY[aspect][0]) == 1 and IPACKEY[aspect][1] == 1]
    voicings = ['+'+aspect for aspect in IPACKEY if len(IPACKEY[aspect][0]) == 1 and IPACKEY[aspect][1] == 2]
    heights = ['+'+aspect for aspect in IPAVKEY if len(IPAVKEY[aspect][0]) == 1 and IPAVKEY[aspect][1] == 0]
    backnesses = ['+'+aspect for aspect in IPAVKEY if len(IPAVKEY[aspect][0]) == 1 and IPAVKEY[aspect][1] == 1]
    roundings = ['+'+aspect for aspect in IPAVKEY if len(IPAVKEY[aspect][0]) == 1 and IPAVKEY[aspect][1] == 2]
    # Compiles them into a single list to return
    features = [places,manners,voicings,heights,backnesses,roundings]
    return [IPAC, IPAV, IPACKEY, IPAVKEY, features]

# Adds set of numbers into an existing set without duplicates (range of lookup values), aka adds phoneme features
def addFeat(existing,toadd):
    newfeat = existing
    for phset in toadd:
        if phset not in existing:
            newfeat.append(phset)
    return newfeat

# Removes set of numbers into an existing set (range of lookup values), aka takes out phoneme features
def rmFeat(existing,torm):
    newfeat = []
    for phset in existing:
        if phset not in torm:
            newfeat.append(phset)
    return newfeat

# Adds a set of lookup values on a given axis (changes place/manner/voicing or height/backness/rounding)
def addFeats(existing,changes):
    toadd, axis = changes
    newfeats = existing
    newfeats[axis] = addFeat(existing[axis],toadd)
    return newfeats

# Removes a set of lookup values on a given axis (changes place/manner/voicing or height/backness/rounding)
def rmFeats(existing,changes):
    torm, axis = changes
    newfeats = existing
    newfeats[axis] = rmFeat(existing[axis],torm)
    return newfeats

# Finds a set of phonemes given phoneme descriptors
def findSet(features, IPASTUFF):
    # Setup
    IPAC, IPAV, IPACKEY, IPAVKEY = IPASTUFF
    ranges = [[],[],[]]
    phonemes = []
    feats = features.split(',')
    ignoreRule = False
    # Warns the user and breaks out of function if any of the input features lack + or -
    for feat in feats:
        if feat in IPACKEY or feat in IPAVKEY:
            print("Warning:",feat,"in",features,"is a feature. Did you mean to add '-' or '+' to the "
                       "beginning of it? This descriptor will be treated as a single phoneme.")
            ignoreRule = True
    # If there is no ',' separator, no '+', and no '-' treat the whole sequence as a single phoneme
    if ignoreRule or ',' not in features and '+' not in features and '-' not in features:
        return [features]
    # Sets consonant or vowel chart and key
    if feats[0][1:] in IPACKEY:
        chart = IPAC
        phonkey = IPACKEY
    else:
        chart = IPAV
        phonkey = IPAVKEY
    # Adds features
    for feat in feats:
        if feat[0] == '+':
            ranges = addFeats(ranges,phonkey[feat[1:]])
    # fills in empty values to full table if left empty
    if ranges[0] == []:
        ranges[0] = [i for i in range(len(chart))] # Fills in for axis 0
    if ranges[1] == []:
        ranges[1] = [i for i in range(len(chart[0]))] # Fills in for axis 1
    if ranges[2] == []:
        ranges[2] = [i for i in range(len(chart[0][0]))] # Fills in for axis 2
    for feat in feats:
        if feat[0] == '-':
            ranges = rmFeats(ranges,phonkey[feat[1:]])
    # Finds all phonemes given features
    for i in ranges[0]:
        for j in ranges[1]:
            for k in ranges[2]:
                if chart[i][j][k] != '0':
                    phonemes.append(chart[i][j][k])
    return phonemes

# Takes intersection of phonemes in inventory and phonemes in a given set
def filterPhonemes(phonemes, phonemeset):
    filtered = []
    for phoneme in phonemes:
        if phoneme in phonemeset:
            filtered.append(phoneme)
    return filtered

if __name__ == "__main__":
    IPASTUFF = readInIPA("L4")
    print(IPASTUFF[3])