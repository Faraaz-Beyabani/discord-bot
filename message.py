import requests
import json
import os
# from dotenv import load_dotenv

if __name__ == "__main__":
    # load_dotenv()

    channelID = "610914973853679648"
    botToken = 'NjgwOTA5Njc3NjM0MTI1ODI2.XlGx8A.iBzAHGwdH6VjljE8w7A8saJBQDA'

    baseURL = "https://discordapp.com/api/channels/{}/messages".format(channelID)
    headers = { "Authorization":"Bot {}".format(botToken),
                "User-Agent":"myBotThing (http://some.url, v0.1)",
                "Content-Type":"application/json", }

    while True:
        message = input()
        POSTedJSON =  json.dumps ( {"content":message} )
        r = requests.post(baseURL, headers = headers, data = POSTedJSON)