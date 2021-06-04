import discord
import os

import requests
import json
import random
from replit import db

client = discord.Client()

sad_words = ["sad", "depressed", "unhappy", "angry", "miserable", "depressing"]

starter_encouragements = [
  "Cheer up!",
  "Hang in there!",
  "You don't suck!",
  "You are a greap person / bot!"
]

if "responding" not in db.keys():
  db["responding"] = True

def get_inspirational_quote(): #getting motivational quotes from an API
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return quote

def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_message]

def delete_encouragement(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
    db["encouragements"] = encouragements

def get_dad_joke(): #Get dad joke from API
  header = {'Accept' : 'application/json'}
  response = requests.get("https://icanhazdadjoke.com/", headers = header)
  json_data = json.loads(response.text)
  joke = json_data['joke']
  return joke

@client.event #login message
async def on_ready():
  print('We have logged in as {0}'.format(client.user))

@client.event #respond to a message
async def on_message(message):
  if message.author == client.user:
    return
  
  if message.content.startswith('$daddy'):
    quote = get_dad_joke()
    await message.channel.send(quote)
    return

  if message.content.startswith('$inspire'): #inspirational quote
    quote = get_inspirational_quote()
    await message.channel.send(quote)
    return

  if db["responding"]:
    options = starter_encouragements #encouragement options
    if "encouragements" in db.keys():
      options = options.extend(db["encouragements"])

    if any(work in message.content for work in sad_words): #if sad word found, send encouraging message
      await message.channel.send(random.choice(options))
      return

  if message.content.startswith("$new"): #add encouraging message
    encouraging_message = message.content.split("$new ",1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New encouraging message added!")
    return

  if message.content.startswith("$del"): #delete encouraging message
    encouragements = []
    if "encouragements" in db.keys():
      index = int(message.content.split("$del",1)[1])
      delete_encouragement(index)
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)
    return

  if message.content.startswith("$lists"):
    encouragements = []
    if "encouragements" in db.keys():
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)
    return
  
  if message.content.startswith("$responding"): #set if bot can respond to messages
    value = message.content.split("$responding ", 1)[1]
    if value.lower() == 'true':
      db["responding"] = True
      await message.channel.send("Responding is on.")
    else:
      db["responding"] = False
      await message.channel.send("Responding is off.")
      return

  if message.content.startswith('$'): #Commands
    await message.channel.send(
    """Commands:
    $inspire: Inspirational message
    $daddy: Dad joke""")

client.run(os.getenv('TOKEN'))