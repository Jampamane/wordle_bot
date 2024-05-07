import time
import json
import random
import os

from rich.live import Live
from rich.table import Table

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Wordle():

    NYT_WEBSITE = "https://www.nytimes.com/games/wordle/index.html"
    ROW_CLASS = "Row-module_row__pwpBq"
    TILE_CLASS = "Tile-module_tile__UWEHN"
    CSS_EMPTY = ".Tile-module_tile__UWEHN[data-state=empty]"
    CSS_ABSENT = ".Tile-module_tile__UWEHN[data-state=absent]"
    CSS_CORRECT = ".Tile-module_tile__UWEHN[data-state=correct]"
    CSS_PRESENT = ".Tile-module_tile__UWEHN[data-state=present]"
    ABSOLUTE_PATH = os.path.dirname(__file__)
    FIVE_LETTER_WORDS_RELATIVE_PATH = "five_letter_words.json"
    FIVE_LETTER_WORDS_ABSOLUTE_PATH = os.path.join(ABSOLUTE_PATH, FIVE_LETTER_WORDS_RELATIVE_PATH)
    with open(FIVE_LETTER_WORDS_ABSOLUTE_PATH, 'r') as file:
        FIVE_LETTER_WORDS = json.load(file)

    def __init__(self) -> None:
        self.potential_words = self.FIVE_LETTER_WORDS
        self.wordle = {
            "letters": {
                1 : {"correct": "", "incorrect": []},
                2 : {"correct": "", "incorrect": []},
                3 : {"correct": "", "incorrect": []},
                4 : {"correct": "", "incorrect": []},
                5 : {"correct": "", "incorrect": []},
            },
            "absent_letters": [],
            "present_letters": []}
        self.table = self.build_table()
        options = Options()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument('--log-level=3')
        # options.add_argument('--headless')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        self.browser = Chrome(options=options)
        self.action_chains = ActionChains(self.browser)
        self.browser.get(self.NYT_WEBSITE)
        play = WebDriverWait(self.browser, 10).until(
        EC.presence_of_element_located((
            By.CLASS_NAME, "Welcome-module_button__ZG0Zh")))
        play.click()
        time.sleep(1)
        self.action_chains.send_keys(Keys.ESCAPE).perform()
        time.sleep(1)

    def build_table(self) -> Table:
        table = Table(title="Wordle")
        table.add_column("Guess", justify="center")
        table.add_column("1")
        table.add_column("2")
        table.add_column("3")
        table.add_column("4")
        table.add_column("5")
        return table

    def submit_guess(self, guess: str, row_number: int) -> bool:
        for letter in guess:
            self.action_chains.send_keys(letter).perform()
            time.sleep(0.1)
        self.action_chains.send_keys(Keys.ENTER).perform()
        time.sleep(3)

        row = self.browser.find_elements(By.CLASS_NAME, self.ROW_CLASS)[row_number - 1]
        tiles = row.find_elements(By.CLASS_NAME, self.TILE_CLASS)
        for letter in tiles:
            letter_check = letter.get_attribute("data-state")
            if letter_check == "tbd":
                return False
        return True

    def is_letter_duplicate(self, letter, word):
        count = 0
        for l in word:
            if l == letter:
                count += 1
        if count > 1:
            return True
        return False

    def update_wordle(self, row_number: int, word: str) -> None:
        row = self.browser.find_elements(By.CLASS_NAME, self.ROW_CLASS)[row_number - 1]
        tiles = row.find_elements(By.CLASS_NAME, self.TILE_CLASS)
        for indx, letter in enumerate(tiles, start=1):
            duplicate_check = self.is_letter_duplicate(letter=letter.text.lower(), word=word)
            letter_check = letter.get_attribute("data-state")
            if letter_check == "absent":
                if duplicate_check is True:
                    self.wordle["letters"][indx]["incorrect"].append(letter.text.lower())
                else:
                    self.wordle["absent_letters"].append(letter.text.lower())
            elif letter_check == "correct":
                self.wordle["letters"][indx]["correct"] = letter.text.lower()
                self.wordle["present_letters"].append(letter.text.lower())
            elif letter_check == "present":
                self.wordle["present_letters"].append(letter.text.lower())
                self.wordle["letters"][indx]["incorrect"].append(letter.text.lower())



    def update_table(self, row_number: int):
        style_dict = {
            "absent": "grey53",
            "present": "yellow bold",
            "correct": "green bold",
            "tbd": "red"
            }
        table_list = []
        table_list.append((row_number, "cyan bold"))
        row = self.browser.find_elements(By.CLASS_NAME, self.ROW_CLASS)[row_number - 1]
        tiles = row.find_elements(By.CLASS_NAME, self.TILE_CLASS)
        for letter in tiles:
            letter_check = letter.get_attribute("data-state")
            table_list.append((letter.text, style_dict[letter_check]))

        self.table.add_row(
            f"[{table_list[0][1]}]{table_list[0][0]}",
            f"[{table_list[1][1]}]{table_list[1][0]}",
            f"[{table_list[2][1]}]{table_list[2][0]}",
            f"[{table_list[3][1]}]{table_list[3][0]}",
            f"[{table_list[4][1]}]{table_list[4][0]}",
            f"[{table_list[5][1]}]{table_list[5][0]}",
        )
        self.table.add_section()

    def check_for_present_letters(self, word):
        if self.wordle['present_letters']:
            for present_letter in self.wordle['present_letters']:
                if present_letter not in word:
                    return False
        return True


    def get_potential_words(self):
        potential_words = {}
        for word in self.potential_words.keys():
            if self.check_for_present_letters(word) is False:
                continue

            for indx, letter in enumerate(word, start=1):
                if letter in self.wordle['absent_letters']:
                    break
                if letter in self.wordle['letters'][indx]['incorrect']:
                    break

                if not self.wordle['letters'][indx]['correct']:
                    pass
                elif letter != self.wordle['letters'][indx]['correct']:
                    break

                if indx == 5:
                    potential_words[word] = 1
        return potential_words


    def check_for_win(self):
        for indx in range(1, 6):
            if not self.wordle['letters'][indx]['correct']:
                return False
        return True


    def delete_guess(self, guess: str):
        for _ in range(6):
            self.action_chains.send_keys(Keys.BACK_SPACE).perform()
            time.sleep(0.1)
        try:
            self.potential_words.pop(guess)
        except KeyError:
            pass
        self.FIVE_LETTER_WORDS.pop(guess)

        with open(self.FIVE_LETTER_WORDS_ABSOLUTE_PATH, 'w') as file:
            file.write(json.dumps(self.FIVE_LETTER_WORDS, indent=1))


    def _solve_hard(self, first_guess: str) -> bool:
        with Live(self.table) as live:
            if self.submit_guess(guess=first_guess, row_number=1) is False:
                raise ValueError("You have provided an invalid first guess.")
            self.update_wordle(row_number=1, word=first_guess)
            self.update_table(row_number=1)
            live.update(self.table)
            for indx in range(2, 7):
                if self.check_for_win() is True:
                    return True
                self.potential_words = self.get_potential_words()
                new_guess = random.choice(list(self.potential_words.keys()))
                print(new_guess)
                while self.submit_guess(guess=new_guess, row_number=indx) is False:
                    print(f"{new_guess} is bad guess")
                    self.delete_guess(new_guess)  
                    new_guess = random.choice(list(self.potential_words.keys()))
                    print(new_guess)
                self.update_wordle(row_number=indx, word=new_guess)
                self.update_table(row_number=indx)
                live.update(self.table)

        if self.check_for_win() is True:
                return True
        return False
    
    def _easy_mode_get_guess(self):
        good_guesses = []
        availible_letters = {}
        for word in self.potential_words.keys():
            for letter in word:
                availible_letters[letter] = 1

        for indx in range(1, 6):
            try:
                availible_letters.pop(self.wordle["letters"][indx]["correct"])
            except KeyError:
                pass

        for word in self.FIVE_LETTER_WORDS:
            for index, letter in enumerate(word, start=1):
                if letter in self.wordle["letters"][index]["incorrect"]:
                    break

                if letter not in list(availible_letters.keys()):
                    break

                good_guesses.append(word)

        try:
            guess = random.choice(good_guesses)
        except IndexError:
            guess = random.choice(list(self.potential_words.keys()))
        return guess

            

        
    
    def _solve_easy(self, first_guess: str):
         with Live(self.table) as live:
            if self.submit_guess(guess=first_guess, row_number=1) is False:
                raise ValueError("You have provided an invalid first guess.")
            self.update_wordle(row_number=1, word=first_guess)
            self.update_table(row_number=1)
            live.update(self.table)
            for indx in range(2, 7):
                if self.check_for_win() is True:
                    return True
                self.potential_words = self.get_potential_words()
                new_guess = self._easy_mode_get_guess()
                print(new_guess)
                while self.submit_guess(guess=new_guess, row_number=indx) is False:
                    print(f"{new_guess} is bad guess")
                    self.delete_guess(new_guess)  
                    new_guess = self._easy_mode_get_guess()
                    print(new_guess)
                self.update_wordle(row_number=indx, word=new_guess)
                self.update_table(row_number=indx)
                live.update(self.table)
    
    def solve(self, mode: str="hard", first_guess: str="arose"):
        if mode == "hard":
            win = self._solve_hard(first_guess=first_guess)
            if win is True:
                print("You win!")
            else:
                print("You lose...")
        elif mode == "easy":
            self._solve_easy(first_guess=first_guess)