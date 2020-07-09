import discord
from discord.ext import commands
import random
import os
import pathlib

description = "beepo for the boys"
bot = commands.Bot(command_prefix='beenis ', description=description, case_insensitive=True)

# start up
@bot.event
async def on_ready():
    print("Logged in as {}".format(bot.user.name))

# test command
@bot.command()
async def test(ctx):
    await ctx.send("beeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeepo")

# quote command
@bot.command()
async def quote(ctx):
    channel = bot.get_channel(692654102458400818) # quote channel
    messages = await channel.history().flatten() # messages list
    valid_messages = []

    for message in messages: # remove messages without quotes
        if '\"' in message.content or message.attachments:
            valid_messages.append(message)

    message = random.choice(valid_messages)

    if message.attachments:
        return await ctx.send(message.content + "\n" + message.attachments[0].url)
    else:
        return await ctx.send(message.content)

bot.run('TOKEN')