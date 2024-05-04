import random
import time
from wordle import Wordle
from rich.console import Console







def main():
    wordle = Wordle()
    wordle.submit_guess(guess='jocks', row_number=1)
    wordle.update_wordle(row_number=1)
    for indx in range(2, 7):
        if wordle.check_for_win() is True:
            print("You win!")
            time.sleep(5)
            raise SystemExit
        potential_words = wordle.get_potential_words()
        time.sleep(2)
        new_guess = random.choice(list(potential_words.keys()))
        while wordle.submit_guess(guess=new_guess, row_number=indx) is False:
            potential_words.pop(new_guess)
            new_guess = random.choice(list(potential_words.keys()))
        wordle.update_wordle(row_number=indx)

    #import IPython; IPython.embed(); quit()

if __name__ == "__main__":
    main()
