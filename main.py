import discord
import os
import random
import json
import re
import asyncio
from keep_alive import keep_alive

client = discord.Client()
with open('men.json') as f:
    men = json.load(f)
with open('users.json') as f:
    manbotUsers = json.load(f)

def min_distance(whomst, call):
    word1 = []
    word2 = []
    for char in whomst:
        word1.append(char) 
    for char in call: 
        word2.append(char)
    j = 0 
    i = 0 
    if abs(len(word1) - len(word2)) >= 2: 
        return 0
    else:
        while (i < len(word2)) and (i < len(word1)): 
            if word1[i] != word2[i]:  
                j = j + 1  
            i = i + 1 
        if j != 0 and j <= 2: 
            return 1  
        else:
            return 0 

def check_for_typo(message):
    splitMsg = str.split(message) 
    manName = splitMsg[0] + " " + splitMsg[1] 
    for i in men:
      if i != "HU GE":
        output = min_distance(i, manName)
        if output == 1:
            fileObj = open("images/hornyJail.txt", "r")
            images = fileObj.readlines()
            j = random.randint(0, len(images) - 1)
            jc = images[j] + " too thirsty to spell, huh "
            return (jc)

def get_man(name, mention, jc,x):
    k = men[name][0]["filename"]
    callCounter = int(men[name][0]["called"])
    comp1 =  callCounter
    callCounter = callCounter + 1
    men[name][0]["called"] = men[name][0]["called"].replace(men[name][0]["called"], str(callCounter))
    comp2 = men[name][0]["called"]

    if comp1 == comp2:
      jc.append("Call counter not updated!")

    j = random.randint(0, 9)  
    rr = random.randint(0, 99) 
    fileObj = open(k, "r") 
    images = fileObj.readlines()  
    i = random.randint(0,len(images)-1)  
    jc.append(images[i])  
    fileObj.close()  

    if x !=1:

      if j == 1 and k == "images/gjImages.txt":
        jc.append(" " + mention + " " + str.lower(name) +" says WUHU to you!!! :smiling_face_with_3_hearts::musical_note::notes:")
        uwuCounter = int(men[name][0]["uwued"])
        uwuCounter = uwuCounter + 1
        men[name][0]["uwued"] = men[name][0]["uwued"].replace(men[name][0]["uwued"], str(uwuCounter))

      if j == 1 and k != "images/gjImages.txt":
        jc.append(" " + mention + " " + str.lower(name) + " says uwu to you!!! :smiling_face_with_3_hearts:")
        uwuCounter = int(men[name][0]["uwued"])
        uwuCounter = uwuCounter + 1
        men[name][0]["uwued"] = men[name][0]["uwued"].replace(men[name][0]["uwued"], str(uwuCounter))

      if rr == 69:  #return rickroll if rr==69
        jc.append("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        rrCounter = int(men[name][0]["rickrolled"])
        rrCounter = rrCounter + 1
        men[name][0]["rickrolled"] = men[name][0]["rickrolled"].replace(men[name][0]["rickrolled"], str(rrCounter))

      if rr == 1:
        jc.append("https://www.youtube.com/watch?v=Pwdr8Q_wjBI&ab" +" you've been WUHUED!!!")
        rrCounter = int(men[name][0]["rickrolled"])
        rrCounter = rrCounter + 1
        men[name][0]["rickrolled"] = men[name][0]["rickrolled"].replace(men[name][0]["rickrolled"], str(rrCounter))

    with open('men.json', 'w') as outfile:
        json.dump(men, outfile)
    return (jc)

def man_stats(man):
    calls = str(men[man][0]["called"])
    rickrolls = str(men[man][0]["rickrolled"])
    uwus = str(men[man][0]["uwued"])
    jc = "Called by users** " + calls + " **times\n Rickrolled users** " + rickrolls + " **times\n Uwued users **" + uwus + " **times"
    return (jc)

def user_favorites(bro,mention,manbotIcon):
    if str(bro) in manbotUsers:
      if len(manbotUsers[str(bro)][0]["favorites"]) > 0:
          embeds = []
          images = []
          for i in manbotUsers[str(bro)][0]["favorites"]:
             images.append(i)
          embeds.append(images)
          jc = embeds

      else:
         embedVar = discord.Embed(title="FAVORITES", description=mention, color=0x7800b4)
         embedVar.add_field(name="HEY!", value="You haven't saved any favorites! React to a manbot image to save a favorite.", inline=False)
         embedVar.set_author(name="el's manbot", icon_url=manbotIcon)
         jc = [embedVar]
      return(jc)

def remove_favorites(bro,url,mention,manbotIcon):
      x = manbotUsers[str(bro)][0]["favorites"]
      temp = []
      for i in x:
        if i != url:
          temp.append(i)
      manbotUsers[str(bro)][0]["favorites"] = temp
      with open('users.json', 'w') as outfile:
        json.dump(manbotUsers, outfile)
      embed = discord.Embed(title="FAVORITE REMOVED", description=mention, color=0x7800b4)
      embed.add_field(name="He's gone", value="You have successfully removed this image from your favorites list. React to this message to add it back.", inline=False)
      embed.set_author(name="el's manbot", icon_url=manbotIcon)
      embed.set_image(url=url)
      return(embed)

def user_checker(sender):
  sender = str(sender)
  if sender in manbotUsers:
    return(0)
  else:
   data = {}
   data[str(sender)] = []
   data[str(sender)].append({"favorites":[]})
   data[str(sender)].append({"call tracker":[]})
   temp = manbotUsers
   temp.update(data)
   with open('users.json', 'w') as outfile:
    json.dump(temp, outfile)
   return(1)

def user_remover(sender):
  sender = str(sender)
  if sender in manbotUsers:
    if not manbotUsers[sender][1]["call tracker"]:
      if not manbotUsers[sender][0]["favorites"]:
        del manbotUsers[sender]
        with open('users.json', 'w') as outfile:
          json.dump(manbotUsers, outfile)
  return

def timeout_message(mention):
  jc = discord.Embed(title="TIMED OUT",description=mention,color=0x7800b4)
  jc.add_field(name="Hey!",value="You timed out. Call the command once more to try again.")
  return(jc)

def man_tracker(user,name):
  user = str(user)
  if user in manbotUsers:
    if "call tracker" in manbotUsers[user][1]:
     if name in str(manbotUsers[user][1]["call tracker"]):
        i = 0
        while i < len(manbotUsers[user][1]["call tracker"]):
         if name in manbotUsers[user][1]["call tracker"][i]:
          counter = int(manbotUsers[user][1]["call tracker"][i][name])
          counter = counter + 1
          manbotUsers[user][1]["call tracker"][i][name] = manbotUsers[user][1]["call tracker"][i][name].replace(manbotUsers[user][1]["call tracker"][i][name], str(counter))
          temp = manbotUsers
          with open('users.json', 'w') as outfile:
           json.dump(manbotUsers, outfile)
          return(0)
         else:
           i = i+1
     else: 
        manbotUsers[user][1]["call tracker"].append({name:"1"})
        temp = manbotUsers
        with open('users.json', 'w') as outfile:
         json.dump(manbotUsers, outfile)
        return(1)
    else:
      if "favorites" in manbotUsers[user][0]:
       manbotUsers[user].append({"call tracker":[{name:"1"}]})
       temp = manbotUsers
       with open('users.json', 'w') as outfile:
        json.dump(temp, outfile)
       return(2)
  return


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name='MANBOT HELP'))
    #await client.change_presence(activity=discord.Game(name='CURRENTLY UNDER MAINTENANCE; NOT ALL FUNCTIONALITY MAY WORK AS EXPECTED'))
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    mention = message.author.mention
    userMessage = message.content
    sender = message.author.id
    senderNOID = message.author
    manbotIcon = client.user.avatar_url

    if (message.author == client.user) or (sender == 834302490106789918):  #bot cannot trigger itself or be triggered by thirstbot
        return

    passed = check_for_typo(userMessage)
    if passed != None:
        jc = passed + " " + mention + "? :wink:"

    user_checker(sender)

    for i in men:
        if i in userMessage:
          man_tracker(message.author.id,i)
          mess = []
          jc = get_man(i, mention, mess,0)
    
    if message.content.startswith('MANBOT RANDOM'):
        menNames = []
        for i in men:
            menNames.append(i)
        i = random.choice(menNames)
        jc = []
        man_tracker(message.author.id,i)
        temp = get_man(i, mention, jc,1)

        embedVar = discord.Embed(title="MANBOT RANDOM",description=mention,color=0x7800b4)
        embedVar.set_author(name="el's manbot", icon_url=manbotIcon)
        embedVar.set_image(url=temp[0])
        embedVar.set_footer(text="You summoned "+ str.upper(i))
        jc = embedVar

    if message.content.startswith('MANBOT MEN'):
      embedVar = discord.Embed(title="MANBOT MEN", description="To summon a man, include his full name in capital letters anywhere in your message. Want a new man in Manbot or more pictures for an existing man? Fill out this form [here](https://forms.gle/ZZebbBqTxhfD5zTb8).\n\nManbot currently has the following men:", color=0x7800b4)
      menList = []
      countList = []
      for i in men:
       menList.append(i)
       menList.sort()
      for i in menList:
        countList.append(men[i][0]["description"])
      i = 0
      while i < len(menList):
       embedVar.add_field(name=menList[i], value=countList[i],inline=True)
       i = i+ 1
      embedVar.set_author(name="el's manbot", icon_url=manbotIcon)
      jc = embedVar

    if message.content.startswith('MANBOT STATS'):
      embedVar = discord.Embed(title="MANBOT STATS", description="Manbot started counting stats on 25 April 2021. Manbot is in " + str(len(client.guilds)) + " thirsty, thirsty servers!", color=0x7800b4)
      embedVar.set_author(name="el's manbot", icon_url=manbotIcon)

    #    for guild in client.guilds:
      #    print(guild.name)
 
      for i in men:
        j = man_stats(i)
        embedVar.add_field(name=i, value=j,inline=True)
      jc = embedVar

    if message.content.startswith("MANBOT MY STATS"):
      embed=discord.Embed(title="YOUR STATS",description=mention,color=0x7800b4)
      embed.set_author(name="el's manbot", icon_url=manbotIcon)
      if manbotUsers[str(sender)][1]["call tracker"] == []:
        embed.add_field(name="Hold it!", value="You haven't summoned any men before! Call a man to start your stats page.", inline=False)
        jc = embed
      else:
       userID = str(sender)
       i = 0
       keys = []
       while i < len(manbotUsers[userID][1]["call tracker"]):
        keys.append(manbotUsers[userID][1]["call tracker"][i])
        i = i + 1
       keys = list(keys)
       for i in keys:
        keysRegex = re.findall(r'[\s\w]',str(i))
        manStat = ''.join(map(str, keysRegex))
        splitStat = manStat.split(" ")
        embed.add_field(name=splitStat[0]+" "+splitStat[1],value="Called by you "+splitStat[2]+" time(s).",inline=True)
        jc = embed

    if message.content.startswith('MANBOT FAVES'):
      jc = user_favorites(message.author.id,mention,manbotIcon)
      page = 0
      arrows = ['⬅️',"➡️"]
      if not isinstance(jc[0],discord.Embed):
        embedVar = discord.Embed(title="YOUR FAVORITES", description=mention, color=0x7800b4)
        embedVar.set_author(name="el's manbot", icon_url=manbotIcon)
        embedVar.set_image(url=jc[0][0])
        embedVar.set_footer(text="1/"+str(len(jc[0]))+ "\nReact to any favorited image with 💔 to remove it from your favorites list.")
        msg = await message.channel.send(embed=embedVar)
        messId = msg.id
        if len(jc[0]) > 1:
          for emoji in arrows:
             await msg.add_reaction(emoji)
        await asyncio.sleep(1)
        def check(reaction, user):
            return user == senderNOID and (str(reaction.emoji) == '⬅️' or str(reaction.emoji) == "➡️" or str(reaction.emoji) == "💔")
        x = 0
        while x == 0:       
          try:
             reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
          except asyncio.TimeoutError:
            x = 1
            return
          if (str(reaction.emoji) == '⬅️') and (reaction.message.id==messId):
               if (page == 0):
                 page = (len(jc[0])-1)
               else:
                 page = page - 1
               embedVar.set_image(url=jc[0][page])
               embedVar.set_footer(text=str(page+1)+"/"+str(len(jc[0]))+ "\nReact to any favorited image with 💔 to remove it from your favorites list.")
               await msg.edit(embed=embedVar)
          if (str(reaction.emoji) == '➡️') and (reaction.message.id==messId):
              if page == (len(jc[0])-1):
                page = 0
              else:
                page = page + 1
              embedVar.set_image(url=jc[0][page])
              embedVar.set_footer(text=str(page+1)+"/"+str(len(jc[0]))+ "\nReact to any favorited image with 💔 to remove it from your favorites list.")
              await msg.edit(embed=embedVar)
          if (str(reaction.emoji) == '💔') and (reaction.message.id==messId):
           jc =  remove_favorites(sender,str(jc[0][page]),mention,manbotIcon)
           await message.channel.send(embed=jc)
            

    if message.content.startswith("MANBOT ERASE MY DATA"):
      hontou = embedVar = discord.Embed(title="ERASE MY DATA", description=mention, color=0x7800b4)
      hontou.add_field(name="Are you sure? This action cannot be undone.",value="React with 🗑️ (wastebasket) to delete your data")
      hontou.set_author(name="el's manbot", icon_url=manbotIcon)
      hontou = await message.channel.send(embed=hontou)
      messId = hontou.id
      def check(reaction, user):
         return user == senderNOID and (str(reaction.emoji) == "🗑️")
      try:
         reaction, user = await client.wait_for('reaction_add', timeout=30.0, check=check)
      except asyncio.TimeoutError:
         jc = timeout_message(mention)
         jc.set_author(name="el's manbot", icon_url=manbotIcon)
         await message.channel.send(embed=jc)
         return

      print(messId)
      print(reaction.message.id)
      if (str(reaction.emoji) == "🗑️") and (reaction.message.id == messId):
        if str(sender) in manbotUsers:
           del manbotUsers[str(sender)]
           with open('users.json', 'w') as outfile:
             json.dump(manbotUsers, outfile)
           jc = embedVar = discord.Embed(title="DATA DELETED", description=mention, color=0x7800b4)
           jc.add_field(name="Success!",value="Your data was deleted.")
           jc.set_author(name="el's manbot", icon_url=manbotIcon)

    if message.content.startswith("MANBOT SLEEP"):
      jc = []
      jc.append("https://cdn.discordapp.com/attachments/830234510124777493/836395008269615144/image0.jpg")
      fileObj = open("sleep.txt", "r")
      sleepy = fileObj.readlines()  
      i = random.randint(0,len(sleepy)-1) 
      fileObj.close() 
      jc.append("Hey! "+sleepy[i])

    if message.content.startswith('MANBOT SEND MAN ADDED MESSAGE') and message.author.id == 262822280357216257:
      #format: MANBOT SEND MAN ADDED MESSAGE 262822280357216257 YAN YUJIN
      splitStr = str.split(message.content)
      leng = len(splitStr)
      man = splitStr[leng-2] + " "+ splitStr[leng-1]
      print(man)
      id = splitStr[leng-3]
      mention = int(id)
      sendto = await client.fetch_user(mention)
      print(sendto)
      await sendto.send("As per your request, " + man + " is now summonable in Manbot. Thanks for requesting him! Any replies sent to this message will not be seen.")
      jc = "message sent"

    if message.content.startswith('MANBOT HELP'):
        embedVar = discord.Embed(title="MANBOT HELP", description="*Preface all the following commands with MANBOT to use them.*", color=0x7800b4)
        embedVar.add_field(name="HELP", value="View Manbot's help menu. You're here right now!", inline=False)
        embedVar.add_field(name="MEN", value="View all currently summonable men. To summon a man, include his full name in capital letters anywhere in your message.", inline=False)
        embedVar.add_field(name="RANDOM", value="Summon a random man.", inline=False)
        embedVar.add_field(name="FAVES", value="View a gallery of your favorite images. React to any manbot image to add it to your favorites list. ", inline=False)
        embedVar.add_field(name="STATS", value="View pan-server bot stats.", inline=False)
        embedVar.add_field(name="MY STATS", value="View your individual stats.", inline=False)
        embedVar.add_field(name="SLEEP", value="Have Manbot send a bedtime reminder.", inline=False)
        embedVar.add_field(name="ERASE MY DATA", value="Erase ALL your Manbot data (this action cannot be undone!)", inline=False)
        embedVar.set_author(name="el's manbot", icon_url=manbotIcon)
        embedVar.set_footer(text="UPDATE 16 JUNE 2021: Favorited images can now be removed. Want Manbot in your server? Invite Manbot here: https://top.gg/bot/829189738387734530")
        jc = embedVar

    user_remover(sender)

    if isinstance(jc, list) == True:
        for i in jc:
            if isinstance(i, discord.Embed):
              await message.channel.send(embed=i)
            else:
              await message.channel.send(i)
    elif isinstance(jc, discord.Embed):
      await message.channel.send(embed=jc)
    else:
        await message.channel.send(jc)

@client.event
async def on_reaction_add(reaction, user):
    if ((reaction.message.author.id == 829189738387734530) or (reaction.message.author.id == 836346113731592262)):
        users = await reaction.users().flatten()
        count = reaction.count
        itsMe = users[count-1]

        async for user in reaction.users():
            myId = str(itsMe.id)
            fave = ""
            if "http" in reaction.message.content:
              fave = reaction.message.content
            else:
              if len(reaction.message.embeds) == 1:
                if (reaction.message.embeds[0].title =="MANBOT RANDOM") or (reaction.message.embeds[0].title =="FAVORITE REMOVED"):
                  fave = reaction.message.embeds[0].image.url
            if myId in manbotUsers:
              if fave != "":
                manbotUsers[myId][0]["favorites"].append(fave)
                with open('users.json', 'w') as outfile:
                  json.dump(manbotUsers, outfile)
                  return
              return
            else:
              if (myId != str(829189738387734530)) and (myId != str(836346113731592262)):
                data = {}
                data[myId] = []
                data[myId].append({"favorites":[]})
                if fave != "":
                  data[myId][0]["favorites"].append(fave)
                data[myId].append({"call tracker":[]})
                temp = manbotUsers
                temp.update(data)
                with open('users.json', 'w') as outfile:
                  json.dump(temp, outfile)
                  return

keep_alive()
client.run(os.getenv('TOKEN'))
