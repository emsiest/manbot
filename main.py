import discord
import os
import random
import json
import re
import asyncio

client = discord.Client()
with open('men.json') as f:
    men = json.load(f)
with open('users.json') as f:
    manbotUsers = json.load(f)
with open('categories.json') as f:
    manbotCategories = json.load(f)

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

def man_stats_2(man):
    calls = int(men[man][0]["called"])
    rickrolls = int(men[man][0]["rickrolled"])
    uwus = int(men[man][0]["uwued"])
    jc = [calls, rickrolls, uwus]
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

def user_checker(sender,serverId):
  userHandle = str(sender.name)+str(sender.discriminator)
  sender = str(sender.id)
  if sender in manbotUsers:
    if (str(serverId) in manbotUsers[sender][2]["servers"]) and (str(userHandle) in manbotUsers[sender][3]["handles"]):
      return(0)
    else:
      if not str(serverId) in manbotUsers[sender][2]["servers"]:
       manbotUsers[sender][2]["servers"].append(str(serverId))
      if not str(userHandle) in manbotUsers[sender][3]["handles"]:
       manbotUsers[sender][3]["handles"].append(str(userHandle))
      with open('users.json', 'w') as outfile:
         json.dump(manbotUsers, outfile)
         return(2)

  else:
   data = {}
   data[str(sender)] = []
   data[str(sender)].append({"favorites":[]})
   data[str(sender)].append({"call tracker":[]})
   data[str(sender)].append({"servers":[]})
   data[str(sender)][2]["servers"].append(str(serverId))
   data[str(sender)].append({"handles":[]})
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
    #await client.change_presence(activity=discord.Game(name='CURRENTLY UNDER MAINTENANCE'))
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
 # if client.activity.name == "CURRENTLY UNDER MAINTENANCE":
 #   return
 # else:
    mention = message.author.mention
    userMessage = message.content
    sender = message.author.id
    senderNOID = message.author
    manbotIcon = client.user.avatar_url
    serverId = message.guild.id

    if (message.author == client.user) or (sender == 834302490106789918):  #bot cannot trigger itself or be triggered by thirstbot
        return

    passed = check_for_typo(userMessage)
    if passed != None:
        jc = passed + " " + mention + "? :wink:"

    user_checker(message.author,serverId)

    for i in men:
        if i in userMessage:
            man_tracker(message.author.id,i)
            mess = []
            if not userMessage.startswith("MANBOT STATS"):
              jc = get_man(i, mention, mess,0)
            if userMessage.startswith("MANBOT STATS "):
              jc = get_man(i, mention, mess,1)
              man = man_stats_2(i)

              embedVar = discord.Embed(title=i,description=mention,color=0x7800b4)
              embedVar.set_author(name="el's manbot", icon_url=manbotIcon)
              embedVar.set_image(url=jc[0])
              embedVar.add_field(name="WHO'S HE?", value=men[i][0]["description"],inline=False)
              calls = str(man[0])
              uwus = str(man[1])
              rickrolls = str(man[2])
              j = "Called by users** " + calls + " **times\n Rickrolled users** " + rickrolls + " **times\n Uwued users **" + uwus + " **times"
              embedVar.add_field(name=i, value=j,inline=True)
              jc= embedVar

    if message.content.startswith("MANBOT DISABLE"):
       categoryTuple = message.content.rpartition(" DISABLE ")
       x = 0

       if categoryTuple[2] == "KDRAMA (CHARACTER)":
        category = "KDC"
       elif categoryTuple[2] == "KDRAMA (ACTOR)":
        category = "KDA"
       elif categoryTuple[2] == "CDRAMA (CHARACTER)":
        category = "CDC"
       elif categoryTuple[2] == "CDRAMA (ACTOR)":
        category = "CDA"
       else:
        category = categoryTuple[2]

       for i in manbotCategories:
         if str(sender) not in manbotCategories[i][0]["disabled"]:
          if category == i:
           manbotCategories[i][0]["disabled"].append(str(sender))
           with open('categories.json', 'w') as outfile:
            json.dump(manbotCategories, outfile)
            embedVar = discord.Embed(title="MANBOT CATEGORIES",description=mention,color=0x7800b4)
            embedVar.set_author(name="el's manbot", icon_url=manbotIcon)
            embedVar.add_field(name="SUCCESS!", value="You've successfully disabled that category.",inline=True)
            x = 1
            jc = embedVar
         else:
           if x == 0 and (category in manbotCategories):
            embedVar = discord.Embed(title="HEY!",description=mention,color=0x7800b4)
            embedVar.set_author(name="el's manbot", icon_url=manbotIcon)
            embedVar.add_field(name="HOLD IT!", value="You've already disabled that category!",inline=True)
          
            jc = embedVar

    if message.content.startswith("MANBOT ENABLE"):
      categoryTuple = message.content.rpartition(" ENABLE ")
      x = 0

      if categoryTuple[2] == "KDRAMA (CHARACTER)":
        category = "KDC"
      elif categoryTuple[2] == "KDRAMA (ACTOR)":
        category = "KDA"
      elif categoryTuple[2] == "CDRAMA (CHARACTER)":
        category = "CDC"
      elif categoryTuple[2] == "CDRAMA (ACTOR)":
        category = "CDA"
      else:
        category = categoryTuple[2]

      for i in manbotCategories:
        if str(sender) in manbotCategories[i][0]["disabled"]:
         if category == i:
           for j in manbotCategories[i][0]["disabled"]:
             if j == str(sender):
              manbotCategories[i][0]["disabled"].remove(str(sender))
              with open('categories.json', 'w') as outfile:
                json.dump(manbotCategories, outfile)
                embedVar = discord.Embed(title="MANBOT CATEGORIES",description=mention,color=0x7800b4)
                embedVar.set_author(name="el's manbot", icon_url=manbotIcon)
                embedVar.add_field(name="SUCCESS!", value="You've successfully enabled that category.",inline=True)
                x = 1
                jc = embedVar
        else:
            if x == 0 and (category in manbotCategories):
             embedVar = discord.Embed(title="HEY!",description=mention,color=0x7800b4)
             embedVar.set_author(name="el's manbot", icon_url=manbotIcon)
             embedVar.add_field(name="HOLD IT!", value="You've already enabled that category!",inline=True)
             jc = embedVar

    if message.content.startswith('MANBOT MY CATEGORIES'):
      embedVar = discord.Embed(title="MANBOT MY CATEGORIES",description=mention,color=0x7800b4)
      embedVar.set_author(name="el's manbot", icon_url=manbotIcon)

      temp = []

      for i in manbotCategories:
        temp.append(i)

      for i in manbotCategories:
       for j in manbotCategories[i][0]["disabled"]:
        if str(sender) == j:
          embedVar.add_field(name=i, value=":no_entry_sign: Disabled!",inline=True)
          temp.remove(i)
      for i in temp:
          embedVar.add_field(name=i, value=":white_check_mark: Enabled!",inline=True)
     
      embedVar.set_footer(text="To enable and disable categories, call MANBOT ENABLE [CATEGORY NAME] or MANBOT DISABLE [CATEGORY NAME] respectively. For example, MANBOT ENABLE ANIME enables anime for your user. KDA, CDC, KDC, CDA, stand for Kdrama (Actor), Cdrama (Character), etc.")     
      jc = embedVar

    if message.content.startswith('MANBOT RANDOM'):
      menNames = []
      enabledCategories = []
      x = 0
      for i in manbotCategories:
          if str(sender) not in manbotCategories[i][0]["disabled"]:
            enabledCategories.append(i)

      if enabledCategories == []:
            embedVar = discord.Embed(title="HEY!",description=mention,color=0x7800b4)
            embedVar.set_author(name="el's manbot", icon_url=manbotIcon)
            embedVar.add_field(name="HOLD IT!", value="You've disabled all the categories! Enable a category to use manbot random. Categories may be enabled by calling MANBOT ENABLE [CATEGORY NAME], e.g. MANBOT ENABLE ANIME.",inline=True)
            jc = embedVar
            x = 1

      for i in enabledCategories:
       if i == "KDC":
        enabledCategories.append("KDRAMA (CHARACTER)")
       if i == "KDA":
        enabledCategories.append("KDRAMA (ACTOR)")
       if i == "CDC":
        enabledCategories.append("CDRAMA (CHARACTER)")
       if i == "CDA":
        enabledCategories.append("CDRAMA (ACTOR)")
      
      if x == 0:
        for i in men:
          for j in enabledCategories:
           if men[i][0]["category"].upper() == j:
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
      categories = ["CDRAMA (CHARACTER)","CDRAMA (ACTOR)","KDRAMA (CHARACTER)","KDRAMA (ACTOR)","KPOP","ANIME","MCYT"]
      categories.sort()
      menList = []
      countList = []
      howManyMen = [0,0,0,0,0,0,0]
      categoryTuple = message.content.rpartition(" MEN ")
      
      for i in men:
        if men[i][0]["category"].upper() in categories:
            howManyMen[categories.index(men[i][0]["category"].upper())] = howManyMen[categories.index(men[i][0]["category"].upper())] + 1

      if categoryTuple[0] == "":
        embedVar = discord.Embed(title="MANBOT MEN - CATEGORIES ", description="Manbot has too many men to be displayed in a single embed. To view the men in a category, type MANBOT MEN followed by the category name in all caps, e.g. 'MANBOT MEN KPOP'", color=0x7800b4)
        embedVar.set_author(name="el's manbot", icon_url=manbotIcon)
        j=0
        for i in categories:

         embedVar.add_field(name=i, value=str(howManyMen[j])+" men in this category",inline=False)
         j = j+1
         
        embedVar.set_footer(text="KDC, KDA, CDC, CDA may be used in place of Cdrama (Character), Kdrama (Actor), etc. For example, MANBOT MEN CDC is equivalent to MANBOT MEN CDRAMA (CHARACTER)")
        jc = embedVar

      else:
       if categoryTuple[2] == "KDC":
        category = "KDRAMA (CHARACTER)"
       elif categoryTuple[2] == "KDA":
        category = "KDRAMA (ACTOR)"
       elif categoryTuple[2] == "CDC":
        category = "CDRAMA (CHARACTER)"
       elif categoryTuple[2] == "CDA":
        category = "CDRAMA (ACTOR)"
       else:
        category = categoryTuple[2]

       if category in categories:
        for i in men:
         if men[i][0]["category"].upper() == category.upper():
          menList.append(i)
          menList.sort()

       for i in menList:
        countList.append(men[i][0]["description"])
       i = 0

       embedVar = discord.Embed(title="MANBOT MEN - "+category, description="To summon a man, include his full name in capital letters anywhere in your message. Want a new man in Manbot or more pictures for an existing man? Fill out this form [here](https://forms.gle/ZZebbBqTxhfD5zTb8). Submissions are usually processed within one week.\n\nManbot currently has the following men for this category:", color=0x7800b4)
       while i < len(menList):
        embedVar.add_field(name=menList[i], value=countList[i],inline=True)
        i = i+ 1
       embedVar.set_author(name="el's manbot", icon_url=manbotIcon)
       jc = embedVar

    if message.content == 'MANBOT STATS':
      embedVar = discord.Embed(title="MANBOT STATS", description="Manbot started counting stats on 25 April 2021. Manbot is in " + str(len(client.guilds)) + " thirsty, thirsty servers! The most popular men are:", color=0x7800b4)
      embedVar.set_author(name="el's manbot", icon_url=manbotIcon)
      embedVar.set_footer(text="Calll MANBOT STATS [MAN NAME] to get stats on any individual man. For example, MANBOT STATS ZHANG ZHEHAN will pull up Zhang Zhehan's stats.")

      sortMen = []
      for i in men:
        sortMen.append([i,man_stats_2(i)])
      sortMen = sorted(sortMen, key=lambda x: x[1][0], reverse=True)

      for i in range(0,9):
        calls = str(sortMen[i][1][0])
        uwus = str(sortMen[i][1][1])
        rickrolls = str(sortMen[i][1][2])
        j = "Called by users** " + calls + " **times\n Rickrolled users** " + rickrolls + " **times\n Uwued users **" + uwus + " **times"
        embedVar.add_field(name=str(i+1)+ " - " + sortMen[i][0], value=j,inline=True)
      
      menNames = []
      for i in men:
        menNames.append(i)
      x = len(menNames)
      newestMan = menNames[x-1]
      embedVar.add_field(name="Most Recently Added Man: "+ str(newestMan), value=men[newestMan][0]["description"],inline=False)
      jc = embedVar

    if message.content.startswith('MANBOT WHAT SERVERS') and message.author.id == 262822280357216257:
      serverList = []
      for guild in client.guilds:
        serverList.append(guild.name)
      jc = serverList

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

    if message.content.startswith("MANBOT WORK"):
      jc = []
      jc.append("https://cdn.discordapp.com/attachments/830234510124777493/873390001499566150/manbotwork.png")
      fileObj = open("work.txt", "r")
      sleepy = fileObj.readlines()  
      i = random.randint(0,len(sleepy)-1) 
      fileObj.close() 
      jc.append("Hey! "+sleepy[i])

    if message.content.startswith('MANBOT SEND MAN ADDED MESSAGE') and message.author.id == 262822280357216257:
      #format: MANBOT SEND MAN ADDED MESSAGE 262822280357216257 WEN KEXING
      splitStr = str.split(message.content)
      leng = len(splitStr)
      man = splitStr[leng-2] + " "+ splitStr[leng-1]
      print(man)
      id = splitStr[leng-3]
      mention = int(id)
      sendto = await client.fetch_user(mention)
      print(sendto)
      await sendto.send("As per your request, :sparkles: " + man + " :sparkles: is now summonable in Manbot (or new pictures of him were added!). Thanks for requesting him! :heart_eyes: \n\nLike Manbot? Vote for him or add him to your server at https://top.gg/bot/829189738387734530. Any replies sent to this message will not be seen.")
      jc = "message sent"

    if message.content.startswith('MANBOT SEND ERROR MESSAGE') and message.author.id == 262822280357216257:
      #format: MANBOT SEND MESSAGE 262822280357216257 messagetext
      x = message.content
      splitStr = x.split(" ",4)
      messagetext = splitStr[4]
      id = splitStr[3]
      mention = int(id)
      sendto = await client.fetch_user(mention)
      print(sendto)
      sent = await sendto.send("Hi there. :wave: You are receiving this message because there was a problem with your Manbot request form submission. " + messagetext + " You may resubmit the form with the issue corrected. https://forms.gle/xDJJbFhAqG7gA1ok7 Any replies to this DM will not be seen. If you have questions, please message celebrian#3368 to speak with El directly.")
      jc = sent

    if message.content.startswith('MANBOT HELP'):
        embedVar = discord.Embed(title="MANBOT HELP", description="*To SUMMON A MAN, include his full name in capital letters anywhere in your message, such as 'I love ZHANG ZHEHAN!' Call any of the following commands (typing in all caps) to use them. Want Manbot in your server? Invite Manbot [here](https://top.gg/bot/829189738387734530).*", color=0x7800b4)
        embedVar.add_field(name="MANBOT HELP", value="View Manbot's help menu. You're here right now!", inline=False)
        embedVar.add_field(name="MANBOT MEN", value="View all categories of currently summonable men. This command takes an optional argument of a category name, such as MANBOT MEN ANIME, to see all the men in that category.", inline=False)
        embedVar.add_field(name="MANBOT RANDOM", value="Summon a random man. Categories of men may be enabled and disabled by calling MANBOT ENABLE [CATEGORY NAME] or MANBOT DISABLE [CATEGORY NAME].", inline=False)
        embedVar.add_field(name="MANBOT ENABLE/DISABLE", value="Enable or disable a category in the random roulette. This command takes a required argument of a category name, such as MANBOT DISABLE KPOP, to disable or enable that category.", inline=False)
        embedVar.add_field(name="MANBOT MY CATEGORIES", value="View the categories you have enabled and disabled for when you call the manbot random roulette.", inline=False)
        embedVar.add_field(name="MANBOT FAVES", value="View a gallery of your favorite images. React to any manbot image to add it to your favorites list. ", inline=False)
        embedVar.add_field(name="MANBOT STATS", value="View Manbot's top ten most popular men, as well as Manbot's most recently added man. Call your favorite man a lot of times to try and get him on the leaderboard! This command takes an optional man name argument, e.g. MANBOT STATS WANG YIBO, to see that man's individual stats and information.", inline=False)
        embedVar.add_field(name="MANBOT MY STATS", value="View your individual stats.", inline=False)
        embedVar.add_field(name="MANBOT SLEEP", value="Have Manbot send a bedtime reminder.", inline=False)
        embedVar.add_field(name="MANBOT WORK", value="Have Manbot send a work time reminder.", inline=False)
        embedVar.add_field(name="MANBOT ERASE MY DATA", value="Erase ALL your Manbot data (this action cannot be undone!)", inline=False)
        embedVar.set_author(name="el's manbot", icon_url=manbotIcon)
        embedVar.set_footer(text="UPDATE 7 AUG 2021: Men can be disabled and enabled for users' individual manbot random roulettes on a category-by-category basis. Tired of anime in the random roulette? Don't want to see kpop? Disable it!")
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
                serverId = reaction.message.guild.id
                data[myId] = []
                data[myId].append({"favorites":[]})
                if fave != "":
                  data[myId][0]["favorites"].append(fave)
                data[myId].append({"call tracker":[]})
                data[myId].append({"servers":[]})
                data[myId].append({"handles":[]})
                temp = manbotUsers
                temp.update(data)
                temp[myId][2]["servers"].append(str(serverId))
                with open('users.json', 'w') as outfile:
                  json.dump(temp, outfile)
                  return

client.run(os.getenv('TOKEN'))
