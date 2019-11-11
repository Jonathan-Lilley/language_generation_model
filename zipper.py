'''                        LANGUAGE ZIPPER                               '''

import sys

def zipWords(words1, words2):
    newwords = []
    for word in range(len(words1)):
        newwords.append(words1[word]+'\t'+words2[word])
    newwords = '\n'.join(newwords)
    return newwords

def zipFiles(dir,stagea,stageb):
    stageawords = [line.strip() for line in open(dir+"/outputs/words"+stagea+".txt")]
    stagebwords = [line.strip() for line in open(dir+"/outputs/words"+stageb+".txt")]
    zippedwords = zipWords(stageawords,stagebwords)
    zippedfile = open(dir+"/stage"+stagea+"-stage"+stageb+".txt",'w')
    zippedfile.write(zippedwords)
    zippedfile.close()

if __name__=="__main__":
    dir = sys.argv[1]
    stagea = sys.argv[2]
    stageb = sys.argv[3]
    zipFiles(dir,stagea,stageb)