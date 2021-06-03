import discord
from discord.ext import commands
import os

import requests
import json

client = discord.Client()

def get_inspirational_quote(): #getting motivational quotes from an API
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return quote

def get_dad_joke(): #Get dad joke from API
  header = {'Accept' : 'application/json'}
  response = requests.get("https://icanhazdadjoke.com/", headers = header)
  json_data = json.loads(response.text)
  joke = json_data['joke']
  return joke

@client.event #login message a
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

  if message.content.startswith('$'): #Commands
    await message.channel.send(
    """Commands:
    $inspire: Inspirational message
    $daddy: Dad joke""")

client.run(os.getenv('TOKEN'))