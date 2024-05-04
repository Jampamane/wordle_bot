# Import Modules
import json
import os
from selenium.webdriver import Chrome

class ChromeCookies(Chrome):
    """
    Custom class running off of Chrome Webdriver.
    Added the functionality to save and load cookies to make it easier to restore sessions.

    Args:
        Chrome (selenium.webdriver.Chrome):
            Chrome webdriver that inherits all of the functionality
            for the regular webdriver.
    """

    def save_cookies(self):
        """Get and store cookies after login and store cookies in a file."""
        cookies = self.get_cookies()

        with open('cookies.json', 'w') as file:
            json.dump(cookies, file)
        print('New Cookies saved successfully')


    def load_cookies(self):
        """
        Check if cookies file exists, load cookies to a vaiable from a file,
        set stored cookies to maintain the session, refresh Browser after login.
        """
        if 'cookies.json' in os.listdir():

            with open('cookies.json', 'r') as file:
                cookies = json.load(file)

            for cookie in cookies:
                self.add_cookie(cookie)
        else:
            print('No cookies file found')

        self.refresh()
