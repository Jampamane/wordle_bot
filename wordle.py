import time
import json
import random
import os

from rich.live import Live
from rich.table import Table

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Wordle():

    NYT_WEBSITE = "https://www.nytimes.com/games/wordle/index.html"
    PLAY_BUTTON_CLASS = "Welcome-module_button__ZG0Zh"
    CLOSE_POPUP_CLASS = "Modal-module_closeIconButton__y9b6c"
    ROW_CLASS = "Row-module_row__pwpBq"
    TILE_CLASS = "Tile-module_tile__UWEHN"
    CSS_EMPTY = ".Tile-module_tile__UWEHN[data-state=empty]"
    CSS_ABSENT = ".Tile-module_tile__UWEHN[data-state=absent]"
    CSS_CORRECT = ".Tile-module_tile__UWEHN[data-state=correct]"
    CSS_PRESENT = ".Tile-module_tile__UWEHN[data-state=present]"
    ABSOLUTE_PATH = os.path.dirname(__file__)
    FIVE_LETTER_WORDS_RELATIVE_PATH = "five_letter_words.json"
    FIVE_LETTER_WORDS_ABSOLUTE_PATH = os.path.join(ABSOLUTE_PATH, FIVE_LETTER_WORDS_RELATIVE_PATH)


    def __init__(self, x=None, y=None, height=None, width=None) -> None:
        with open(self.FIVE_LETTER_WORDS_ABSOLUTE_PATH, 'r') as file:
            self.five_letter_words = json.load(file)
        self.potential_words = self.five_letter_words
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
        self.table = self._build_table()
        options = Options()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument('--log-level=3')
        # options.add_argument('--headless')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        self.browser = Chrome(options=options)
        self.action_chains = ActionChains(self.browser)

        if x is not None and y is not None:
            self.browser.set_window_position(x=x, y=y)
        if height is not None and width is not None:
            self.browser.set_window_size(width=width, height=height)

        self.browser.get(self.NYT_WEBSITE)
        play = WebDriverWait(self.browser, 10).until(
        EC.presence_of_element_located((
            By.CLASS_NAME, self.PLAY_BUTTON_CLASS)))
        play.click()
        time.sleep(1)
        self.action_chains.send_keys(Keys.ESCAPE).perform()
        time.sleep(1)

        last_row = self.browser.find_elements(By.CLASS_NAME, self.ROW_CLASS)[5]
        self.action_chains.scroll_to_element(last_row).perform()

    def _build_table(self) -> Table:
        table = Table(title="Wordle")
        table.add_column("Guess", justify="center")
        table.add_column("1")
        table.add_column("2")
        table.add_column("3")
        table.add_column("4")
        table.add_column("5")
        return table

    def _submit_guess(self, guess: str, row_number: int) -> bool:
        for letter in guess:
            self.action_chains.send_keys(letter).perform()
            time.sleep(0.1)
        self.action_chains.send_keys(Keys.ENTER).perform()
        time.sleep(2.5)

        row = self.browser.find_elements(By.CLASS_NAME, self.ROW_CLASS)[row_number - 1]
        tiles = row.find_elements(By.CLASS_NAME, self.TILE_CLASS)
        for letter in tiles:
            letter_check = letter.get_attribute("data-state")
            if letter_check == "tbd":
                return False
        return True

    def _is_letter_duplicate(self, letter, word):
        count = 0
        for l in word:
            if l == letter:
                count += 1
        if count > 1:
            return True
        return False

    def _update_wordle(self, row_number: int, word: str) -> None:
        row = self.browser.find_elements(By.CLASS_NAME, self.ROW_CLASS)[row_number - 1]
        tiles = row.find_elements(By.CLASS_NAME, self.TILE_CLASS)
        for indx, letter in enumerate(tiles, start=1):
            duplicate_check = self._is_letter_duplicate(letter=letter.text.lower(), word=word)
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



    def _update_table(self, row_number: int):
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

    def _check_for_present_letters(self, word):
        if self.wordle['present_letters']:
            for present_letter in self.wordle['present_letters']:
                if present_letter not in word:
                    return False
        return True


    def _get_potential_words(self):
        potential_words = {}
        for word in self.potential_words.keys():
            if self._check_for_present_letters(word) is False:
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


    def _check_for_win(self, check_word: str):
        for indx in range(1, 6):
            if not self.wordle['letters'][indx]['correct']:
                return False
        wordle = str(
            self.wordle['letters'][1]['correct'] +
            self.wordle['letters'][2]['correct'] +
            self.wordle['letters'][3]['correct'] +
            self.wordle['letters'][4]['correct'] +
            self.wordle['letters'][5]['correct'])
        if check_word != wordle:
            return False
        return True


    def _delete_guess(self, guess: str):
        for _ in range(5):
            self.action_chains.send_keys(Keys.BACK_SPACE).perform()
            time.sleep(0.1)
        try:
            self.potential_words.pop(guess)
        except KeyError:
            pass

        try:
            self.five_letter_words.pop(guess)
        except KeyError:
            pass

        with open(self.FIVE_LETTER_WORDS_ABSOLUTE_PATH, 'w') as file:
            file.write(json.dumps(self.five_letter_words, indent=1))

    def _get_best_guess(self, score=5):
        if len(self.potential_words) == 1:
            best_guess = list(self.potential_words.keys())[0]
            return best_guess
        best_guesses = []
        availible_letters = {}
        if not availible_letters:
            for word in self.potential_words.keys():
                for letter in word:
                    availible_letters[letter] = 1

        for indx in range(1, 6):
            try:
                availible_letters.pop(self.wordle["letters"][indx]["correct"])
            except KeyError:
                pass

        if len(availible_letters) == 0:
            best_guess = list(self.potential_words.keys())[0]
            return best_guess

        for word in self.five_letter_words:
            for index, letter in enumerate(word, start=1):
                if self._is_letter_duplicate(letter=letter, word=word) is True:
                    break
                if letter in self.wordle["letters"][index]["incorrect"]:
                    break

                if index == 5:
                    word_score = 0
                    for l in availible_letters.keys():
                        if l in word:
                            word_score += 1
                    if word_score == score:
                        best_guesses.append(word)
        if len(best_guesses) == 0:
            guess = self._get_best_guess(score=score-1)
        else:
            guess = random.choice(best_guesses)
        return guess
    
    def _close_popups(self):
        WebDriverWait(self.browser, 5).until(
        EC.presence_of_element_located((
            By.CLASS_NAME, self.CLOSE_POPUP_CLASS))).click()
        time.sleep(0.5)
        WebDriverWait(self.browser, 5).until(
        EC.presence_of_element_located((
            By.CLASS_NAME, self.CLOSE_POPUP_CLASS))).click()

    def solve(self, first_guess: str="") -> bool:
        with Live(self.table):
            if not first_guess:
                first_guess = random.choice(list(self.potential_words.keys()))
                while self._submit_guess(guess=first_guess, row_number=1) is False:
                    self._delete_guess(first_guess)
                    first_guess = random.choice(list(self.potential_words.keys()))
            elif self._submit_guess(guess=first_guess, row_number=1) is False:
                raise ValueError("You have provided an invalid first guess.")
            self._update_wordle(row_number=1, word=first_guess)
            self._update_table(row_number=1)
            if self._check_for_win(first_guess) is True:
                self._close_popups()
                return True

            for indx in range(2, 7):
                self.potential_words = self._get_potential_words()
                new_guess = self._get_best_guess()
                while self._submit_guess(guess=new_guess, row_number=indx) is False:
                    self._delete_guess(new_guess)
                    new_guess = self._get_best_guess()
                self._update_wordle(row_number=indx, word=new_guess)
                self._update_table(row_number=indx)
                if self._check_for_win(new_guess) is True:
                    self._close_popups()
                    return True

        self._close_popups()
        if self._check_for_win(new_guess) is True:
            return True
        return False
