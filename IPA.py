'''                 IPA READER AND CLASSES              '''
from SubIPA import SubIPA
from enum import Enum

class Valid(Enum):
    VAL = 0
    INVSET = 1
    INVFEAT = 2


class IPA:
    def __init__(self,direct):
        self.IPAC = SubIPA(direct,"C")
        self.IPAV = SubIPA(direct,"V")

    def findSet(self,features):
        feats = [feat.strip().upper() for feat in features.split(',')]
        ignoreRule = False
        for feat in feats:
            if feat in self.IPAC.key or feat in self.IPAV.key:
                print("Warning:",feat,"in",features,"is a feature, not a phoneme or set. Did you mean to add '-' or "
                            "'+' to the beginning of it? This descriptor will be treated as a single phoneme.")
                ignoreRule = True
        # If there is no ',' separator, no '+', and no '-' treat the whole sequence as a single phoneme
        if ignoreRule or ',' not in features and '+' not in features and '-' not in features:
            return [features]
        phonemes = list()
        if feats[0][1:] in self.IPAC.key:
            self.IPAC.findSet(phonemes,feats)
        else:
            self.IPAV.findSet(phonemes,feats)
        return phonemes

    def filterPhonemes(self,phonemes, phonemeset):
        filtered = []
        for phoneme in phonemes:
            if phoneme in phonemeset:
                filtered.append(phoneme)
        if not filtered:
            filtered = ['']
        return filtered

    def validPhonemeSet(self,features):
        valid = Valid.VAL
        feats = features.split(',')
        if len(feats[0]) <= 2:
            return valid

        alphas = ["PLACE:a", "MANNER:a", "VOICING:a", "HEIGHT:a", "BACKNESS:a", "ROUNDING:a"]
        combkeys = {**self.IPAC.key, **self.IPAV.key}


        if feats[0][1:] not in combkeys and feats[0][1:] not in alphas:
            print("Warning: Descriptor " + feats[0][1:] + " not in IPACKEY or IPAVKEY.")
            return Valid.INVFEAT
        featset = (self.IPAC.key,self.IPAV.key)[(feats[0][1:] in self.IPAV.key or feats[0] in alphas[3:])]

        for feat in feats:
            if feat[1:] not in combkeys and feat not in alphas:
                print("Warning: Descriptor ",feat," not in IPACKEY or IPAVKEY.")
                return Valid.INVFEAT
            elif feat[1:] not in featset:
                print("Warning: Descriptor",feat,"is not in the same feature set.")
                return Valid.INVSET

        return valid

    @staticmethod
    def checkConflict(features):
        feats = features.split(',')
        if len(feats[0]) <= 2:
            return False
        featset = set(feats[0])
        for feat in feats[1:]:
            # reverse sign and check if its in feat set
            if ('+','-')[feat[0] == '+'] + feat[1:] in featset:
                return True
            featset.add(feat)
        return False


if __name__ == "__main__":
    # tests
    full = IPA("L3")
    print(full.findSet("p"))