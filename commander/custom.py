from commander.text.embed import *
import json

with open("config/custom-commands.json", "r") as custom_com:
    custom_commands = json.loads(custom_com.read())

def load():
    with open("config/custom-commands.json", "r") as custom_com:
        custom_commands = json.loads(custom_com.read())

def get_help():
    #my_servers_custom = load(server.id())
    result = ""
    for key, value in custom_commands.items():
        result += key + "\n"
    return result

async def run_custom(bot, message, command):
    #my_servers_custom = load(server.id())
    if command in custom_commands:
        command = custom_commands[command]
        print(command)
        if command[1] == True:
            await bot.send_message(message.channel, embed=embed_link(command[2], None, command[0]))
        else:
            await bot.send_message(message.channel, command)

def define(args):
    if len(args) < 3: return
    custom_commands[args[1]] = (" ".join(args[2:]), False)

def define_link(args):
    if len(args) < 3: return
    custom_commands[args[1]] = (args[2], True, " ".join(args[3:]))

def delete(args):
    if args[1] in custom_commands:
        custom_commands.pop(args[1], None)

async def save(bot, message):
    with open("config/custom-commands.json", "w") as custom_com:
        custom_com.write(json.dumps(custom_commands, sort_keys=True, indent=4))
    await bot.send_message(message.channel, embed=embed_ok("Commands saved"))
