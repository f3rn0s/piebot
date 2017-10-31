import discord, json
from commander.text.embed import *
import commander.custom as custom

with open("config/perms.json", "r") as permissions:
    perms_conf = json.loads(permissions.read())

admin = perms_conf["admin"]
mod = perms_conf["moderator"]
trusted = perms_conf["trusted"]

ADMIN_PERSMISSIONS = 3
MOD_PERMISSIONS = 2
TRUSTED_PERMISSIONS = 1

async def get_permissions(member):
    perms = []

    for r in member.roles:
        if r.name in admin:
            perms.append(3)
        elif r.name in mod:
            perms.append(2)
        elif r.name in trusted:
            perms.append(1)
        else:
            perms.append(0)

    return max(perms)

async def purge(bot, message, amount):
    await bot.purge_from(message.channel, limit=amount)

async def get_channel(bot, message):
    await bot.send_message(message.channel, "The current channel is: #" + message.channel.name)

async def find_channel(name, message):
    for channel in message.server.channels:
        if channel.name == name: return channel

async def announce(bot, message, args):
    channel = await find_channel("announcements", message)
    await bot.send_message(channel, " ".join(args[1:]))

async def owner(bot, message):
    await bot.send_message(message.channel, "This sever is owned by: " + message.server.owner.name)

async def change_nick(bot, message, args):
    await bot.change_nickname(message.server.me, " ".join(args[1:]))

async def check_permissions(bot, message, level):
    member = message.author
    if level <= await get_permissions(member):
        return True
    else:
        await bot.send_message(message.channel, embed=embed_error("You are not allowed to access this command!"))
        return False

async def help(bot, message):
    commands = ["help", "status", "info", "channel"]
    admin_commands = ["changenick", "purge", "define", "save", "load", "announce"]

    result = "Commands:\n```\n"
    for com in commands:
        result += com + "\n"
    result += "```\n"

    result += "Admin Commands:\n```\n"
    for com in admin_commands:
        result += com + "\n"

    result += "```\nCustom Commands:\n```\n"

    result += custom.get_help()

    result += "```"

    return result

async def handle_command(bot, message, com_arg):
    command = com_arg[0]
    args = com_arg[1]

    channel = message.channel

    if command == "help":
        await bot.send_message(channel, await help(bot, message))
    elif command == "status":
        await bot.send_message(channel, embed=embed_ok("Bot is up and running"))
    elif command == "info":
        await bot.send_message(channel, embed=embed_link("Github", "Pybot's github", "https://github.com/f3rn0s/pybot"))
    elif command == "channel":
        await get_channel(bot, message)
    elif command == "owner":
        await owner(bot, message)
    elif command == "announce":
        if await check_permissions(bot, message, ADMIN_PERSMISSIONS):
            await announce(bot, message, args)
    elif command == "changenick":
        if await check_permissions(bot, message, ADMIN_PERSMISSIONS):
            await change_nick(bot, message, args)
    elif command == "define":
        if await check_permissions(bot, message, ADMIN_PERSMISSIONS):
            custom.define(args)
    elif command == "definelink":
        if await check_permissions(bot, message, ADMIN_PERSMISSIONS):
            custom.define_link(args)
    elif command == "delete":
        if await check_permissions(bot, message, ADMIN_PERSMISSIONS):
            custom.delete(args)
    elif command == "save":
        if await check_permissions(bot, message, ADMIN_PERSMISSIONS):
            await custom.save(bot, message)
    elif command == "load":
        if await check_permissions(bot, message, ADMIN_PERSMISSIONS):
            custom.load()
    elif command == "purge":
        if await check_permissions(bot, message, MOD_PERMISSIONS):
            await purge(bot, message, int(args[1]) + 1)
    else:
        await custom.run_custom(bot, message, command)
