import os
import discord
import json
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TOKEN')

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

#this command calls up your balance

@bot.command(name = "balance")
async def balance(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()

    coinpurse_amt = users[str(user.id)]["coinpurse"]
    bank_amt = users[str(user.id)]["bank"]

    em = discord.Embed(title = f"{ctx.author.name}'s balance",color = discord.Color.green())
    em.add_field(name = "Coinpurse",value = coinpurse_amt)
    em.add_field(name = "Bank",value = bank_amt)
    await ctx.send(embed = em)

#this command donates 10 gold to your coinpurse

@bot.command(name = "donate")
async def donate(ctx):
    await open_account(ctx.author)

    user = ctx.author
    users = await get_bank_data()

    earnings = 10

    await ctx.send(f"Someone donated {earnings} monies")

    users[str(user.id)]["coinpurse"] += earnings

    with open("bank.json", "w") as f:
        json.dump(users,f)


#this function creates a new account

async def open_account(user):
    with open("bank.json", "r") as f:
        users = json.load(f)

    if str(user.id) in users:
        return False
    else:
        
        users[str(user.id)] = {}
        users[str(user.id)]["coinpurse"] = 0
        users[str(user.id)]["bank"] = 0
        
    with open("bank.json", "w") as f:
        json.dump(users,f)
    return True

async def get_bank_data():
    with open("bank.json", "r") as f:
        users = json.load(f)

    return users 

#retrieves bot token from .env
bot.run(TOKEN)
