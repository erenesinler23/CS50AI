import nltk
import sys
import re

nltk.download('punkt')

# You can add more terminals and non-terminals if you want to parse your own sentence.
# you can run python parser.py if you want to input your own sentence instead of 
# python parser.py sentences/x.txt

# Terminals are the individual words, punctuation marks, or basic units in a language.
TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

# Nonterminals are symbolic representations that serve as placeholders for abstract syntactic. 
NONTERMINALS = """
S -> NP VP | NP VP PP
AP -> Adv | Adj AP | Adj
NP -> N | Det NP | AP NP | N PP | NP CP | NP Adv | Adv NP
CP -> Conj S | Conj VP
PP -> P NP | P S
VP -> V | V NP | V NP PP | Adv V NP | V Adv CP
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    # Tokenize the sentence into words using nltk's word_tokenize function
    words = nltk.word_tokenize(sentence)
    # Initialize an empty list to store preprocessed words

    # Iterate through each word in the tokenized sentence
    wordList = []
    for word in words:
        # Check if the word contains at least one alphabetic character
        if re.search(".*[a-zA-Z]+.*", word) is not None:
            # Convert the word to lowercase and add it to the list
            wordList.append(word.lower())

    # Return the list of preprocessed words
    return wordList


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    # Initialize an empty list to store noun phrase chunks
    np_chunks = []

    # Iterate through subtrees of the syntax tree with the label 'NP' (Noun Phrase)
    for subtree in tree.subtrees(filter=lambda t: t.label() == 'NP' and not any(sub.label() == 'NP' for sub in t.subtrees())):
        # Add the subtree to the list of noun phrase chunks
        np_chunks.append(subtree)

    # Return the list of noun phrase chunks
    return np_chunks


if __name__ == "__main__":
    main()
