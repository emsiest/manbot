import discord
import os

from discord.ext import commands
from dotenv import load_dotenv

from general_commands import (get_help_embed, get_list_categories_embed, get_list_men_embed, get_stats_embed,
                              get_hello_embed, get_sleep_embed, get_work_embed)
from man_commands import (get_random_embed, get_man)
from manbot_utils import ManbotUtils

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# bot.command will pick up messages starting with 'MANBOT'
bot = commands.Bot(command_prefix="MANBOT ", intents=discord.Intents.all())

@bot.event
# called after bot is logged in 
async def on_ready():
    # set activity status
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.custom, name="custom", state="He is risen!"))
    print('manbot ready!')

'''
Command Stubs
'''
@bot.command(name="CATEGORY")
async def categories_command(ctx):
    await ctx.send(embed=get_list_categories_embed(ctx))

@bot.command(name="CATEGORIES")
async def categories_command(ctx):
    await ctx.send(embed=get_list_categories_embed(ctx))

@bot.command("HELLO")
async def hello_command(ctx):
    await ctx.send(get_hello_embed(ctx))

@bot.command("HELP")
async def help_command(ctx):
    await ctx.send(embed=get_help_embed(ctx))

@bot.command("LIST")
async def my_command(ctx):
    if ctx.message.content.startswith("MANBOT LIST CATEGORIES") or ctx.message.content.startswith("MANBOT LIST CATEGORY"):
        await ctx.send(embed=get_list_categories_embed(ctx))
    if ctx.message.content.startswith("MANBOT LIST MEN"):
        await ctx.send(embed=get_list_men_embed(ctx))
    else:
        await ctx.send("Please use 'MANBOT LIST CATEGORIES' or 'MANBOT LIST MEN'.")

@bot.command("MAN")
async def man_command(ctx):
    await ctx.send(embed=get_list_men_embed(ctx))

@bot.command(name="MEN")
async def men_command(ctx):
    await ctx.send(embed=get_list_men_embed(ctx))

@bot.command("RANDOM")
async def random_command(ctx):
    await ctx.send(embed=get_random_embed(ctx))

@bot.command("SLEEP")
async def sleep_command(ctx):
    await ctx.send(get_sleep_embed(ctx))

@bot.command("STATS")
async def stats_command(ctx):
    await ctx.send(embed=get_stats_embed(ctx))

@bot.command("WORK")
async def work_command(ctx):
    await ctx.send(get_work_embed(ctx))

'''
Message Handling
'''
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        await ctx.send("404 manbot command not found!")

@bot.event
# called for every message received
async def on_message(message):

    # bot cannot trigger itself or be triggered by thirstbot
    if (message.author == bot.user) or (message.author.id == 834302490106789918):
        return

    # check commands here
    await bot.process_commands(message)

    if not message.content.startswith("MANBOT"):
        man_message = get_man(message)
        if man_message:
            await message.channel.send(get_man(message))
            return
        else:
            # check for typos and bonks users if typo detected
            message = ManbotUtils.clean_message(message)
            has_typo = ManbotUtils.check_typo(message)
            if has_typo:
                await message.channel.send(has_typo)
                return

bot.run(TOKEN)
