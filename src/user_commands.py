import discord

from manbot_utils import ManbotUtils

'''
Implementations for user settings commands: DISABLE, ENABLE, MY CATEGORIES, MY MEN, RESET.
'''

utils = ManbotUtils()
all_categories = utils.all_categories
all_men = utils.all_men
purple = utils.purple

# disable a category or man for a user
def get_disable_embed(ctx):
    author = ctx.message.author.id
    mention = ctx.message.author.mention
    category = utils.get_category(ctx.message.content, " DISABLE ")
    man = utils.get_man(ctx.message.content, " DISABLE ")

    embed = discord.Embed(title="HEY",
                          description=mention + " Please supply a valid man or category name to disable, e.g. MANBOT DISABLE KPOP.",
                          color=purple)
    # if message contains valid category name
    if category:
        for c in all_categories:
            if category == c:
                # add author to disabled list if not present
                if author not in all_categories[c][0]["disabled"]:
                    all_categories[c][0]["disabled"].append(author)
                    ManbotUtils.update_file('resources/categories.json', all_categories)
                    embed = discord.Embed(title="WOOHOO",
                                          description=mention + " Successfully disabled " + category + ".",
                                          color=purple)
                else:
                    embed = discord.Embed(title="HOLD UP",
                                          description=mention + " You've already disabled " + category + " you silly goose.",
                                          color=purple)
    # if message contains valid man name
    elif man:
        for m in all_men:
            if man == m:
                # add author to disabled list if not present
                if author not in all_men[m][0]["disabled"]:
                    all_men[m][0]["disabled"].append(author)
                    ManbotUtils.update_file('resources/men.json', all_men)
                    embed = discord.Embed(title="WOOHOO", description=mention + " Successfully disabled " + man + ".", color=purple)
                else:
                    embed = discord.Embed(title="HOLD UP", description=mention + " You've already disabled " + man + " you silly goose.", color=purple)
    return embed

# enable a category or man for a user
def get_enable_embed(ctx):
    author = ctx.message.author.id
    mention = ctx.message.author.mention
    category = utils.get_category(ctx.message.content, " ENABLE ")
    man = utils.get_man(ctx.message.content, " ENABLE ")

    embed = discord.Embed(title="HEY",
                          description=mention + " Please supply a valid man or category name to enable, e.g. MANBOT ENABLE KPOP.",
                          color=purple)
    # if message contains valid category name
    if category:
        for c in all_categories:
            if category == c:
                # remove author from disabled list if present
                if author in all_categories[c][0]["disabled"]:
                    all_categories[c][0]["disabled"].remove(author)
                    ManbotUtils.update_file('resources/categories.json', all_categories)
                    embed = discord.Embed(title="WOOHOO",
                                          description=mention + " Successfully enabled " + category + ".",
                                          color=purple)
                else:
                    embed = discord.Embed(title="HOLD UP",
                                          description=mention + " You've already enabled " + category + " you silly goose.",
                                          color=purple)
    # if message contains valid man name
    elif man:
        for m in all_men:
            if man == m:
                # remove author from disabled list if present
                if author in all_men[m][0]["disabled"]:
                    all_men[m][0]["disabled"].remove(author)
                    ManbotUtils.update_file('resources/men.json', all_men)
                    embed = discord.Embed(title="WOOHOO",
                                          description=mention + " Successfully enabled " + man + ".",
                                          color=purple)
                else:
                    embed = discord.Embed(title="HOLD UP",
                                          description=mention + " You've already enabled " + man + " you silly goose.",
                                          color=purple)
    return embed

# return list of categories enabled/disabled for a user
def get_my_categories_embed(ctx):
    author = ctx.message.author.id
    mention = ctx.message.author.mention

    embed = discord.Embed(title="MANBOT MY CATEGORIES", description=mention + " Here are your categories:", color=purple)
    for c in all_categories:
        disabled = False
        if author in all_categories[c][0]["disabled"]:
            disabled = True
        if disabled:
            embed.add_field(name="", value=c + " :no_entry_sign: Disabled!", inline=False)
        else:
            embed.add_field(name="", value=c + " :white_check_mark: Enabled!", inline=False)
    return embed

# return list of men disabled for a user
def get_my_men_embed(ctx):
    author = ctx.message.author.id
    mention = ctx.message.author.mention

    embed = discord.Embed(title="MANBOT MY MEN", description=mention + " Here are your inactive men:", color=purple)
    for m in all_men:
        disabled = False
        if author in all_men[m][0]["disabled"]:
            disabled = True
        if disabled:
            embed.add_field(name="", value=m, inline=False)
    return embed

def get_reset_embed(ctx):
    author = ctx.message.author.id
    mention = ctx.message.author.mention

    for c in all_categories:
        # remove author from disabled list if present
        if author in all_categories[c][0]["disabled"]:
            all_categories[c][0]["disabled"].remove(author)
        ManbotUtils.update_file('resources/categories.json', all_categories)
    for m in all_men:
        # remove author from disabled list if present
        if author in all_men[m][0]["disabled"]:
            all_men[m][0]["disabled"].remove(author)
        ManbotUtils.update_file('resources/men.json', all_men)

    return discord.Embed(title="WOOHOO",
                          description=mention + " Successfully reset user.",
                          color=purple)
