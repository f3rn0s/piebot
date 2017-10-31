#!/usr/bin/env python3

import discord, asyncio, json, sys

import commander.commands as commands
import commander.custom as custom

with open("config/settings.json", "r") as configuration:
    settings = json.loads(configuration.read())

prefix = settings["prefix"]

with open("config/token.json", "r") as configuration:
    token = json.loads(configuration.read())

token = token["token"]

#Create bot
bot = discord.Client()

@bot.event
async def on_ready():
    print('Logged in as:')
    print(bot.user.name)
    print(bot.user.id)
    custom.load()

def invalid_channel(message):
    channel_name = message.channel.name
    return channel_name != "bot-testing"

def not_prefixed(message):
    return message.content[0] != prefix

async def valid_command(message):
    if message.author.bot: return False
    if invalid_channel(message): return False
    if not_prefixed(message): return False
    return True

async def get_command(message):
    args = message.content[1:].strip().split(" ")
    command = args[0].lower()
    print("User: " + message.author.name + " on channel " + message.channel.name + " used command " + command)
    return (command, args)

@bot.event
async def on_member_join(member):
    channel = commands.find_channel("hello-world", bot)
    await bot.send_message(channel, "Welcome " + member)

@bot.event
async def on_message(message):
    if not await valid_command(message): return
    await commands.handle_command(bot, message, await get_command(message))

try:
    bot.run(token)
except discord.LoginFailure:
    sys.exit("Invalid token")
except discord.ConnectionClosed as ex:
    sys.exit(ex.text)

