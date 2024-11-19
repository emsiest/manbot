import discord

from manbot_utils import ManbotUtils

'''
Implementation for general commands: HELP, LIST CATEGORIES, LIST MEN.
'''

utils = ManbotUtils()
all_categories = utils.all_categories
all_men = utils.all_men
purple = utils.purple

# display help menu
def get_help_embed(ctx):
    embed = discord.Embed(title="HELP MENU", description="To summon a man, include his full name in capital letters anywhere in your message, for example 'I love ZHANG ZHEHAN!'\n\n", color=purple)
    embed.add_field(name="", value="For any broken links or suggestions, please tag Em or dm her the message link.", inline=False)
    embed.add_field(name="\nGeneral Commands:", value="", inline=False)
    embed.add_field(name="", value="`MANBOT HELP` \nView Manbot's help menu. You're here right now!", inline=False)
    embed.add_field(name="", value="`MANBOT LIST CATEGORIES [CATEGORY NAME]` \nView all categories of currently summonable men. You may supply an optional category name to list all subcategories in that category, e.g. MANBOT MEN ANIME.",inline=False)
    embed.add_field(name="", value="`MANBOT LIST MEN <CATEGORY NAME>` \nView names of all currently summonable men in a category. You must supply a category name to list all men in that category, e.g. MANBOT MEN KDRAMA ACTOR.",inline=False)
    embed.add_field(name="", value="`MANBOT RANDOM [CATEGORY NAME]` \nSummon a random man. You may supply an optional category name to summon a random man in that category, e.g. MANBOT RANDOM KDRAMA CHARACTER.", inline=False)
    embed.add_field(name="", value="`MANBOT STATS [MAN/CATEGORY NAME]` \nView Manbot's top most popular men. You may optionally supply a man or category name to see their stats, e.g. MANBOT STATS KPOP.", inline=False)
    embed.add_field(name="\nUser Commands:", value="", inline=False)
    embed.add_field(name="", value="`MANBOT DISABLE <MAN/CATEGORY NAME>` \nDisable a man or category for yourself. You must supply a man or category name, e.g. MANBOT DISABLE CDRAMA ACTOR.", inline=False)
    embed.add_field(name="", value="`MANBOT ENABLE <MAN/CATEGORY NAME>` \nEnable a man or category for yourself. You must supply a man or category name, e.g. MANBOT ENABLE CDRAMA CHARACTER.", inline=False)
    embed.add_field(name="", value="`MANBOT MY CATEGORIES` \nView the categories you have enabled/disabled.",inline=False)
    embed.add_field(name="", value="`MANBOT MY MEN` \nView the men you have disabled.",inline=False)
    embed.add_field(name="", value="`MANBOT RESET` \nReset all your Manbot data and settings. This action cannot be undone!",inline=False)
    embed.add_field(name="\nOther Commands:", value="", inline=False)
    embed.add_field(name="", value="`MANBOT HELLO` \nReceive a greeting.", inline=False)
    embed.add_field(name="", value="`MANBOT SLEEP` \nReceive a loving bedtime message.", inline=False)
    embed.add_field(name="", value="`MANBOT WORK` \nReceive a motivational work message.", inline=False)
    return embed

# return list of all categories or subcategories of a supplied category
def get_list_categories_embed(ctx):
    category = ManbotUtils.get_category(ctx.message.content, " CATEGORIES ")

    if category:
        embed = discord.Embed(title=category + " SUBCATEGORIES", color=purple)
        output = ""
        for s in all_categories[category][0]["subcategories"]:
            output += s + "\n"
        embed.add_field(name="", value=output, inline=False)
    else:
        embed = discord.Embed(title="ALL CATEGORIES", color=purple)
        output = ""
        for c in all_categories:
            output += c + "\n"
        embed.add_field(name="", value=output, inline=False)
        embed.set_footer(text="Call MANBOT CATEGORIES [CATEGORY NAME] to list all subcategories for that category.")
    return embed

# return list of men in a supplied category
def get_list_men_embed(ctx):
    category = utils.get_category(ctx.message.content, " MEN ")

    if category:
        embed = discord.Embed(title=category + " MEN",
                              color=purple)
        output = ""
        for m in all_categories[category][0]["men"]:
            output += m + "\n"
        embed.add_field(name="", value=output, inline=False)
    else:
        embed = discord.Embed(title="HEY",
                              description="Manbot has too many men to be displayed in a single embed. To view the men in a category, type MANBOT MEN followed by the category name, e.g. MANBOT MEN KPOP.",
                              color=purple)
    return embed

# helper to retrieve stats for given man
def get_man_stats(man):
    calls = int(all_men[man][0]["called"])
    rickrolls = int(all_men[man][0]["rickrolled"])
    uwus = int(all_men[man][0]["uwued"])
    return [calls, rickrolls, uwus]

def get_stats_embed(ctx):
    category = utils.get_category(ctx.message.content, " STATS ")
    man = utils.get_man(ctx.message.content, " STATS ")

    # calculate overall leaderboard
    all_stats = dict((m, get_man_stats(m)) for m in all_men)
    sorted_all_stats = sorted(all_stats.keys(), key=lambda x: all_stats[x][0], reverse=True) # list man names by popularity

    embed = discord.Embed(title="MANBOT STATS",description="",color=purple)
    # if message contains valid man name
    if man:
        man_stats = get_man_stats(man)
        embed.add_field(name=man + " - " + all_men[man][0]["category"],
                        value=all_men[man][0]["description"] + "\nCalled **" + str(man_stats[0]) +
                              "** times \nRickrolled users **" + str(man_stats[1]) +
                              "** times \nUwued users **" + str(man_stats[2]) +
                              "** times \nRanked **" + str(sorted_all_stats.index(man)) + "** overall",
                        inline=True)
    # if message contains valid category name
    elif category:
        # get stats for all men in category
        category_men = all_categories[category][0]["men"]
        category_stats = dict((m, all_stats[m]) for m in category_men)
        sorted_category_stats = sorted(category_stats.keys(), key=lambda x: all_stats[x][0], reverse=True)  # list man names by popularity

        embed = discord.Embed(title="MANBOT STATS - " + category,
                              description="Manbot knows " + str(len(category_stats)) + " men in this category.",
                              color=purple)
        embed.description = "Manbot knows " + str(len(category_stats)) + " men in this category."
        # get leaderboard for men in category
        for i in range(0, min(9, len(category_stats))):
            ranked_man = sorted_category_stats[i]
            embed.add_field(name=str(i + 1) + " - " + ranked_man,
                            value="Called **" + str(category_stats[ranked_man][0]) +
                                  "** times\n Rickrolled users **" + str(category_stats[ranked_man][1]) +
                                  "** times\n Uwued users **" + str(category_stats[ranked_man][2]) +
                                  "** times \nRanked **" + str(sorted_all_stats.index(ranked_man)) + "** overall",
                            inline=True)

        # display most recently added man
        newest_man = category_men[-1]
        embed.add_field(name="Most recently added man: " + newest_man,
                        value=all_men[newest_man][0]["description"],
                        inline=False)
    # else return overall leaderboard
    else:
        embed = discord.Embed(title="MANBOT STATS",
                              description="Manbot knows " + str(len(all_stats)) + " total men.",
                              color=purple)

        # get leaderboard for all men
        for i in range(0, 9):
            ranked_man = sorted_all_stats[i]
            embed.add_field(name=str(i + 1) + " - " + ranked_man,
                            value="Called **" + str(all_stats[ranked_man][0]) +
                                  "** times\n Rickrolled users **" + str(all_stats[ranked_man][1]) +
                                  "** times\n Uwued users **" + str(all_stats[ranked_man][2]) + "** times",
                            inline=True)

        # display most recently added man
        newest_man = list(all_men.keys())[-1]
        embed.add_field(name="Most recently added man: " + newest_man,
                        value=all_men[newest_man][0]["description"],
                        inline=False)

        embed.add_field(name="", value="Call MANBOT STATS [MAN/CATEGORY NAME] to get stats on any individual man or category.", inline=False)

    embed.set_footer(text="Manbot started counting stats on 25 April 2021.")
    return embed
