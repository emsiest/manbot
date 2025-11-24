import discord
import random

from manbot_utils import ManbotUtils

'''
Implementation for RANDOM command and get_man
'''

utils = ManbotUtils()
all_categories = utils.all_categories
all_men = utils.all_men
purple = utils.purple

# helper to return random image of given man and update stats
def get_image_for_man(man):
    # update stats
    called = int(all_men[man][0]["called"])
    all_men[man][0]["called"] = str(called + 1)
    ManbotUtils.update_file("resources/men.json", all_men)

    # get random image of man
    file_name = all_men[man][0]["filename"]
    images = ManbotUtils.read_file(file_name)
    return random.choice(images)

# check message for man name and return image
# user has a random chance of uwuing or rickrolling
def get_man(message):
    author = message.author.id
    mention = message.author.mention

    # selects first man found in message
    man = None
    for m in all_men.keys():
        if m in message.content:
            man = m
            break
    if not man:
        return

    if random.randint(0, 19) == 0:
        uwu_count = int(all_men[man][0]["uwued"])
        all_men[man][0]["uwued"] = str(uwu_count + 1)
        ManbotUtils.update_file("resources/men.json", all_men)
        if man in ["GONG JUN", "ZHANG ZHEHAN", "WEN KEXING", "ZHOU ZISHU"]:
            return mention + " " + man + " says WUHU to you!!! :smiling_face_with_3_hearts::musical_note::notes:"
        else:
            return mention + " " + man + " says uwu to you!!! :smiling_face_with_3_hearts:"
    elif random.randint(0, 99) == 69:
        rick_roll_count = int(all_men[man][0]["rickrolled"])
        all_men[man][0]["rickrolled"] = str(rick_roll_count + 1)
        ManbotUtils.update_file("resources/men.json", all_men)
        if man in ["GONG JUN", "ZHANG ZHEHAN", "WEN KEXING", "ZHOU ZISHU"]:
            return "https://www.youtube.com/watch?v=Pwdr8Q_wjBI&ab" + " you've been WUHUED!!!"
        else:
            return "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    else:
        return get_image_for_man(man)

def get_random_embed(ctx):
    mention = ctx.message.author.mention
    category = utils.get_category(ctx.message.content, " RANDOM ")

    men = []
    # if message contains valid category name
    if category:
        # add all men in category
        for m in all_men:
            if all_men[m][0]["category"] == category:
                men.append(m)
    # else add all categories
    else:
        men = list(all_men.keys())

    # return random man from enabled men
    random_man = random.choice(men)
    embed = discord.Embed(title="RANDOM", description=mention + " You summoned " + random_man + ", " + all_men[random_man][0]["description"], color=purple)
    embed.set_image(url=get_image_for_man(random_man))
    return embed
