import time
import json
import random
import os

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
        self.potential_words = []
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
        options = Options()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument('--log-level=3')
        #options.add_argument('--headless')
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


    def submit_guess(self, guess: str, row_number: int) -> bool:
        for letter in guess:
            self.action_chains.send_keys(letter).perform()
            time.sleep(0.1)
        self.action_chains.send_keys(Keys.ENTER).perform()
        time.sleep(3)

        row = self.browser.find_elements(By.CLASS_NAME, self.ROW_CLASS)[row_number - 1]
        empty = row.find_elements(By.CSS_SELECTOR, self.CSS_EMPTY)
        if len(empty) == 0:
            return True
        return False

    def update_wordle(self, row_number: int) -> None:
        row = self.browser.find_elements(By.CLASS_NAME, self.ROW_CLASS)[row_number - 1]
        tiles = row.find_elements(By.CLASS_NAME, self.TILE_CLASS)
        for indx, letter in enumerate(tiles, start=1):
            letter_check = letter.get_dom_attribute("data-state")
            if letter_check == "absent":
                self.wordle["absent_letters"].append(letter.text.lower())
            elif letter_check == "correct":
                self.wordle["letters"][indx]["correct"] = letter.text.lower()
            elif letter_check == "present":
                self.wordle["present_letters"].append(letter.text.lower())
                self.wordle["letters"][indx]["incorrect"].append(letter.text.lower())

    def get_potential_words(self):
        potential_words = {}
        for word in self.FIVE_LETTER_WORDS.keys():
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
                    if self.wordle['present_letters']:
                        for i, present_letter in enumerate(self.wordle['present_letters'], start=1):
                            if present_letter not in word:
                                break
                            if len(self.wordle['present_letters']) == i:
                                potential_words[word] = 1
                    else:
                        potential_words[word] = 1
        return potential_words

    def check_for_win(self):
        for indx in range(1, 6):
            if self.wordle['letters'][indx]['correct']:
                pass
            else:
                return False
        return True