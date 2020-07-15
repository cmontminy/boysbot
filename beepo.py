import discord
from discord.ext import commands
import random
import pathlib
import sys
import io
import traceback
import os
import sqlite3

from roles import Roles


description = "beepo for the boys"
bot = commands.Bot(command_prefix='beepo ', description=description, 
        case_insensitive=True)

# token = 0
guild_id = 675196476086812683
quote_list = []
washed_hands = 0

connection = sqlite3.connect("beepo.db")
cursor     = connection.cursor()

bot.add_cog(Roles(bot))

# f = open("secrets.txt", "r") # fetch token from secrets file
# lines = f.readlines()
# for line in lines:
#     if "TOKEN" in line:
#         line_list = line.split("=")
#         token = line_list[1]

# start up
@bot.event
async def on_ready():
    print("Logged in as {}".format(bot.user.name))

    # set bot status
    game = discord.Game("stinky is stinky")
    await bot.change_presence(activity = game)

    # load quotes
    await compile_quotes()

    cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='user_elems' ''')
    if cursor.fetchone()[0] == 0:
        # init database
        cursor.execute(''' CREATE TABLE user_elems (
            name      text,
            user_id   text,
            money     text,
            stinky    text,
            rps_wins  text,
            rps_plays text
        )''')
        connection.commit()

        member_list = bot.get_guild(guild_id).members
        for member in member_list:
            data_string = str((member.name,member.id,0,0,0,0))
            print(data_string)
            entry_string = f"INSERT INTO user_elems VALUES {data_string}"
            cursor.execute(entry_string)
        connection.commit()

    # load roles
    # cache_roles()
    

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
    global washed_hands
    member_id = member_id[3:-1]
    print(member_id)
    member = ctx.message.guild.get_member(int(member_id))
    check_id = ctx.message.author.id
    print(member.nick)
    print(washed_hands)
    if member:
        if (check_id == 145869054136156160) :
            if (not washed_hands) :
                await ctx.send(f"OH NOOOOOOOOOO {ctx.message.author.mention} HAS LATHERED {member.mention} WITH HIS CUM VAPORS!!!!")
            else :
                washed_hands = 0
                await ctx.send(f"{ctx.message.author.mention} is omega cute and hugged {member.mention}!")
        else :
            if (member.id == 145869054136156160) and not (washed_hands) :
                await ctx.send(f"{ctx.message.author.mention} is omega cute and hugged {member.mention}!")
            else :
                await ctx.send(f"{ctx.message.author.mention} is omega cute and hugged {member.mention}!")
    else:
        await ctx.send("I couldn't find that user D:")


# washhands command
@bot.command()
async def washhands(ctx):
    global washed_hands
    member_id = ctx.message.author.id
    if (member_id == 145869054136156160) :
        washed_hands = 1
        await ctx.send(f"the cum vapors have been washed off of {ctx.message.author.mention}... for now...")
    else :
        await ctx.send(f"{ctx.message.author.mention} has washed their hands! yay!")


# rock papers scissors command
@bot.command()
async def rps(ctx, user_guess = None):
    message = ""
    options = ["scissors", "paper", "rock"]
    outcome = False

    if user_guess is not None and user_guess in options:
        user_num = options.index(user_guess)
        bot_num  = random.randint(0, 2)
        diff     = user_num - bot_num

        if diff == 0: # tie
            message = f"You both guessed {user_guess}, so it's a tie!"
        elif diff == 1 or diff == -2:
            message = f"Beepo picked {options[bot_num]}, so you win!"
            outcome = True
        else:
            message = f"Beepo picked {options[bot_num]}, so you lose!"
            
    else:
        message = "This is rock paper scissors you dumb shit, pick one of those."
    
    rps_log(ctx.author.id, outcome)
    await ctx.send(message)


# rps log
def rps_log(user_id, outcome):
    if outcome:
        cursor.execute(f"SELECT rps_wins FROM user_elems WHERE user_id={user_id}")
        curr_wins = int(cursor.fetchone()[0])
        curr_wins += 1
        cursor.execute(f"UPDATE user_elems SET rps_wins = {curr_wins} WHERE user_id = {user_id}")
    else: # beepo won
        cursor.execute(f"SELECT rps_wins FROM user_elems WHERE user_id={bot.user.id}")
        curr_wins = int(cursor.fetchone()[0])
        curr_wins += 1
        cursor.execute(f"UPDATE user_elems SET rps_wins = {curr_wins} WHERE user_id = {bot.user.id}")
    # update players total plays
    cursor.execute(f"SELECT rps_plays FROM user_elems WHERE user_id={user_id}")
    curr_plays = int(cursor.fetchone()[0])
    curr_plays += 1
    cursor.execute(f"UPDATE user_elems SET rps_plays = {curr_plays} WHERE user_id = {user_id}")

    # update beepos total plays
    cursor.execute(f"SELECT rps_plays FROM user_elems WHERE user_id={bot.user.id}")
    curr_plays = int(cursor.fetchone()[0])
    curr_plays += 1
    cursor.execute(f"UPDATE user_elems SET rps_plays = {curr_plays} WHERE user_id = {bot.user.id}")
    
    connection.commit()

bot.run(os.environ.get('BOT_TOKEN'))
# bot.run(token)