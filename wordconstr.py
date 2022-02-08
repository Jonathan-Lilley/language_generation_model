'''                 WORD CONSTRUCTOR                    '''
import random, time


# Note: this also excludes anything the max number is divisible by to make sure it doesn't loop over any number twice
def getPrimes(max):
    primes = [2]
    for i in range(3,max):
        if max % i != 0 and not [j for j in primes if i % j == 0]:
            primes.append(i)
    return primes


class WordGen:
    def __init__(self,direct,wordcount,sylratios):
        self.direct = direct
        self.syllables = [line.strip() for line in open(self.direct + "/outputs/syllables.txt")]
        self.sylNum = len(self.syllables)
        self.wordCount = wordcount
        self.sylRatios = self.getRatios(sylratios.split(':'))
        self.sylCount = len(self.sylRatios)
        self.primes = getPrimes(self.sylNum)[-self.sylCount:]
        self.words = []
        self.start = 0

    def getRatios(self,sylratios):
        ratios = [int((self.wordCount * (int(rat))/100)//1) for rat in sylratios]
        if sum(ratios) > self.wordCount:
            print("Warning: ratios do not add up to word count. Reducing highest ratio")
            ratios[-1] = self.wordCount - sum(ratios[:-1])
        elif sum(ratios) < self.wordCount:
            print("Warning: ratios do not add up to word count. Increasing highest ratio")
            ratios[-1] += self.wordCount - sum(ratios)
        for ratio in range(len(ratios)):
            if ratios[ratio] > self.sylNum**(ratio+1):
                if ratio < len(ratios):
                    ratios[ratio+1] += ratios[ratio] - self.sylNum**(ratio+1)
                    print(f"Warning: words requested with syllable length {ratio+1} requires more syllables than "
                          f"possible. Limiting these syllable words and increasing the next highest syllable words.")
                else:
                    print("Warning: more words requested than syllables possible")
                ratios[ratio] = self.sylNum**(ratio+1)
        return ratios

    def genBySyl(self,currWords,ratios,indices,syl):
        for s in range(self.sylRatios[ratios]):
            while indices[syl] >= self.sylNum:
                indices[syl] -= self.sylNum
                if indices[syl] < 0:
                    indices[syl] += self.primes[syl]
            currWords[s] += self.syllables[indices[syl]]
            indices[syl] += self.primes[syl]
            print(f"Elapsed time = {round((time.time()-self.start),2)} ... Generating word {currWords[s]}",end="\r")

    def genWords(self):
        indices = self.primes
        for ratios in range(self.sylCount):
            random.shuffle(self.syllables)
            currWords = ['']*self.sylRatios[ratios]
            for syl in range(ratios+1):
                self.genBySyl(currWords,ratios,indices,syl)
            self.words += currWords

    def writeWords(self):
        self.start = time.time()
        self.genWords()
        with open(self.direct+"/outputs/words0.txt",'w') as outfile:
            outfile.write('\n'.join(self.words))