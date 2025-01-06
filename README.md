# Wordle Bot
This project is my attempt to beat Wordle every day as efficiently as possible. It uses a couple of things to accomplish this:

- Selenium to connect to NYT and interact with the website.
- Github cron job to play Wordle every day and publish the results to a website.
- A JSON word list of all of the valid 5 letter word guesses.

# Running with Docker
```
  docker build -t wordle-bot .
  docker run -it --name wordle-bot wordle-bot
  docker start -ai wordle-bot
```
