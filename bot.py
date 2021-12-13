import discord
import asyncio
from discord.ext import commands
import firebase_admin
from firebase_admin import credentials, firestore, initialize_app
from snapshot import get_holders
import requests as r

firebaseConfig = "ADDCONFIG"


cred = credentials.Certificate(firebaseConfig)
app = initialize_app(cred, {})
db = firestore.client()

DISCORD_BOT_TOKEN = "ADD_BOT_TOKEN"

GUILD_ID = "ADD GUILD ID AS INT"

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix="s!", intents=intents)

@bot.command()
async def verify(ctx):
    try:
        docs = db.collection(u'verify').where(u'discord_userid', u'==', ctx.message.author.id).stream()
        wallet = []
        for doc in docs:
            wallet += [doc.id]
            if(doc.to_dict()['verify']):
                embed_channel = discord.Embed(title="You've already been verified!", description = "Please check your DMs for further information. In case of any queries, please contact the admin.", color=0xe67e22)
                embed_author = discord.Embed(title="You've already been verified!", description="Your Discord profile has already been matched with\nWallet Address : " + doc.id + "\nIf you think this is a mistake, contact one of the admins of Fantom Boy.", color=0xe67e22)
                await ctx.channel.send(embed=embed_channel)
                await ctx.author.send(embed=embed_author)
            else:
                embed_channel = discord.Embed(title="Looks like you started the verification but didn't complete it.", description = "Please check your DMs!", color=0xe67e22)
                #embed_author = discord.Embed(title="Get verified now!", description="Please verify yourself using the link below!", color=0xe67e22)
                await ctx.channel.send(embed=embed_channel)
                #await ctx.author.send(embed=embed_author)
                await ctx.author.send("Thank you for sharing your wallet address! Please use the link below to complete your verification")
                await ctx.author.send("http://localhost:3000")

        if(len(wallet)==0):
            embed_channel = discord.Embed(title="Your Verification has been started!", description = "Please check your DMs to continue with verification.", color=0xe67e22)
            embed_author = discord.Embed(title="Thank you for starting your verification.", description="Please enter your Metamask Wallet address!", color=0xe67e22)
            await ctx.channel.send(embed=embed_channel)
            await ctx.author.send(embed=embed_author)
    except Exception as e:
        print(e)

@bot.command()
async def sroles(ctx):
    try:
        holders_address = get_holders()
        discord_ids = []
        print(holders_address)
        verified_users = db.collection(u'verify')
        docs = verified_users.stream()

        for doc in docs:
            if((doc.id.lower() in holders_address) and (doc.to_dict()['verify'])):
                discord_ids += [doc.to_dict()['discord_userid']]

        guild = bot.get_guild(GUILD_ID)
        print(guild)

        role = discord.utils.get(guild.roles, name="Holder")
        members = guild.members
        print(members)
        i=0
        for member in members:
            try:
                print(member.id)
                i+=1
                print(i)
                if(member.id in discord_ids):
                    print("AR", member.name)
                    await member.add_roles(role)
                elif(member.id not in discord_ids and role in member.roles):
                    print("RR", member.name)
                    await member.remove_roles(role)
            except:
                continue

        embed = discord.Embed(title="Snapshot Successfully Taken!", description="All current holders have received the role!", color=0xe67e22)
        await ctx.channel.send(embed=embed)

    except Exception as e:
        print(e)


@bot.command()
async def info(ctx):
    try:
        embed = discord.Embed(title="Stonkify Bot - Your Friendly Verification Bot", description = "Allows you to verify yourself to be able to participate in DAO voting process!")
        embed.add_field(name="Author", value="rahulkumaran#9892", inline=False)
        embed.add_field(name="You can tip me if you like my work!", value="Wallet Address : 0xFf4D2C8e588b0307B7C0Cd19BAb220EC7F5873E8", inline=False)
        await ctx.channel.send(embed=embed)
    except Exception as e:
        print(e)

@bot.remove_command("help")

@bot.command()
async def help(ctx):
	'''
	Gives the list and highlights
	of what each bot command does
	'''
	embed = discord.Embed(title="Stonkify Bot - A Friendly Verification Tool", description = "Allows you to verify yourself to be able to participate in DAO voting process!")
	embed.add_field(name="s!verify", value="This command allows you to get verified!", inline=False)
	embed.add_field(name="s!info", value="Gives a information about the bot", inline=False)
	embed.add_field(name="s!help", value="Gives a list of commands available with the bot", inline=False)
	await ctx.channel.send(embed=embed)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.channel.send("Please check the command you entered!")

@bot.event
async def on_message(message):
    if((message.content.startswith("0x")) and (str(message.channel)[0:20]=='Direct Message with ')):
        user_name = message.author.name
        user_id = message.author.id
        data = {
            u'discord_username': user_name,
            u'discord_userid' : user_id,
            u'verify' : False
        }
        db.collection(u'verify').document(message.content).set(data)
        #embed_author = discord.Embed(title="Get verified now!", description="Use the link below to complete your verification!", color=0xe67e22)
        await message.author.send("Thank you for sharing your wallet address! Please use the link below to complete your verification")
        await message.author.send("http://localhost:3000")
    await bot.process_commands(message)

if(__name__=='__main__'):
    bot.run(DISCORD_BOT_TOKEN)
