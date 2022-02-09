'''             Tests           '''
from createlang import *

os.chdir(os.path.dirname(os.path.abspath(__file__)))
args = sys.argv[1:]
swc, direct, wordcount, ratios = checkArgs(args)

IPAf = IPA(direct)

def test_IPA_phonemes():



syls = []
words = []
changes = []

if "s" in swc:
    sylConstructor = SylConst(direct, IPAf)
    sylConstructor.writeSyls()
    syls = sylConstructor.getSyls()

if "w" in swc:
    wordGenerator = WordGen(direct, wordcount, ratios, syls)
    wordGenerator.writeWords()
    words = wordGenerator.getWords()