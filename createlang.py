'''             CREATE LANGUAGE             '''
# This file creates an entire language with all stages given an input directory

import sylconstr
import wordconstr
import soundchange
import sys
import os


def createLanguage(swc,dir,syls,wordcount):
    if 's' in swc:
        sylconstr.constructSyls(dir)
    if 'w' in swc:
        wordconstr.makeWords(dir,syls,wordcount)
    if 'c' in swc:
        soundchange.allChanges(dir)


if __name__ == "__main__":
    arguments = sys.argv[1:]
    swc = arguments[0]
    dir = arguments[1]
    abort = False
    try:
        if len(os.listdir(dir)) == 0:
            print(dir,"is empty. Aborting.")
            abort = True
        else:
            if 'inputs' not in os.listdir(dir):
                print(dir,"does not have an inputs directory. Aborting.")
                abort = True
            if 'outputs' not in os.listdir(dir):
                print(dir,"does not have an outputs directory. Aborting.")
                abort = True
    except IOError:
        print(dir,"does not exist. Aborting.")
        abort = True
    if not abort:
        syls = 3
        if len(arguments) > 2:
            syls = int(sys.argv[3])
        wordcount = 10000
        if len(arguments) > 3:
            wordcount = int(sys.argv[4])
        createLanguage(swc,dir,syls,wordcount)