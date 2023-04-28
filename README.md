General Purpose Discord Bot ("RaazBot")
====================================

## Description

RaazBot is a Discord integration built in Python using the Discord.py library. [Discord.py](https://discordpy.readthedocs.io/en/stable/) is a Python library designed to streamline integration with the official Discord API.

The integration is capable of enhancing Tabletop experiences by rolling dice, performing search queries online and returning formatted results, as well as other features.

## System Requirements
- [Python 3.9 (latest release recommended)](https://www.python.org/)

## Running
Before starting, create an application and obtain an API key from the [Discord Developer Portal](https://discord.com/developers/applications). Store the key like below in a [.env file](https://medium.com/chingu/an-introduction-to-environment-variables-and-how-to-use-them-f602f66d15fa) (a type of file used to store environmental variables, such as passwords and API keys) in the root of the directory. Make sure to also add the .env file to a .gitignore so as not to publish sensitive data to Github:

```
BOT_TOKEN = <API_KEY_HERE>
```

To run the app locally, first, clone this repository to your local machine.

```bash
git clone https://github.com/Faraaz-Beyabani/discord-bot.git
cd discord-bot
```

Then, in the root directory, open a terminal window and install all necessary packages:

```bash
pip install -r requirements.txt
```

Finally, in the same directory, run the following command to begin a local server to run commands in connected servers:

```bash
python bot.py
```

## License

This project is open source following the MIT License guidelines.
