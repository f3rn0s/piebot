import discord

def embed_ok(text):
    return discord.Embed(color=discord.Color.green(), description=text)

def embed_error(text):
    return discord.Embed(color=discord.Color.red(), description=text)

def embed_link(website_name, website_description, url):
    return discord.Embed(title=website_name, color=discord.Color.blue(), description=website_description, url=url)
