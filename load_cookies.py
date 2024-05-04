import json
from rich.console import Console

c = Console()
with open('five_letter_words.json', 'r') as file:
        five_letter_words = json.load(file)

first_guesses = {}
for word in five_letter_words.keys():
    if 's' in word and 'e' in word and 'a' in word and 'o' in word and 'r' in word:
        first_guesses[word] = 1

c.print(first_guesses)