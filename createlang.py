'''             CREATE LANGUAGE             '''
# This file creates an entire language with all stages given an input direcectory

import sys, os
from sylconstr import SylConst
from wordconstr import WordGen
from IPA import IPA

def checkSWCDirect(args):
    if len(args) > 1:
        swc = args[0].lower()
        direct = args[1]
    else:
        print(
            "Error: Not enough arguments. Please enter at least syllable/word/change (swc) mode and language directory.")
        sys.exit()
    if direct in os.listdir():
        if 'inputs' not in os.listdir(direct):
            print("Error:", direct, "does not have an inputs directory.")
            sys.exit()
    else:
        print("Error:", direct, "does not exist.")
        sys.exit()
    return swc, direct


def checkCountRat(args):
    wordcount, ratios = 100, "15:51:34"
    for i in range(2,4):
        if len(args) > i:
            if ":" in args[i] and [_ for _ in args[i].split(":") if _.isdigit()]:
                ratios = args[i]
            elif args[i].isdigit():
                wordcount = int(args[i])
            else:
                print("Error: invalid argument at argument",i)
                sys.exit()
    return wordcount, ratios


def checkArgs(args):
    swc, direct = checkSWCDirect(args)
    wordcount, ratios = checkCountRat(args)
    return swc, direct, wordcount, ratios


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    args = sys.argv[1:]
    swc, direct, wordcount, ratios = checkArgs(args)

    IPAf = IPA(direct)

    syls = []
    words = []
    changes = []

    if "s" in swc:
        sylConstructor = SylConst(direct,IPAf)
        sylConstructor.writeSyls()
        syls = sylConstructor.getSyls()

    if "w" in swc:
        wordGenerator = WordGen(direct,wordcount,ratios,syls)
        wordGenerator.writeWords()
        words = wordGenerator.getWords()


