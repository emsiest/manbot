import discord
import os

from discord.ext import commands
from dotenv import load_dotenv

from general_commands import (get_help_embed, get_list_categories_embed, get_list_men_embed, get_stats_embed,
                              get_hello_embed, get_sleep_embed, get_work_embed)
from man_commands import (get_random_embed, get_man)
from user_commands import (get_disable_embed, get_enable_embed, get_my_categories_embed, get_my_men_embed, get_reset_embed)
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
@bot.command(name="DISABLE")
async def disable_command(ctx):
    await ctx.send(embed=get_disable_embed(ctx))

@bot.command(name="ENABLE")
async def enable_command(ctx):
    await ctx.send(embed=get_enable_embed(ctx))

@bot.command("HELLO")
async def hello_command(ctx):
    await ctx.send(get_hello_embed(ctx))

@bot.command("HELP")
async def help_command(ctx):
    await ctx.send(embed=get_help_embed(ctx))

@bot.command("LIST")
async def my_command(ctx):
    if ctx.message.content.startswith("MANBOT LIST CATEGORIES"):
        await ctx.send(embed=get_list_categories_embed(ctx))
    if ctx.message.content.startswith("MANBOT LIST MEN"):
        await ctx.send(embed=get_list_men_embed(ctx))

@bot.command("MAN")
async def man_command(ctx):
    await ctx.send("Hey " + ctx.message.author.mention + " the correct command is MANBOT MEN <CATEGORY NAME>, e.g. MANBOT MEN ANIME.")

@bot.command("MY")
async def my_command(ctx):
    if "MANBOT MY CATEGORIES" == ctx.message.content:
        await ctx.send(embed=get_my_categories_embed(ctx))
    if "MANBOT MY MEN" == ctx.message.content:
        await ctx.send(embed=get_my_men_embed(ctx))

@bot.command("RANDOM")
async def random_command(ctx):
    await ctx.send(embed=get_random_embed(ctx))

@bot.command("RESET")
async def reset_command(ctx):
    await ctx.send(embed=get_reset_embed(ctx))

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

    # check for typos and bonks users if typo detected
    ManbotUtils.clean_message(message)
    has_typo = ManbotUtils.check_typo(message)
    if has_typo:
        await message.channel.send(has_typo)
        return

    # check commands here
    await bot.process_commands(message)

    if not message.content.startswith("MANBOT"):
        man_message = get_man(message)
        if man_message:
            await message.channel.send(get_man(message))
        return

bot.run(TOKEN)
