import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

channelID = "688401132304990231"
botToken = os.environ['BOT_TOKEN']

baseURL = "https://discordapp.com/api/channels/{}/messages".format(channelID)
headers = { "Authorization":"Bot {}".format(botToken),
            "User-Agent":"myBotThing (http://some.url, v0.1)",
            "Content-Type":"application/json", }

while True:
    message = input()
    POSTedJSON =  json.dumps ( {"content":message} )
    r = requests.post(baseURL, headers = headers, data = POSTedJSON)