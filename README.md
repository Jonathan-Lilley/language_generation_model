------------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
                                             LANGUAGE GENERATOR
------------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------

Overview:

This is half of a final project for a Diachronic Linguistics (historical linguistics) course. The purpose of this half
of the project is to design a program that can generate a "toy language" given sounds and sound rules and evolutionary
stages given sound change rules. It can be used to model real languages and their descendants or constructed languages.
All of the parts of a language constructed by this program are organized into a single directory with that language's
name (e.g. "L1", "L2", etc.)

This program is made to be highly modifiable and capable of adjusting to many different forms of input. This means that
the IPA directory can be edited as needed to accommodate whatever language is being developed. However, the key feature
is that the only thing that needs to be edited are the text files (the IPA{C/V}.txt, IPA{C/V}KEY.txt, and language
directory files). The python files should need no modification (ideally). This makes this project useful for anyone who
does not wish to spend excessive amounts of time programming but wants to utilize what this program has to offer.

README TOC:
    IPA directory
    Contents of language directories
    The program

------------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
                                                  IPA directory

The files:
IPAC.txt -- The consonants IPA chart
IPAV.txt -- The vowels IPA chart
IPACKEY.txt -- The lookup keys for IPAC.txt
IPAVKEY.txt -- The lookup keys for IPAV.txt

These files can be modified to add, remove, or rearrange sounds as needed/desired.


-- Format of IPAC.txt --

                                 0   1   2   3   4   5   6   7   8   9  10
                            0   b,p 0,0 0,0 d,t 0,0 ɖ,ʈ ɟ,c g,k ɢ,q 0,0 0,ʔ
                            1   β,ɸ v,f ð,θ z,s ʒ,ʃ ʐ,ʂ ʝ,ç ɣ,x ʁ,χ ʕ,ħ ɦ,h
                            2   0,0 0,0 0,0 ɮ,ɬ 0,0 0,0 0,0 0,0 0,0 0,0 0,0
                            3   m,0 ɱ,0 0,0 n,0 0,0 ɳ,0 ɲ,0 ŋ,0 ɴ,0 0,0 0,0
                            4   w,0 ʋ,0 0,0 ɹ,0 0,0 ɻ,0 j,0 ɰ,0 0,0 0,0 0,0
                            5   0,0 0,0 0,0 l,0 0,0 ɭ,0 ʎ,0 ʟ,0 0,0 0,0 0,0
                            6   ʙ,0 0,0 0,0 r,0 0,0 0,0 0,0 0,0 ʀ,0 0,0 0,0
                            7   0,0 ⱱ,0 0,0 ɾ,0 0,0 ɽ,0 0,0 0,0 0,0 0,0 0,0

This is the standard IPA consonants chart (although the voiced and voiceless consonants are flipped). 0 represents
a sound not found in the IPA.
(The numbered rows and columns are not present in the file, they are solely so that the IPACKEY.txt format is explained
better)


-- Format of IPACKEY.txt --

                                        ATTRIBUTE range,range;dimension
where
    ATTRIBUTE = 4-letter abbreviation for attribute name
    range,range = bottom to top of index range
    dimension = place/manner/voicing dimension for range (0 = place, 1 = manner, 2 = voicing)

Since IPAC is read in as a 3 dimensional array, the way sets of sounds are extracted is by finding the ranges in which
they reside. To find a singular sound, you can input three attributes: place, manner, and voicing. You are more likely,
however, to use this to find sets of sounds that fall under certain categories, such as voiced stops or alveolar
fricatives.
This was designed to directly mimic how phonological feature systems work. It was implemented with phonological rules
and syllable rules in mind, specifically for constructing syllables and implementing sound changes (see below).

Some examples (see the IPAC table for reference to see how this works)

CONS 0,0;0 -- All consonants (this is special, the IPA reading file will interpret this value as instructions to fill in
                the entire chart)
NASA 3,4;0 -- Nasals
CONT 1,5;0 -- Continuants
DENT 2,3;1 -- Dentals
DORS 5,11;1 -- Dorsals
VLSS 1,2;2 -- Voiceless


-- Format of IPAV.txt --

                                                     1   2   3
                                                1   i,y ɨ,ʉ ɯ,u
                                                2   ɪ,ʏ 0,0 0,ʊ
                                                3   e,ø ɘ,ɵ ɤ,o
                                                4   0,0 ə,0 0,0
                                                5   ɛ,œ ɜ,ɞ ʌ,ɔ
                                                6   æ,0 ɐ,0 0,0
                                                7   a,ɶ 0,0 ɑ,ɒ

This is the standard IPA chart for vowels. Note that there are 7 height levels instead of 4: 2 and 6 represent
near-closed and near-open, respectively, since they do not have their own formal tiers in the IPA; 4 represents mid,
which also does not have its own tier. Again, 0 represents sounds not found in the IPA.
(The numbered rows and columns are not present in the file, they are solely so that the IPAVKEY.txt format is explained
better)


-- Format of IPAVKEY.txt --

                                        ATTRIBUTE range,range;dimension
where
    ATTRIBUTE = 4-letter abbreviation for attribute name
    range,range = bottom to top of index range
    dimension = place/manner/voicing dimension for range (0 = height, 1 = backness, 2 = rounding)

Since IPAV is read in as a 3 dimensional array, the way sets of sounds are extracted is by finding the ranges in which
they reside. To find a singular sound, you can input three attributes: height, backness, and rounding. You are more
likely, however, to use this to find sets of sounds that fall under certain categories, such as front high vowels or
back round vowels.
This was designed to directly mimic how phonological feature systems work. It was implemented with phonological rules
and syllable rules in mind, specifically for constructing syllables and implementing sound changes (see below).

Some examples (see the IPAV table for reference to see how this works)

VOWL 0,0;0 -- All vowels (see: all consonants in previous section for explanation)
MIDC 2,3;0 -- Mid-closed vowels
MIDV 3,4;0 -- Mid-vowels (schwa)
CENT 1,2;1 -- Central vowels
ROND 1,2;2 -- Round vowels



------------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
                                      Contents of a language's directory

The inputs directory:
- changes{n}.txt -- The diachronic sound changes for the language from stage n-1 to stage n
- phonemes.txt -- All of the phonemes found in the language at stage 0
- sylstructs.txt -- All of the syllable structure rules found in the language at stage 0

The outputs directory:
- syllables.txt -- All the possible syllables for the language at stage 0
- words0.txt -- n randomly generated words with up to m syllables per word, where n and m are user-defined
- words{n}.txt -- All of the words from the file words0.txt after undergoing changes from the changes{n}.txt file


                                             Input file formats

-- changes{n}.txt --

This text file takes the form of classic rewrite rules found in synchronic and diachronic phonology.
The following is the general format:
                                                i>o/c1 _ c2
where
    i = input phoneme
    > = becomes
    o = output phoneme
    / = in the context of
    c1 = context 1
    _ = position of i
    c2 = context 2

Further detail:
i, o, c1, and c2 can take the form of individual phonemes (or sequences of phonemes in the case of c1 and c2), or they
can take the form of phoneme set descriptors. These phoneme set descriptors can be modified in the IPACKEY.txt and
IPAVKEY.txt files. See the IPA section above for explanation of how these descriptors work.

w>0/_ +CLOS,+BACK
    w deletes before closed back vowels
s>θ/# _
    s becomes θ word initially
a>æ/+CONS _ +CONS
    a becomes æ between consonants
*+NRCL,BACKNESS:a,ROUNDING:a>+CLOS,BACKNESS:a,ROUNDING:a/_
    *Near closed back vowels become their closed counterparts everywhere
*+LATA>+LATA,PLACE:a/_ +APPR,PLACE:a
    *Lateral approximants assimilate to place of articulation before approximants

*** \*NOTE ABOUT {X}:a ***
All rules above marked with * contain at least two phoneme set descriptors with an attribute {X}:a.
This notation has one function that is used in two ways. It is based on α-notation (alpha-notation).

Function: This notation tells the program to create multiple rules based on one rule, replacing the attribute with
all its possible realizations (PLACE>BILA,LABD,DENT,etc;ROUNDING>ROND,URND;etc) -- but specifically, it will always
replace {X}:a with the same realization. In other words, {X}:a will generate a set of parallel rules. Example:
PLACE:a>+STOP,PLACE:a becomes +BILA>+STOP,+BILA; +ALVE>+STOP,+ALVE; etc.

Use 1: This allows for us to make sure all sound that change in one attribute to retain their other attributes. This
is because if we input a traditional rule STOP>VOICED/_VOICED, where t would become d before b, g, etc., unless we
use this specific strategy, t will become _all_ voiced stops before voiced consonants. In other words, t will become
b and g as well as d. The {X}:a format requires all stops tht become voiced to retain their other qualities. Thus,
t will only become d.

Use 2: We can also use it for the traditional usage of alpha. In this case, we can make the output phoneme mirror
the context phonemes in some aspect.


-- phonemes.txt --

This textfile contains all the phonemes used for stage 0 of the language.
This is the format:

                                            i ɪ e ɛ u ʊ o ɔ a
                                            p b f d t s n ɹ l g k

The file can have any number of lines for organization's sake, so long as all the phonemes are separated by either a
single space or a newline.


-- sylstructs.txt --

This textfile contains the rules required for syllable structures.
This is the format:

                   ;+CONS;+CONS,-APPR +APPR;p f;t s;s n|+VOWL|;+CONS;+APPR +CONS,-APPR;f p;s t;n s

This file is split on bars to separate the onsets (before the first bar), nuclei (between bars), and codas (after
second bar). Then, each syllable segment is split on semicolons. This allows the generator to create all the possible
syllable combinations.


                                             Output file formats

-- syllables.txt --

This file contains all possible syllables for language stage 0 given the phonemes and syllable structures. It is
created in order to generate words for words0.txt.


-- words0.txt --

This file contains a user-set number of words of up to a user-set number of syllables (the amount of words per syllable
level is weighted and pre-defined, see below).


-- words{n}.txt --

This file contains the words from words{n-1}.txt after having undergone the changes from changes{n}.txt



------------------------------------------------------------------------------------------------------------------------
                                                The program




















