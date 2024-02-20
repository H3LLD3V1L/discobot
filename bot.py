import discord
from discord import app_commands
from discord.ext import commands
import gspread

gc = gspread.service_account(filename='/storage/emulated/0/serviceAuth.json')
bot = commands.Bot(command_prefix="!", intents = discord.Intents.all())

list = ""
@bot.event
async def on_ready():
    print("Bot is Up and Ready!")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

@bot.tree.command(name="hello")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hey {interaction.user.mention}! This is a slash command!" ,ephemeral=False)

@bot.tree.command(name="say")
@app_commands.describe(thing_to_say = "What should I say?")
async def say(interaction: discord.Interaction, thing_to_say: str):
    await interaction.response.send_message(f"{interaction.user.name} said: `{thing_to_say}`")

@bot.tree.command(name="task")
@app_commands.describe(option = "list or create")
@app_commands.describe(name = "name of task to create")
async def say(interaction: discord.Interaction, option: str, name: str=None):
  global list
  if option=="list":
    await interaction.response.send_message(f"Name of tasks are : {list}")
  if option=="create":
    await interaction.response.send_message(f"{name} task has been created")
    wks = gc.create(name)
    list = list + "\n"+ name

@bot.tree.command(name="update")
@app_commands.describe(task = "name of task")
@app_commands.describe(user = "name of user")
@app_commands.describe(label = "Complete, Pending etc.")
async def say(interaction: discord.Interaction, task: str, user: str, label: str):
  wks = gc.open(f"{task}").sheet1
  if user=="Harshit" and (interaction.user.name)=="proharshit.":
    wks.update('A1',[['Harshit',label]])
    await interaction.response.send_message(f"{task} has been updated to state {label}")

@bot.tree.command(name="progress")
@app_commands.describe(task = "name of task")
@app_commands.describe(user = "name of user to check")
async def say(interaction: discord.Interaction, task: str, user: str):
  wks = gc.open(task).sheet1
  if user=="Harshit":
    progress = str(wks.get('B1'))
    val = progress[3:-3]
    await interaction.response.send_message(f"{user} has completed task till state {val}")
    
bot.run("MTIwNjE3MTMyNTIyODUxNTQwOA.GwVW5B.wGjxAk9mHBn6SCnuo7RRCqith_FhGjOqMrTkpA")
