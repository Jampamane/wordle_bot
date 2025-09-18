"""Wordle Module, connects to and plays Wordle"""

import time
import json
import random
import os
import requests

from rich.live import Live
from rich.table import Table
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import SessionNotCreatedException


class Wordle:
    """
    Handles all the logic for connecting to NYT website and playing Wordle.

    Raises:
        ValueError:
            Will raise a value error if you provide an
            invalid first guess when using Wordle.solve().

    Args:
        headless (bool, optional):
            Will run the selenium browser in headless mode.
            You will still be able to see what is going on since
            it will build a dynamic table in the console.
            Defaults to False.
    """

    NYT_WEBSITE = "https://www.nytimes.com/games/wordle/index.html"
    PLAY_BUTTON_CLASS = "Welcome-module_button__ZG0Zh"
    CLOSE_POPUP_CLASS = "Modal-module_closeIconButton__y9b6c"
    ROW_CLASS = "Row-module_row__pwpBq"
    TILE_CLASS = "Tile-module_tile__UWEHN"
    CSS_EMPTY = ".Tile-module_tile__UWEHN[data-state=empty]"
    CSS_ABSENT = ".Tile-module_tile__UWEHN[data-state=absent]"
    CSS_CORRECT = ".Tile-module_tile__UWEHN[data-state=correct]"
    CSS_PRESENT = ".Tile-module_tile__UWEHN[data-state=present]"
    FIVE_LETTER_WORDS_ABSOLUTE_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)),
        "five_letter_words.json",
    )

    def __init__(self, headless: bool = False) -> None:
        self.console = Console()
        with self.console.status("Setting up Wordle..."):
            try:
                response = requests.get("https://raw.githubusercontent.com/Jampamane/wordle_bot/refs/heads/main/five_letter_words.json")
                response.raise_for_status()
                self.five_letter_words = response.json()
            except requests.RequestException as e:
                print("Error fetching data:", e)
            except ValueError as e:
                print("Error decoding JSON:", e)

            self.potential_words = self.five_letter_words
            self.potential_letters = [
                "a",
                "b",
                "c",
                "d",
                "e",
                "f",
                "g",
                "h",
                "i",
                "j",
                "k",
                "l",
                "m",
                "n",
                "o",
                "p",
                "q",
                "r",
                "s",
                "t",
                "u",
                "v",
                "w",
                "x",
                "y",
                "z",
            ]
            self.style_dict = {
                "absent": "grey53",
                "present": "yellow bold",
                "correct": "green bold",
                "tbd": "red",
            }
            self.wordle = {
                "letters": {
                    1: {"correct": "", "incorrect": []},
                    2: {"correct": "", "incorrect": []},
                    3: {"correct": "", "incorrect": []},
                    4: {"correct": "", "incorrect": []},
                    5: {"correct": "", "incorrect": []},
                },
                "absent_letters": [],
                "present_letters": [],
                "guess": {
                    1: {"word": "", "letters": []},
                    2: {"word": "", "letters": []},
                    3: {"word": "", "letters": []},
                    4: {"word": "", "letters": []},
                    5: {"word": "", "letters": []},
                    6: {"word": "", "letters": []},
                },
            }
            options = Options()
            options.add_experimental_option("excludeSwitches", ["enable-logging"])
            options.add_argument("--log-level=3")
            options.add_argument("--no-sandbox")  # Bypass OS security model
            options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource issues
            options.add_argument("--disable-gpu")  # Applicable for Windows/Linux GUI environments
            options.add_argument("--remote-debugging-port=9222")  # Debugging port for ChromeDriver
            options.add_argument("--disable-software-rasterizer")  # Avoid GPU rendering issues
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-logging")
            options.add_argument("--disable-popup-blocking")
            if headless is True:
                options.add_argument("--headless")
            options.add_argument("--ignore-certificate-errors")
            options.add_argument("--ignore-ssl-errors")

            try:
                self.browser = Chrome(options=options)
            except SessionNotCreatedException as e:
                self.console.print("Selenium web browser failed to start!", style="red")
                self.console.print("You might be missing some dependencies.", style="red")
                self.console.print("Selenium error: SessionNotCreatedException", style="yellow")
                exit(3)

            self.action_chains = ActionChains(self.browser)

            self.browser.get(self.NYT_WEBSITE)

            # ----------------------------------------------------------------------------------
            # NEW YORK TIMES "WE'VE UPDATED OUR TERMS OF SERVICE" BUTTON
            try:
                WebDriverWait(self.browser, 10).until(
                    EC.presence_of_element_located(
                        (By.CLASS_NAME, "purr-blocker-card__button")
                    )
                )
                self.browser.find_element(
                    By.CLASS_NAME, "purr-blocker-card__button"
                ).click()
            except TimeoutException:
                pass
            # -----------------------------------------------------------------------------------

            WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, self.PLAY_BUTTON_CLASS))
            )
            play = self.browser.find_elements(By.CLASS_NAME, self.PLAY_BUTTON_CLASS)[-1]
            play.click()
            time.sleep(1)
            self.action_chains.send_keys(Keys.ESCAPE).perform()
            time.sleep(1)

            last_row = self.browser.find_elements(By.CLASS_NAME, self.ROW_CLASS)[5]
            self.action_chains.scroll_to_element(last_row).perform()

    @property
    def wordle_today(self) -> str:
        """
        Grabs today's wordle from the Wordle Class's wordle dictionary.
        Only works if wordle has been solved.

        Returns:
            str: Today's wordle.
        """
        return str(
            self.wordle["letters"][1]["correct"]
            + self.wordle["letters"][2]["correct"]
            + self.wordle["letters"][3]["correct"]
            + self.wordle["letters"][4]["correct"]
            + self.wordle["letters"][5]["correct"]
        )

    def build_layout(self, guess="", style="yellow") -> Layout:
        """
        Dynamically build the layout in the console so
        the user can see how the wordle is being solved.

        Args:
            guess (str, optional):
                The 5 letter word that is being guessed. Defaults to "".
            style (str, optional):
                The color that the guess will be displayed as. Defaults to "yellow".

        Returns:
            Layout: Layout object for displaying wordle.
        """

        print_guess = False
        table = Table(title="Wordle", show_header=False)
        table.add_column("Guess", width=5, justify="center")
        table.add_column("1", width=1, justify="center")
        table.add_column("2", width=1, justify="center")
        table.add_column("3", width=1, justify="center")
        table.add_column("4", width=1, justify="center")
        table.add_column("5", width=1, justify="center")
        for x in range(1, 7):
            if self.wordle["guess"][x]["letters"]:
                table.add_row(
                    self.wordle["guess"][x]["word"].capitalize(),
                    f"[{self.wordle['guess'][x]['letters'][0][1]}]{self.wordle['guess'][x]['letters'][0][0]}",
                    f"[{self.wordle['guess'][x]['letters'][1][1]}]{self.wordle['guess'][x]['letters'][1][0]}",
                    f"[{self.wordle['guess'][x]['letters'][2][1]}]{self.wordle['guess'][x]['letters'][2][0]}",
                    f"[{self.wordle['guess'][x]['letters'][3][1]}]{self.wordle['guess'][x]['letters'][3][0]}",
                    f"[{self.wordle['guess'][x]['letters'][4][1]}]{self.wordle['guess'][x]['letters'][4][0]}",
                )
                table.add_section()
            elif not guess:
                table.add_row(str(x), style="cyan")
                table.add_section()
            elif print_guess is False:
                print_guess = True
                table.add_row(guess.capitalize(), style=style)
                table.add_section()
            else:
                table.add_row(str(x), style="cyan")
                table.add_section()

        letters = Table(show_header=False, show_lines=False, show_edge=False)
        letters.add_row(
            f"Total potential words: [cyan bold]{len(self.potential_words.keys())}"
        )
        words = Table(show_header=False, show_lines=False, show_edge=False)
        words.add_row(str(self.potential_letters))
        words.add_section()
        words.add_row(str(list(self.potential_words.keys())))

        layout = Layout()
        layout.split_row(Layout(name="table"), Layout(name="info"))
        layout["info"].split_column(Layout(name="letters"), Layout(name="words"))
        layout["table"].size = 33
        layout["letters"].size = 3
        layout["table"].update(Panel(table))
        layout["letters"].update(Panel(letters))
        layout["words"].update(Panel(words))
        return layout

    def _submit_guess(self, guess: str, row_number: int) -> bool:
        """Submits the guess to NYT Wordle.

        Args:
            guess (str):
                Guess to submit.
            row_number (int):
                Row number the guess is being submitted to.
                Used for validating if the guess was successful or not.

        Returns:
            bool: True or False based on if guess was successfully submitted.
        """
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

    def _is_letter_duplicate(self, letter: str, word: str) -> bool:
        """Checks if a given letter shows up more than once in a word.

        Args:
            letter (str): Letter to check for duplicate.
            word (str): Word to check letter duplicate.

        Returns:
            bool: True if duplicate, False if otherwise.
        """
        count = 0
        for word_letter in word:
            if word_letter == letter:
                count += 1
        if count > 1:
            return True
        return False

    def _totally_absent(self, row_number: int, letter: str) -> bool:
        row = self.browser.find_elements(By.CLASS_NAME, self.ROW_CLASS)[row_number - 1]
        tiles = row.find_elements(By.CLASS_NAME, self.TILE_CLASS)
        for tile_letter in tiles:
            if tile_letter.text.lower() == letter:
                if tile_letter.get_attribute("data-state") != "absent":
                    return False
        return True

    def _update_wordle(self, row_number: int, word: str) -> None:
        self.wordle["guess"][row_number]["word"] = word
        row = self.browser.find_elements(By.CLASS_NAME, self.ROW_CLASS)[row_number - 1]
        tiles = row.find_elements(By.CLASS_NAME, self.TILE_CLASS)
        for indx, letter in enumerate(tiles, start=1):
            letter_check = letter.get_attribute("data-state")
            if letter_check == "absent":
                if (
                    self._is_letter_duplicate(letter=letter.text.lower(), word=word)
                    is True
                ):
                    if (
                        self._totally_absent(
                            row_number=row_number, letter=letter.text.lower()
                        )
                        is False
                    ):
                        self.wordle["letters"][indx]["incorrect"].append(
                            letter.text.lower()
                        )
                    else:
                        self.wordle["absent_letters"].append(letter.text.lower())
                else:
                    self.wordle["absent_letters"].append(letter.text.lower())
            elif letter_check == "correct":
                self.wordle["letters"][indx]["correct"] = letter.text.lower()
                self.wordle["present_letters"].append(letter.text.lower())
            elif letter_check == "present":
                self.wordle["present_letters"].append(letter.text.lower())
                self.wordle["letters"][indx]["incorrect"].append(letter.text.lower())

            self.wordle["guess"][row_number]["letters"].append(
                (letter.text, self.style_dict[letter_check])
            )

    def _check_for_present_letters(self, word):
        if self.wordle["present_letters"]:
            for present_letter in self.wordle["present_letters"]:
                if present_letter not in word:
                    return False
        return True

    def _get_potential_words(self):
        potential_words = {}
        for word in self.potential_words.keys():
            if self._check_for_present_letters(word) is False:
                continue

            for indx, letter in enumerate(word, start=1):
                if letter in self.wordle["absent_letters"]:
                    break
                if letter in self.wordle["letters"][indx]["incorrect"]:
                    break

                if not self.wordle["letters"][indx]["correct"]:
                    pass
                elif letter != self.wordle["letters"][indx]["correct"]:
                    break

                if indx == 5:
                    potential_words[word] = 1
        return potential_words

    def _check_for_win(self, check_word: str):
        for indx in range(1, 6):
            if not self.wordle["letters"][indx]["correct"]:
                return False
        if check_word != self.wordle_today:
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

        with open(self.FIVE_LETTER_WORDS_ABSOLUTE_PATH, "w", encoding="utf-8") as file:
            file.write(json.dumps(self.five_letter_words, indent=1))

    def _get_available_letters(self) -> dict:
        availible_letters = {}
        for word in self.potential_words.keys():
            for letter in word:
                availible_letters[letter] = 1

        for indx in range(1, 6):
            try:
                availible_letters.pop(self.wordle["letters"][indx]["correct"])
            except KeyError:
                pass
        self.potential_letters = list(availible_letters.keys())
        return availible_letters

    def _get_best_guess(self, score: int = 5) -> str:
        """
        Generates a list of best guesses based on the remaining
        letters from the list of potential remaining words.

        Args:
            score (int, optional):
                Defaults to 5. Used in recusion. If function can't find a word that
                includes 5 unique letters from the list of potential letters
                then it will call the function again with a score of -= 1.

        Returns:
            guess (str):
                Random guess for the list of potential guesses.
        """
        best_guesses = []
        availible_letters = self._get_available_letters()

        if len(self.potential_words) == 1 or len(availible_letters) == 0:
            best_guess = list(self.potential_words.keys())[0]
            return best_guess

        if len(self.potential_words) == 2:
            best_guess = random.choice(list(self.potential_words.keys()))
            return best_guess

        for word in self.five_letter_words:
            for index, letter in enumerate(word, start=1):
                if self._is_letter_duplicate(letter=letter, word=word) is True:
                    break
                if letter in self.wordle["letters"][index]["incorrect"]:
                    break

                if index == 5:
                    word_score = 0
                    for availible_letter in availible_letters:
                        if availible_letter in word:
                            word_score += 1
                    if word_score == score:
                        best_guesses.append(word)
        if len(best_guesses) == 0:
            guess = self._get_best_guess(score=score - 1)
        else:
            guess = random.choice(best_guesses)
        return guess

    def _close_popups(self) -> None:
        """Closes the popups when done solving the Wordle."""
        WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, self.CLOSE_POPUP_CLASS))
        ).click()
        time.sleep(0.5)
        WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, self.CLOSE_POPUP_CLASS))
        ).click()

    def solve(self, first_guess: str = "") -> bool:
        """Solve the wordle by selecting random 'best guesses'.

        Args:
            first_guess (str, optional):
                The first guess the wordle solver will use.
                If blank, will just pick a random word. Defaults to "".

        Raises:
            ValueError:
                Will raise a ValueError if provided an invalid first guess.

        Returns:
            bool: True if successfully solved, False if otherwise.
        """
        with Live(self.build_layout()) as live:
            if first_guess:
                live.update(self.build_layout(guess=first_guess))
            if not first_guess:
                first_guess = random.choice(list(self.potential_words.keys()))
                live.update(self.build_layout(guess=first_guess))
                while self._submit_guess(guess=first_guess, row_number=1) is False:
                    live.update(self.build_layout(guess=first_guess, style="red bold"))
                    self._delete_guess(first_guess)
                    first_guess = random.choice(list(self.potential_words.keys()))
                    live.update(self.build_layout(guess=first_guess))
            elif self._submit_guess(guess=first_guess, row_number=1) is False:
                raise ValueError("You have provided an invalid first guess.")
            self._update_wordle(row_number=1, word=first_guess)
            live.update(self.build_layout())
            if self._check_for_win(first_guess) is True:
                self._close_popups()
                return True

            for indx in range(2, 7):
                self.potential_words = self._get_potential_words()
                new_guess = self._get_best_guess()
                live.update(self.build_layout(guess=new_guess))
                while self._submit_guess(guess=new_guess, row_number=indx) is False:
                    live.update(self.build_layout(guess=new_guess, style="red bold"))
                    self._delete_guess(new_guess)
                    new_guess = self._get_best_guess()
                    live.update(self.build_layout(guess=new_guess))
                self._update_wordle(row_number=indx, word=new_guess)
                live.update(self.build_layout())
                if self._check_for_win(new_guess) is True:
                    break

        self._close_popups()
        if self._check_for_win(new_guess) is True:
            self.console.print(
                f"Today's wordle is: [green bold]{self.wordle_today.upper()}",
                justify="center",
            )
            return True
        self.console.print(
            "Looks like the bot failed wordle today...", justify="center"
        )
        return False
