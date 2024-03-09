import discord
import streamlit as st
import gspread
import google.generativeai as genai
from discord import app_commands
from discord.ext import commands, tasks
from variables import var, vararray, ans
from pathlib import Path
import time
from time import sleep

genai.configure(api_key="AIzaSyDssvAqJ-icp8QyxCQNGlSlU623sQzTQps")
channel_id = 1215575801966108698
model = genai.GenerativeModel(model_name="gemini-pro")
list = str(var)
taskarray = vararray
anskey = str(ans)
file_path = Path("variables.py")
gc = gspread.service_account(filename='serviceAuth.json')
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
TOKEN = st.secrets["TOKEN"]

def count(string1, string2):
  common_count = sum(char1 == char2 for char1, char2 in zip(string1, string2))
  return common_count

@bot.event
async def on_ready():
  print("Bot is Up and Ready!")
  try:
    synced = await bot.tree.sync()
    print(f"Synced {len(synced)} command(s)")
  except Exception as e:
    print(e)
  t = time.localtime()
  current_time = time.strftime("%H:%M:%S", t)
  check.start()

@tasks.loop(minutes=60)
async def check():
  t = time.localtime()
  current_hour = time.strftime("%H", t)
  current_min = time.strftime("%M", t)
  if (current_hour=="12" and current_min>=30) or (current_hour=="13" and current_min<=30):
    channel = bot.get_channel(channel_id)
    if channel:
      array = ["B1", "B2", "B3", "B4", "B5", "B6" ,"B7"]
      for x in array:
        for task in taskarray:
          wks = gc.open(task).sheet1
          progress = str(wks.get(x))
          val = progress[3:-3]
          if x == "B1" and val != "Complete":
            await channel.send(f"Harshit has not completed task {task}")
          if x == "B2" and val != "Complete":
            await channel.send(f"Shivansh has not completed task {task}")
          if x == "B3" and val != "Complete":
            await channel.send(f"Tushar has not completed task {task}")
          if x == "B4" and val != "Complete":
            await channel.send(f"Kalp has not completed task {task}")
          if x == "B5" and val != "Complete":
            await channel.send(f"Arpit has not completed task {task}")
          if x == "B6" and val != "Complete":
            await channel.send(f"Avneet has not completed task {task}")
          if x == "B7" and val != "Complete":
            await channel.send(f"Sasmit has not completed task {task}")
    else:
      print("Channel not found.")

@bot.tree.command(name="hello")
async def hello(interaction: discord.Interaction):
  await interaction.response.send_message(f"Hey {interaction.user.mention}! This is a slash command!", ephemeral=False)

@bot.tree.command(name="say")
@app_commands.describe(thing_to_say="What should I say?")
async def say(interaction: discord.Interaction, thing_to_say: str):
  await interaction.response.send_message(f"{interaction.user.name} said: `{thing_to_say}`")

@bot.tree.command(name="task")
@app_commands.describe(option="list or create")
@app_commands.describe(name="name of task to create")
async def say(interaction: discord.Interaction, option: str, name: str=None):
  global list
  global taskarray
  if option == "list":
    await interaction.response.send_message(f"Name of tasks are : {list}")
  if option == "create":
    await interaction.response.defer()
    wks1 = gc.open(name)
    if wks1:
      await interaction.followup.send(f"{name} task has already been created")
    else:
      wks = gc.create(name)
      list = list + "\n" + name
      taskarray.append(name)
      file_path.unlink()
      with open("variables.py", mode="w") as file:
        file.write(f"""var = \"\"\"{list}\"\"\"""")
        file.write(f"""\nvararray = {taskarray}""")
        file.write(f"""\nans = {anskey}""")
      await interaction.followup.send(f"{name} task has been created")

@bot.tree.command(name="update")
@app_commands.describe(task="name of task")
@app_commands.describe(label="Complete, Pending etc.")
async def say(interaction: discord.Interaction, task: str, label: str):
  await interaction.response.defer()
  wks = gc.open(f"{task}").sheet1
  if (interaction.user.name) == "proharshit.":
    wks.update([['Harshit', label]], 'A1')
    await interaction.followup.send(f"{task} has been updated to state {label}")
  if (interaction.user.name) == "ignoreme_sg":
    wks.update([['Shivansh', label]], 'A2')
    await interaction.followup.send(f"{task} has been updated to state {label}")
  if (interaction.user.name) == "Tapster1510":
    wks.update([['Tushar', label]], 'A3')
    await interaction.followup.send(f"{task} has been updated to state {label}")
  if (interaction.user.name) == "helldevil69":
    wks.update([['Kalp', label]], 'A4')
    await interaction.followup.send(f"{task} has been updated to state {label}")
  if (interaction.user.name) == "":
    wks.update([['Arpit', label]], 'A5')
    await interaction.followup.send(f"{task} has been updated to state {label}")
  if (interaction.user.name) == "beluga06660":
    wks.update([['Avneet', label]], 'A6')
    await interaction.followup.send(f"{task} has been updated to state {label}")
  if (interaction.user.name) == "sasmit0509":
    wks.update([['Sasmit', label]], 'A7')
    await interaction.followup.send(f"{task} has been updated to state {label}")

@bot.tree.command(name="progress")
@app_commands.describe(task="name of task")
@app_commands.describe(user="name of user to check")
async def say(interaction: discord.Interaction, task: str, user: str):
  await interaction.response.defer()
  wks = gc.open(task).sheet1
  if user == "Harshit":
    progress = str(wks.get('B1'))
    val = progress[3:-3]
    await interaction.followup.send(f"{user} has completed task till state {val}")
  if user == "Shivansh":
    progress = str(wks.get('B2'))
    val = progress[3:-3]
    await interaction.followup.send(f"{user} has completed task till state {val}")
  if user == "Tushar":
    progress = str(wks.get('B3'))
    val = progress[3:-3]
    await interaction.followup.send(f"{user} has completed task till state {val}")
  if user == "Kalp":
    progress = str(wks.get('B4'))
    val = progress[3:-3]
    await interaction.followup.send(f"{user} has completed task till state {val}")
  if user == "Arpit":
    progress = str(wks.get('B5'))
    val = progress[3:-3]
    await interaction.followup.send(f"{user} has completed task till state {val}")
  if user == "Avneet":
    progress = str(wks.get('B6'))
    val = progress[3:-3]
    await interaction.followup.send(f"{user} has completed task till state {val}")
  if user == "Sasmit":
    progress = str(wks.get('B7'))
    val = progress[3:-3]
    await interaction.followup.send(f"{user} has completed task till state {val}")

@bot.tree.command(name="chat")
@app_commands.describe(ques="Question which you want to ask")
async def say(interaction: discord.Interaction, ques: str):
  await interaction.response.defer()
  response = model.generate_content(f"Answer the question {ques}")
  await interaction.followup.send("Answer is \n : " + response.text)

@bot.tree.command(name="key")
@app_commands.describe(key="Type the answer key")
async def say(interaction: discord.Interaction, key :str):
  await interaction.response.defer()
  global anskey
  if interaction.user.name=="proharshit.":
    key1 = key.replace(" ","")
    anskey = key1.lower()
    file_path.unlink()
    with open("variables.py", mode="w") as file:
      file.write(f"""var = \"\"\"..{list}\"\"\"""")
      file.write(f"""\nvararray = {taskarray}""")
      file.write(f"""\nans = \"\"\"{anskey}\"\"\"""")
    await interaction.followup.send("Answer key has been set")

@bot.tree.command(name="smts")
@app_commands.describe(answers="Type the letters of appropriate options without spaces")
async def say(interaction: discord.Interaction, answers :str):
  await interaction.response.defer()
  wks1 = gc.open("smts").sheet1
  if (interaction.user.name) == "proharshit.":
    wks1.update([['Harshit', answers]], 'A1')
    await interaction.followup.send(str(wks1.get('B1')))
    await interaction.followup.send(f"{interaction.user.mention } has submitted the test")
  if (interaction.user.name) == "ignoreme_sg":
    wks1.update([['Shivansh', answers]], 'A2')
    await interaction.followup.send(f"{interaction.user.mention } has submitted the test")
  if (interaction.user.name) == "Tapster1510":
    wks1.update([['Tushar', answers]], 'A3')
    await interaction.followup.send(f"{interaction.user.mention } has submitted the test")
  if (interaction.user.name) == "helldevil69":
    wks1.update([['Kalp', answers]], 'A4')
    await interaction.followup.send(f"{interaction.user.mention } has submitted the test")
  if (interaction.user.name) == "nemesis_killedrse3":
    wks1.update([['Arpit', answers]], 'A5')
    await interaction.followup.send(f"{interaction.user.mention } has submitted the test")
  if (interaction.user.name) == "beluga06660":
    wks1.update([['Avneet', answers]], 'A6')
    await interaction.followup.send(f"{interaction.user.mention } has submitted the test")
  if (interaction.user.name) == "sasmit0509":
    wks1.update([['Sasmit', answers]], 'A7')
    await interaction.followup.send(f"{interaction.user.mention } has submitted the test")

@bot.tree.command(name="evaluate")
async def say(interaction: discord.Interaction):
  await interaction.response.defer()
  wks2 = gc.open("smts").sheet1
  cell = ["B1","B2","B3","B4","B5","B6","B7"]
  cells1 = ["C1","C2","C3","C4","C5","C6","C7"]
  names = ["Harshit","Shivansh","Tushar","Kalp","Arpit","Avneet","Sasmit"]
  await interaction.followup.send(str(wks2.get('C1'))) 
  for n in range(7):
    x = cell[n]
    cell1 = cells1[n]
    value = str(wks2.get(x)) 
    val2 = value[3:-3]
    val3 = val2.lower()
    val1 = val3.replace(" ","")
    scores = count(val1,anskey)
    wks2.update([[scores,'']], cell1)
    name = names[n]
    value1 = str(wks2.get(cell1))
    print(value1[3:-3])
    await interaction.followup.send(f"{name} has scored {value1[3:-3]}")

bot.run(TOKEN)
