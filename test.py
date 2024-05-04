import requests
from bs4 import BeautifulSoup
from rich.console import Console

NYT_WORDLE = "https://www.nytimes.com/games/wordle/index.html"

response = requests.get(NYT_WORDLE)
soup = BeautifulSoup(response.content, "html.parser")
console = Console()

console.print(soup.prettify())