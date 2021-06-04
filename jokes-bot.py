import discord
import os

import requests
import json
from replit import db

from keep_alive import keep_alive

client = discord.Client()

def get_dark_joke(): #Get dark humor joke from API
  response = requests.get("https://v2.jokeapi.dev/joke/Dark")
  json_data = json.loads(response.text)
  if json_data['type'] == 'single': #if no set-up
    joke = json_data['joke']
    return joke, ''
  else:
    setup = json_data['setup']
    delivery = json_data['delivery']
    return setup, delivery

def get_chuck_joke(): #Get Chuck Norris joke from API
  response = requests.get("https://api.chucknorris.io/jokes/random")
  json_data = json.loads(response.text)
  joke = json_data['value']
  return joke

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
  
  msg_con = message.content

  if msg_con.startswith('$daddy'):
    quote = get_dad_joke()
    await message.channel.send(quote)
    return
  
  if msg_con.startswith('$chuck'):
    joke = get_chuck_joke()
    await message.channel.send(joke)
    return

  if msg_con.startswith('$dark'):
    setup, delivery = get_dark_joke()
    await message.channel.send(setup, delivery)
    
  if msg_con.startswith('$'): #Commands
    await message.channel.send(
    """Commands:
    $daddy: Dad joke
    $chuck: Chuck Norris joke
    $dark: Dark humor joke""")

#keep_alive()
#client.run(os.getenv('TOKEN'))