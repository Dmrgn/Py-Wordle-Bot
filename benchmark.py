import pyautogui as pa
import time
import string
import itertools
import random
from wordfreq import zipf_frequency
from spellchecker import SpellChecker
spell = SpellChecker()

# comparator function to sort word bank by frequency
def compareFreq(elm):
    return zipf_frequency(elm, 'en')
# All known 5 letter words
allwords = sorted(list(spell.known([''.join(x) for x in itertools.product(string.ascii_lowercase, repeat=5)])), reverse=True, key=compareFreq)
bank = allwords.copy()
# answer to the wordle
answer = random.choice(bank)
# currenly guessed word
word = "crane"
# known letters in their position
correctOrder = [" "," "," "," "," "]
# know letters in incorrect positions e.g:
# wrongOrder = {"h":[0,1],"l":[4,2],"m":[3]}
# h was correct but in the wrong order at positions 0 and 1
# l was correct but in the wrong order at positions 4 and 2
# m was correct but in the wrong order at position 3
wrongOrder = {}
# incorrect letters
wrongLetters = set()
# Top left is 478,448
x = 508; y = 478; width = 62
row = 0
# grey incorrect
grey = (58,58,60)
# yellow wrong place
yellow = (177,161,69)
# green correct
green = (93, 139, 82)
# map each colour to an int
colmap = [grey, yellow, green]

# get which letters in row are correct, in the wrong place, wrong
def getRowData():
    # array mapping what state the current letter is in 0=wrong 1=wrong place 2=correct
    pos = []
    for i in range(5):
        if word[i] in answer:
            if word[i] == answer[i]:
                pos.append(2)
            else:
                pos.append(1)
        else:
            pos.append(0)
    return pos

# checks if the passed word matches parameters of correctWords and wrongOrder
def checkCorrect(passed):
    for key, value in wrongOrder.items():
        if not(key in passed):
            return False
    for i in range(5):
        if passed[i] in wrongLetters:
            return False
        if correctOrder[i] != " ":
            if not(passed[i] == correctOrder[i]):
                return False
        for key, value in wrongOrder.items():
            if (passed[i] == key) and (i in value):
                return False
    return True

# refines the list of possible 5 letter words based on restrictions
def refineOptions():
    filtered = list(filter(checkCorrect, bank))
    return filtered
    

# gets gets state of the previous row and returns the next guess
def playRow():
    global bank, row
    # get the current row
    state = getRowData()
    # increment row
    row = row+1
    # add correct letters to letter array
    for x in range(len(state)):
        if state[x] == 1:
            if word[x] in wrongOrder:
                wrongOrder[word[x]].append(x)
            else:
                wrongOrder[word[x]] = [x]
        elif state[x] == 2:
            correctOrder[x] = word[x]
        else:
            wrongLetters.add(word[x])
    # check if correct order is complete
    if not " " in correctOrder:
        return "".join(correctOrder)
    # refine the search 
    bank = refineOptions()
    return False

guesses = []

print("Starting!")
start = time.time()

for x in range(2500):
    answer = allwords[x]
    row = 0
    word = "crane"
    correctOrder = [" "," "," "," "," "]
    wrongOrder = {}
    wrongLetters = set()
    isSolved = playRow()
    while not(isSolved) and row < 6:
        word = bank[0]
        isSolved = playRow()
    print("Found that the word was",answer,"after",row,"guesses")
    guesses.append(row)
    bank = allwords.copy()

print("In set of",len(guesses),"words, we took an average of",sum(guesses)/len(guesses),"guesses per word.")

print("That took", (time.time()-start), "seconds")

