"""Main function that handles creating an instance and solving wordle."""
from wordle import Wordle
import json

def main():
    """Create a wordle class and calls the solve method."""
    with open(Wordle.FIVE_LETTER_WORDS_ABSOLUTE_PATH, 'r', encoding="utf-8") as file:
        five_letter_words = json.load(file)
    i = 0
    words = {}
    for indx, word in enumerate(list(five_letter_words.keys())):
        words[indx] = word
    while True:
        wordle = Wordle(headless=True)
        i = wordle.process_words(word_list=words, indx=i)
        wordle.browser.quit()


if __name__ == "__main__":
    main()
