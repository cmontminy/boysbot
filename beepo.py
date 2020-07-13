import discord
from discord.ext import commands
import random
import pathlib
import sys
import io
import traceback


description = "beepo for the boys"
bot = commands.Bot(command_prefix='beepo ', description=description, 
        case_insensitive=True)
guild_id = 675196476086812683
token = 0
quote_list = []
cached_invite_list = {}


f = open("secrets.txt", "r") # fetch token from secrets file
lines = f.readlines()
for line in lines:
    if "TOKEN" in line:
        line_list = line.split("=")
        token = line_list[1]


# start up
@bot.event
async def on_ready():
    print("Logged in as {}".format(bot.user.name))
    await compile_quotes()
    print("try to cache invites")
    await cache_invites()

    game = discord.Game("skyler is stinky")
    await bot.change_presence(activity = game)


# member join
@bot.event
async def on_member_join(member):
    invite_id_list = await member.guild.invites() # fetch current invite uses
    curr_invite_list = {}
    for invite in invite_id_list:
        curr_invite_list[str(invite.id)] = invite.uses
    message = f"{member.display_name} has joined!"
    for invite in invite_id_list:
        if curr_invite_list[str(invite.id)] != cached_invite_list[str(invite.id)]:
            message += f" Invited from {invite.code} by {invite.inviter}"
            break

    await cache_invites()
    await bot.get_channel(670469511572488229).send(message)


# gets current invites
async def cache_invites():
    print("in cache invites")
    invite_id_list = await bot.get_guild(670469511572488223).invites() 
    print(len(cached_invite_list))
    for invite in invite_id_list:
        cached_invite_list[str(invite.id)] = invite.uses
        print(f"added invite {invite.id}")
    

# gets quotes command
async def compile_quotes():
    channel = bot.get_channel(692654102458400818) # quote channel
    messages = await channel.history().flatten() # messages list

    for message in messages: # remove messages without quotes
        if '\"' in message.content or message.attachments:
            quote_list.append(message)


# test command
@bot.command()
async def test(ctx):
    await ctx.send("beeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeepo")


# help command
@bot.command()
async def helpme(ctx):
    embed = discord.Embed(title="BEEEEEEEEEEEEEPO COMMANDS", description="Command prefix = beepo")
    embed.add_field(name="test", value="Sends beeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeepo", inline=False)
    embed.add_field(name="helpme", value="Generates this message silly", inline=False)
    embed.add_field(name="quote", value="Generates a random quote from the #quotes channel", inline=False)
    embed.add_field(name="advice", value="Ask B E E P O a question and receive an answer", inline=False)
    embed.add_field(name="porn", value="Get some simpy pics from #simp-town", inline=False)
    embed.add_field(name="python", value="Run some stinky pythonic shit", inline=False)
    await ctx.send(embed = embed)


# quote command
@bot.command()
async def quote(ctx):
    message = random.choice(quote_list)
    if message.attachments:
        return await ctx.send(message.content + "\n" + message.attachments[0].url)
    else:
        return await ctx.send(message.content)


# advice command
@bot.command()
async def advice(ctx):
    valid_message = False
    advice = ""
    while not valid_message:
        message = random.choice(quote_list).content
        if message.count('\"') == 2:
            valid_message = True
            start_quote = message.index('\"')
            end_quote = message.index('\"', start_quote + 1)
            advice = message[start_quote + 1:end_quote]
    return await ctx.send(advice)


# porn command
@bot.command()
async def porn(ctx):
    channel = bot.get_channel(726685657812041799) # simp channel
    messages = await channel.history().flatten() # messages list
    valid_message = False
    while not valid_message:
        message = messages[random.randint(0, len(messages) - 1)]
        if message.attachments:
            valid_message = True
            message_url = message.attachments[0].url
    return await ctx.send(message_url)


# python command
@bot.command()
async def py(ctx, *args):
    user_line = " ".join(args)
    print(user_line)
    try:
        result = eval(user_line)
        if result == None:
            result = exec(user_line)
        if result == None:
            old_stdout = sys.stdout
            sys.stdout = buffer = io.StringIO()
            result = exec(user_line)
            sys.stdout = old_stdout
            result = buffer.getvalue()
            buffer.close()
    except Exception as e:
        err = traceback.extract_stack()
        result = ("Oopsie woopsie! You made a fucky wucky. " + 
                    f"Here's your Ewwor >w<\n{e}")
    if result != None:
        return await ctx.send(result)
    else:
        return await ctx.send("Done")

# hug command
@bot.command()
async def hug(ctx, member_id):
    member_id = member_id[3:-1]
    print(member_id)
    member = ctx.message.guild.get_member(int(member_id))
    print(member.nick)
    if member:
        await ctx.send(f"{ctx.message.author.mention} is omega cute and hugged {member.mention}!")
    else:
        await ctx.send("I couldn't find that user D:")


bot.run(token)