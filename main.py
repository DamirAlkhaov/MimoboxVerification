import discord
import os
import requests
import json
from discord.ext import commands
from datetime import datetime
import string
import random
from discord.utils import get
from ping import ping


bot = commands.Bot(command_prefix="mv!")

async def getinfoByUser(ctx, username, onlyUSername=False):
  url = os.getenv("GetDesc") + username
  response = requests.get(url)
  json_Data = json.loads(response.text)
  if 'description' in json_Data and not onlyUSername:
    code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
    code = "mv>" + code
    # Add embed 
    embed = discord.Embed(title="Add Code to Description in order to Verify!", description = "You have 5 minutes in order to add the given code in your MimoBox User Description!\nWhen done type 'Done'.", color = discord.Colour.green())
    #Add code field
    embed.add_field(name="Code: ", value=code, inline = True)
    #Add Footer to Embed
    embed.set_footer(text='Request by: ' + ctx.message.author.name + ' | ' +
                         str(datetime.now()),
                         icon_url=ctx.message.author.avatar_url)
    await ctx.send(embed=embed)
    return(code)
  elif 'description in json_Data' and onlyUSername:
    return(json_Data['description'], json_Data['user'])
  elif 'status' in json_Data:
    embed = discord.Embed(title = "Error "+json_Data['status'] , description = json_Data['message'], color = discord.Colour.red())
    await ctx.send(embed=embed)
    


@bot.event
async def on_ready():
    print('online!')
    game = discord.Game("mv!info")
    await bot.change_presence(status=discord.Status.online, activity=game)

@bot.command()
async def verify(ctx, *,username):
    member = ctx.message.author
    server = ctx.message.guild
    role = get(server.roles, name="verified")
    if not role in member.roles:
      # Gets the generated Code
      code = await getinfoByUser(ctx, username)
      if code:
        #wait for user to say done when he says done, make it send another request and if it right give him verified role and nickname if its wrong tell the user to try again.
        
        msg = await bot.wait_for('message',timeout=300.00, check=lambda message: message.author == ctx.author and message.content == "Done")
        if msg:
          
          description, username = await getinfoByUser(ctx, username, onlyUSername = True)
          if code in description:
            embed = discord.Embed(title = "Verification Success", description = "You have been verified!", color = discord.Colour.green())
            await ctx.send(embed=embed)
            #addes verified Role
            await member.add_roles(role)
            await member.edit(nick=username)
          else:
            embed = discord.Embed(title = "Verification Error", description = "Please try again!", color = discord.Colour.red())
            await ctx.send(embed=embed)

      else:
        return
    else:
      embed = discord.Embed(title = "Already Verified", description = "If you want to verify again please use mv!unverify", color = discord.Colour.red())
      await ctx.send(embed=embed)
@bot.command()
async def unverify(ctx):
  member = ctx.message.author
  server = ctx.message.guild
  role = get(server.roles, name="verified")
  if role in member.roles:
    await member.remove_roles(role)
    
    embed = discord.Embed(title = "Successfully Unverified!", description = "You have successfully unverified your account!", color = discord.Colour.green())
    await ctx.send(embed=embed)
    await member.edit(nick=False)
  else:
    embed = discord.Embed(title = "Not Verified", description = "First verify in order to unverify, using the mv!verify command.", color = discord.Colour.red())
    await ctx.send(embed=embed)
    
@bot.command()
async def info(ctx):
  embed = discord.Embed(title = "Info", description = "Info about the MimoBox Verification Bot", color=discord.Colour.green())
  
  embed.add_field(name="Commands: ", value="mv!verify - verifies a User by giving them a code to add to their description.\nmv!unverify - unverifies a user(if already verified)", inline = True)

  await ctx.send(embed=embed)
ping()
bot.run(os.getenv("TOKEN"))
# Code written and made by Damir and is the property of MimoBox™