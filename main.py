import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
BAD_WORDS = {"shit", "fuck", "bitch"}



load_dotenv()
token = os.getenv('DISCORD_TOKEN')
if not token:
    raise ValueError("DISCORD_TOKEN not found. Create a .env file with DISCORD_TOKEN=...")


handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
discord_role = "Agent"
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f"Let's get in, {bot.user.name}")

@bot.event
async def on_member_join(member):
    await member.send(f"Welcome to Gengu, {member.name}龍神の剣を喰らえ")

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    content = message.content.lower()
    words = content.split()
    if any(word in BAD_WORDS for word in words):
        try:
            await message.delete()
        except discord.Forbidden:
            await message.channel.send("I need permission to delete this Message!")
        await message.channel.send(f"{message.author.mention} - dont use dirty word")
    await bot.process_commands(message)


@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.mention}!")

@bot.command()
async def assign(ctx):
    role = discord.utils.get(ctx.guild.roles, name = discord_role)
    if role:
        await ctx.author.add_roles(role)
        await ctx.send(f"{ctx.author.mention} is now assigned to {discord_role}")
    else:
        await ctx.send("Role doesn't exist!")

@bot.command()
async def remove(ctx):
    role = discord.utils.get(ctx.guild.roles, name = discord_role)
    if role:
        await ctx.author.remove_roles(role)
        await ctx.send(f"{ctx.author.mention} has had the {discord_role} role removed!")
    else:
        await ctx.send("Role doesn't exist!")


@bot.command()
@commands.has_role(discord_role)
async def agent(ctx):
    await ctx.send("Welcome to the server!")

@agent.error
async def agent_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("You do not have permission to do that!")

@bot.command()
async def dm(ctx, *, msg):
    await ctx.author.send(f"You said {msg}")

@bot.command()
async def reply(ctx):
    await ctx.reply("This is a reply!")

@bot.command()
async def poll(ctx, *, question):
    embed = discord.Embed(title = "New Poll", description=question)
    poll_message = await ctx.send(embed = embed)
    await poll_message.add_reaction("👍")
    await poll_message.add_reaction("👎")

try:
    bot.run(token, log_handler=handler, log_level=logging.DEBUG)
finally:
    print("Shutting down Bot...")

