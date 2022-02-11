# Language Generation Model

This was half of a final project for a Diachronic Linguistics (historical linguistics) course. Since then, this project 
has been reworked so that it is written cleaner and runs faster. However, there are still bugs in parts of it. Please 
send me an email if you find any you wish to be fixed so that I can look into them.
------------------------------------------------------------------------------------------------------------------------

## Overview

This project, which I have called a Language Generation Model, is a highly modular, flexible, and powerful data
augmentation model designed for creating and enhancing linguistic data for use in computational phonology and morphology
tasks. It is designed for linguists and uses traditional phonology terminology and concepts. Specifically, this model
uses the rule-based phonology models.

This program takes in a directory of (customizable) IPA data and a directory of phonology rule files and outputs a
directory of syllable and word files generated from the input data. It can model regular synchronic and diachronic sound
changes as the user desires and specifies, and it can model all of this in the context of a set of phonemes and classes
as specified by the IPA input directory.

The LSample directory is a core example that uses all the "standard" IPA information and some basic syllable 
constructions and sound sound change rules.

------------------------------------------------------------------------------------------------------------------------

### README TOC:
- [Quick guide](##quickguide)
- [The IPA directory](##theipadirectory)
- [Contents of language directories](##Contents of a language's directory)

------------------------------------------------------------------------------------------------------------------------

## Quick guide 

If you wish to start using this program right away but don't care about the details of how it works, start with this
section.

The three things you need to utilize this program are:
- A set of phonemes
- A set of syllable rules
- One or more sets of sound changes (optional)

If you want to learn more about how to use these in more detail, check out the sections below.

#### Step 1.

Create a directory *MyLang* with two subdirectories, *inputs* and *IPA*

#### Step 2.

Create a file in the inputs directory named phonemes.txt. Enter your phonemes into this file, each separated by either a
space or a newline, and save. **Separating them with any other characters, including tabs, will throw an error.**

#### Step 3.

Create a file in the inputs directory named sylstructs.txt. Enter your syllable rules, and format them such that the 
onset, nucleus, and coda are separated by the | symbol, and each subset of the onset, nucleus, and coda are sparated by 
the ; symbol.

#### Step 4.

Create any number of changes#.txt files, where # starts at 1 and goes up by 1 each time. Fill these in with synchronic
or diachronic sound change rules (see IPA directory again for explanation on sets). Sound changes will be applied from 
first to last.

#### Step 5.

Run the program. In the terminal, navigate to the main directory, and enter the following command.

`python createlang.py swc MyLanguageDirectory <# of words> <syllable ratios>`

This will generate all the syllables possible in the language in `MyLanguageDirectory`, a number of words equal to 
`<# of words>` with syllable distributions proportionate to `<syllable ratios>`, which must add up to 100 (e.g. 
`10:50:40` will yield 10% 1-syllable, 50% 2-syllable, and 40% 3-syllable), and all their evolutionary stages as 
described in your changes files. If you are opting not to have sound changes, you can remove the `c` from `swc`, and if
you only wish to generate the syllables you can remove the `wc` from `swc`.

------------------------------------------------------------------------------------------------------------------------
## The IPA directory                                                  

The IPA directory contains all the information about the IPA symbols and their classes. For a basic setup, check the 
LSample directory. It contains the "standard" IPA and IPA sets. Those are included below as examples.

### The files:
- **IPAC.txt** -- The consonants IPA chart
- **IPAV.txt** -- The vowels IPA chart
- **IPACKEY.txt** -- The lookup keys for IPAC.txt
- **IPAVKEY.txt** -- The lookup keys for IPAV.txt

These files can be modified to add, remove, or rearrange sounds as needed/desired.


### -- Format of IPAC.txt --

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


### -- Format of IPACKEY.txt --

       ATTRIBUTE start,end;dimension

where
    
        ATTRIBUTE = 4-letter abbreviation for attribute name
        start,end = start to end of index range
        dimension = place/manner/voicing dimension for range (0 = place, 1 = manner, 2 = voicing)

Since IPAC is read in as a 3 dimensional array, the way sets of sounds are extracted is by finding the ranges in which
they reside. To find a singular sound, you can input three attributes: place, manner, and voicing. You are more likely,
however, to use this to find sets of sounds that fall under certain categories, such as voiced stops or alveolar
fricatives.

This was designed to directly mimic how phonological feature systems work. It was implemented with phonological rules
and syllable rules in mind, specifically for constructing syllables and implementing sound changes (see below).

This feature is also designed to be modifiable. If you have a langauge in which bilabials are a non-class, you can 
simply remove it from the keys -- and, if you have a non-natural class of phonemes that doesn't exist in any language,
you can include that in the keys for your own purposes. (This could be powerful for conlangers.)

Some examples (see the IPAC table for reference to see how this works)

    CONS 0,0;0 -- All consonants (this is special, the IPA reading file will interpret this value 
                    as instructions to fill in the entire chart)
    NASA 3,4;0 -- Nasals
    CONT 1,5;0 -- Continuants
    DENT 2,3;1 -- Dentals
    DORS 5,11;1 -- Dorsals
    VLSS 1,2;2 -- Voiceless


### -- Format of IPAV.txt --

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


### -- Format of IPAVKEY.txt --

      ATTRIBUTE range,range;dimension
where

    ATTRIBUTE = 4-letter abbreviation for attribute name
    range,range = bottom to top of index range
    dimension = height/backness/rounding dimension for range (0 = height, 1 = backness, 2 = rounding)

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

### IPA Directory Notes

1. For sounds that are modified with diacritics, such as nasalized vowels, it is encouraged that you experiment with
digraphs. To use diagraphs in this program, it is recommended that you take an existing symbol (e.g. `i`) and put
put a symbol on each side of it (e.g. `NiN`). Unfortunately, due to the nature of the program, if you were to attach
a digraph to either side of the symbol (e.g. `iN` or `Ni`), it would be changed in certain contexts of sound changes
that may be unexpected -- using a digraph on each side is the only way to prevent such unexpected behavior. However,
this also opens up the opportunity to use multiple digraph symbols to express nuance, e.g. `NiV` can indicate
nasalized `i` with falling intonation. Play around with it!

2. It is recommended that when editing the charts, you minimize the work you have to do for yourself while still making
it functional for your own purposes. For example, if modeling French vowels, it would be recommended to add a third and
fourth value to the roundness dimension (2) (e.g. `i,y,NiN,NyN` as a vowel value). This way, you can have ɛ,œ,NɛN,NœN 
where N means nasalized, and you do the same for all other nasal vowels. If you do this, it is easy to add NASL 2,4;2 
(nasalized), URNA 2,3;2 (unround nasal), and RONA 3,4;2 (rounded nasal) to the IPAVKEY file. This minimizes the work you
 have to do adjusting the IPAVKEY file. If you only have a few sounds to add, such as labialized stops, it may be 
easier or make more sense to simply add a new row or column for them. Again, if you do this, be sure to adjust the KEY 
files.

------------------------------------------------------------------------------------------------------------------------
## Contents of a language's directory

### Files in the directories:

###### The inputs directory:
- changes{n}.txt -- The diachronic sound changes for the language from stage n-1 to stage n
- phonemes.txt -- All of the phonemes found in the language at stage 0
- sylstructs.txt -- All of the syllable structure rules found in the language at stage 0

###### The outputs directory:
- syllables.txt -- All the possible syllables for the language at stage 0
- words0.txt -- n randomly generated words with up to m syllables per word, where n and m are user-defined
- words{n}.txt -- All of the words from the file words0.txt after undergoing changes from the changes{n}.txt file

### Input file formats

#### -- changes{n}.txt --

This text file takes the form of classic rewrite rules found in synchronic and diachronic phonology.
The following is the general format:

    i>o/c1 _ c2

where

```
i = input phoneme
> = becomes
o = output phoneme
/ = in the context of
c1 = context 1
_ = position of i
c2 = context 2
```

Further detail:
i, o, c1, and c2 can take the form of individual phonemes (or sequences of phonemes in the case of c1 and c2), or they
can take the form of phoneme set descriptors. These phoneme set descriptors can be modified in the IPACKEY.txt and
IPAVKEY.txt files. See the IPA section above for explanation of how these descriptors work.

```
w>0/_ +CLOS,+BACK
    w deletes before closed back vowels
s>θ/# _
    s becomes θ word initially
a>æ/+CONS _ +CONS
    a becomes æ between consonants
†+NRCL,BACKNESS:a,ROUNDING:a>+CLOS,BACKNESS:a,ROUNDING:a/_
    *Near closed back vowels become their closed counterparts everywhere
†+LATA>+LATA,PLACE:a/_ +APPR,PLACE:a
    *Lateral approximants assimilate to place of articulation before approximants
```

##### † NOTE ABOUT {X}:a 

All rules above marked with † contain at least two phoneme set descriptors with an attribute {X}:a.
This notation has one function that is used in two ways. It is based on α-notation (alpha-notation).

Alpha notation in classical phonology: When you are writing a phonological rule and you want an output phoneme to match
a phoneme in the context, you can insert an "alpha value". This "alpha value" will ensure that the output phoneme and 
the context phoneme to match in one or more features.

In this program: This notation tells the program to generate multiple rules based on one rule, replacing the attribute 
with all its possible realizations (PLACE>BILA,LABD,DENT,etc;ROUNDING>ROND,URND;etc) -- but specifically, it will always
replace all values of {X}:a within a rule with the same realization. In other words, {X}:a will generate a set of 
parallel rules. Example: 

```
PLACE:a>+STOP,PLACE:a becomes +BILA>+STOP,+BILA; +ALVE>+STOP,+ALVE; +CORO>+STOP,+COROetc.
```

**Use 1:** This allows for us to make sure all sound that change in one attribute to retain their other attributes. This
is because if we input a traditional rule `STOP>VOICED/_ VOICED`, where t would become d before b, g, etc., unless we
use this specific strategy, t will become *all* voiced stops before voiced consonants. In other words, t will become
b and g as well as d. The {X}:a format requires all stops tht become voiced to retain their other qualities. Thus,
t will only become d. Explanation through example:

```
Without alhpa value:
    +STOP>+VOID/_ +VOID -->
        t>d/_ b
        t>d/_ g
        t>b/_ b
        t>b/_ g
        t>g/_ b
        t>g/_ g
    (d,b,g all voiced stops)
        
With alpha value:
    +STOP,PLACE:a>+VOID/_ +VOID -->
        t>d/_ b
        t>d/_ g
    (only d is voiced stop in the same place as t)
```

**Use 2:** We can also use it for the traditional usage of alpha. In this case, we can make the output phoneme mirror
the context phonemes in some aspect.


#### -- phonemes.txt --

This textfile contains all the phonemes used for stage 0 of the language.
This is the format:

                                        i ɪ e ɛ u ʊ o ɔ a
                                        p b f d t s n ɹ l g k

The file can have any number of lines for organization's sake, so long as all the phonemes are separated by either a
single space or a newline.


#### -- sylstructs.txt --

This textfile contains the rules required for syllable structures.
This is the format:

```
+CONS;+CONS,-APPR +APPR;p f|+VOWL|;+CONS;+APPR +CONS,-APPR;f p;
```

This file is split on bars to separate the onsets (before the first bar), nuclei (between bars), and codas (after
second bar). Then, each syllable segment is split on semicolons. This allows the generator to create all the possible
syllable combinations.

### Output file formats

#### -- syllables.txt --

This file contains all possible syllables for language stage 0 given the phonemes and syllable structures. It is
created in order to generate words for words0.txt.


##### -- words0.txt --

This file contains a user-set number of words of up to a user-set number of syllables (the amount of words per syllable
level is weighted and pre-defined, see below).


##### -- words{n}.txt --

This file contains the words from words{n-1}.txt after having undergone the changes from changes{n}.txt


