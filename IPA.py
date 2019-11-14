'''                 IPA READER AND FUNCTIONS              '''

# Splits an input into a range set of values (list) and an axis value (int), then returns them
def splitter(rangeaxis):
    ra = rangeaxis.split(';')
    r = ra[0].split(',')
    axis = int(ra[1])
    ranges = [i for i in range(int(r[0]),int(r[1]))]
    return ranges, axis

# Reads in all the IPA files to create two sets of IPA matrices and two sets of IPA data lookups (consonants and vowels)
def readInIPA():
    # Reads in IPAs
    IPAC = [[pair.split(',') for pair in line.strip().split(' ')] for line in open("IPA/IPAC.txt")]
    IPAV = [[pair.split(',') for pair in line.strip().split(' ')] for line in open("IPA/IPAV.txt")]
    # Reads in IPA keys and sets up dictionaries
    ipackeylines = [line.strip().split(' ') for line in open("IPA/IPACKEY.txt")]
    ipavkeylines = [line.strip().split(' ') for line in open("IPA/IPAVKEY.txt")]
    IPACKEY = {line[0]:splitter(line[1]) for line in ipackeylines}
    IPAVKEY = {line[0]:splitter(line[1]) for line in ipavkeylines}
    # Sets up featuresets for future use
    places = ["+BILA","+LABD","+DENT","+ALVE","+PALV","+RETR","+PALT","+VELA","+UVUL","+PHAR","+LARY"]
    manners = ["+STOP","+FRIC","+LATF","+NASA","+APPR","+LATA","+TRIL","+FLAP"]
    voicings = ["+VOID","+VLSS"]
    heights = ["+CLOS","+NRCL","+MIDC","+MIDO","+NROP","+OPEN"]
    backnesses = ["+FRNT","+CENT","+BACK"]
    roundings = ["+URND","+ROND"]
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
    # Breaks out of function if features is a single phoneme
    if features[0] not in "+-":
        return [features]
    # Setup
    IPAC, IPAV, IPACKEY, IPAVKEY = IPASTUFF
    ranges = [[],[],[]]
    phonemes = []
    feats = features.split(',')
    for feat in range(len(feats)):
        if feats[feat][0] == '-' and '+'+feats[feat][1:] in feats[feat:]:
            phonemes.append("NULL SET")
            return phonemes
        elif feats[feat][0] == '+' and '-'+feats[feat][1:] in feats[feat:]:
            phonemes.append("NULL SET")
            return phonemes
    # Sets consonant or vowel
    if feats[0][1:] in IPACKEY:
        phonemeset = IPAC
        phonkey = IPACKEY
    else:
        phonemeset = IPAV
        phonkey = IPAVKEY
    # Adds features
    #print(feats)
    for feat in feats:
        if feat[0] == '+':
            ranges = addFeats(ranges,phonkey[feat[1:]])
    # fills in empty values to full table if left empty
    if ranges[0] == []:
        ranges[0] = [i for i in phonemeset] # Fills in for axis 0
    if ranges[1] == []:
        ranges[1] = [i for i in phonemeset[0]] # Fills in for axis 1
    if ranges[2] == []:
        ranges[2] = [i for i in phonemeset[0][0]] # Fills in for axis 2
    for feat in feats:
        if feat[0] == '-':
            ranges = rmFeats(ranges,phonkey[feat[1:]])
    # Finds all phonemes given features
    for i in ranges[0]:
        for j in ranges[1]:
            for k in ranges[2]:
                if phonemeset[i][j][k] != '0':
                    phonemes.append(phonemeset[i][j][k])
    return phonemes

# Finds a specific phoneme given features
def findPhoneme(features, IPASTUFF):
    if len(features.split(',')) != 3:
        print("Wrong number of features")
        return
    return findSet(features,IPASTUFF)[0]

# Takes intersection of phonemes in inventory and phonemes in a given set
def filterPhonemes(phonemes, phonemeset):
    filtered = []
    for phoneme in phonemes:
        if phoneme in phonemeset:
            filtered.append(phoneme)
    return filtered