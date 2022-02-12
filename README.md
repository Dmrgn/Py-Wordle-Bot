# Py-Wordle-Bot
A python bot for the popular word game Wordle

Makes use of the following python modules:
- [pyautogui](https://pypi.org/project/PyAutoGUI/)
- [wordfreq](https://pypi.org/project/wordfreq/)
- [pyspellchecker](https://pypi.org/project/pyspellchecker/)

Which can be installed by running:
```
pip install pyautogui
pip install pyspellchecker
pip install wordfreq
```

The bot follows the following algorithm:
- Generate "bank" a list of all valid 5 letter english words
- Sort "bank" from most common to least commonly used
- Guess "crane"
- Read the resulting response from the game and update guess requirments
- While we have not solved the puzzle
  - Remove all words from bank which do not meet the guess requirments
  - Guess the word at the first index of "bank"
  - Read the resulting response from the game and update guess requirments
