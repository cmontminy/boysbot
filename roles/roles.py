import discord
from discord.ext import commands
import sqlite3

default_channel_id = 0
cache_roles = []

class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    # # MESSAGE_ID:EMOJI=ROLE_ID,EMOJI=ROLE_ID...
    # def cache_roles():
    #     f = open("roles.txt", "r")
    #     lines = f.readlines()
    #     for line in lines:
    #         line_list = line.split(":")
    #         cached_roles.append(line_list)


    # set channel command
    @commands.command()
    async def setchannel(self, ctx):
        global default_channel_id
        default_channel_id = ctx.message.channel.id
        await ctx.send(f"{self.bot.get_channel(default_channel_id).mention} has been set as the default channel" 
                         + " for role reactions! [LOCAL]")


    # get channel command
    @commands.command()
    async def getchannel(self, ctx):
        global default_channel_id
        await ctx.send(f"The default channel is {self.bot.get_channel(default_channel_id).mention}.")


    # send role message function
    

    # select role message function


    # add role function

    
    # remove role function

    
    # assign / remove role on react


    # # hug command
    # @commands.command()
    # async def hug(self, ctx, member_id):
    #     member_id = member_id[3:-1]
    #     member = ctx.message.guild.get_member(int(member_id))
    #     if member:
    #         await ctx.send(f"{ctx.message.author.mention} is omega cute and " +
    #                         "hugged {member.mention}!")
    #     else:
    #         await ctx.send("I couldn't find that user D:")