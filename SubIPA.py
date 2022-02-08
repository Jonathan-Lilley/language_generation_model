'''                 SUBIPA              '''

class SubIPA:
    def __init__(self,direct,consvowel):
        paths = [direct+"/IPA/IPA"+("C","V")[consvowel=="V"]+suff for suff in [".txt","KEY.txt"]]

        self.phons = [[pair.split(',') for pair in line.strip().split(' ')] for line in open(paths[0])]
        # key : ([range int list, axis int])
        self.key = {line[0]:self.splitter(line[1]) for line in [line.strip().split(' ') for line in open(paths[1])]}

        # Quick note: this catches all the aspects in a row/col/aisle sublist format
        #   Basically, features[0] is the "rows", aka manner of artic, feat[1] is "cols", aka place, etc
        #   We check if the key[aspect][0] is 1 because that means it *only* refers to that singular row/col/aisle
        #   That will catch things like FRIC, but not SONO, which spans multiple rows
        #   This is really just for alpha values
        self.features = {K:['+'+aspect for aspect in self.key if len(self.key[aspect][0]) == 1
                          and self.key[aspect][1] == num] for num in range(3)
                         for K in (["HEIGHT","BACKNESS","ROUNDING"],["PLACE","MANNER","VOICING"])[consvowel == "C"]}

        # Splits an input into a range set of values (list) and an axis value (int), then returns them
    def splitter(self,rangeaxis):
        r, axis = rangeaxis.split(';')
        r = r.split(',')
        return [i for i in range(int(r[0]), int(r[1]))], int(axis)

    def rmaddFeats(self,ranges,phonkey,rmadd):
        values, axis = self.key[phonkey[1:]]
        for val in values:
            if rmadd == "add" and val not in ranges[axis]:
                ranges[axis].append(val)
            elif rmadd == "rm" and val in ranges[axis]:
                ranges[axis].remove(val)

    def findSet(self,phonemes,feats):
        # ranges[0] keeps track of row #, ranges[1] is col #, ranges[2] is aisle #
        ranges = [list() for _ in range(3)]

        for feat in feats:
            if feat[0] == "+":
                self.rmaddFeats(ranges,feat,"add")

        chart = self.phons
        for i in range(len(ranges)):
            # If you input an axis, this will fill in its other indices
            # If the entire table is empty (if you're donly doing -FEAT), it will fill in everything before removing
            if (not ranges[i] and any(ranges[0:len(ranges)])) or not any(ranges):
                ranges[i] = [j for j in range(len(chart))]
            chart = chart[0]

        for feat in feats:
            if feat[0] == "-":
                self.rmaddFeats(ranges,feat,"rm")

        # collapse the values into index triplets
        ranges = [[[[i,j,k] for i in ranges[0]] for j in ranges[1]] for k in ranges[2]]
        # Pull all of the indices to a 2d list instead of a frickin 4d list lol
        ranges = [Lthree for Lone in ranges for Ltwo in Lone for Lthree in Ltwo]

        for idx in ranges:
            if self.phons[idx[0]][idx[1]][idx[2]] != "0":
                phonemes.append(self.phons[idx[0]][idx[1]][idx[2]])