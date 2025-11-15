import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive

from discord.ext import commands
from discord import app_commands
import youtube_dl
import asyncio
import json
import os

DATA_FILE = "data.json"

# sad_words = [
#     "sad", "depressed", "unhappy", "angry", "miserable", "depressing",
#     "heartbroken", "upset", " bad ", "worried", "sorry", "dissapointed",
#     "shoot my head", "cut my life into pieces", "kill me", "suicide", 
#     "my dick is small", "i want to die", "suicidal"
# ]
sad_words = [
    "sad", "depressed", "unhappy", "angry", "miserable", "depressing",
    "heartbroken", "upset", " bad ", "worried", "sorry", "dissapointed", 
    "shoot my head", "cut my life into pieces", "kill me", "suicide", 
    "my dick is small", "i want to die", "suicidal", "feel like shit", "gloomy",
    "melancholy", "dispirited", "low-spirited", "somber", "slightly upset", "sorrowful", 
    "dejected", "despondent", "miserable", "wretched", "heavy-hearted", "morose", 
    "crestfallen", "grief-stricken", "devastated", "bereaved", "desolate",       
    "anguished", "tormented", "dismayed", "despairing", "crushed",   "overwhelmed", "kill myself", "kms"
]

mean_words = ["shut up", "fuck off", "fuck you", "fuck"]

starter_encouragements = [
    "Cheer up!", "Hang in there.", "You are a great person"
]

# if "responding" not in db.keys():
#     db["responding"] = True

def load_data():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump({"responding": True, "encouragements": []}, f)
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return (quote)


# def update_encouragements(encouraging_message):
#     if "encouragements" in db.keys():
#         encouragements = data["encouragements"]
#         encouragements.append(encouraging_message)
#         data["encouragements"] = encouragements
#     else:
#         data["encouragements"] = [encouraging_message]
def update_encouragements(encouraging_message):
    data = load_data()
    data["encouragements"].append(encouraging_message)
    save_data(data)


# def delete_encouragement(index):
#     encouragements = data["encouragements"]
#     if len(encouragements) > index:
#         del encouragements[index]
#         data["encouragements"] = encouragements
def delete_encouragement(index):
    data = load_data()
    if index < len(data["encouragements"]):
        del data["encouragements"][index]
    save_data(data)

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
# data = load_data()

@client.event
async def on_ready():
    await tree.sync()
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    global data
    if message.author == client.user:
        return

    data = load_data()
    msg = message.content
    
    if msg == '/test':
        await message.channel.send('ping pong!')
        
    if data["responding"]:
        options = starter_encouragements
        if "encouragements" in data:
            options = options + data["encouragements"]

        if any(word in msg.lower() for word in sad_words):
            await message.channel.send(random.choice(options))

        if any(word in msg.lower() for word in mean_words):
            await message.channel.send("That's not very nice " + message.author.mention)

    if msg.startswith("/new"):
        encouraging_message = msg.split("/new ", 1)[1]
        update_encouragements(encouraging_message)
        await message.channel.send("New encouraging message added.")

    if msg.startswith("/del"):
        encouragements = []
        if "encouragements" in data:
            index = int(msg.split("!del", 1)[1])
            delete_encouragement(index)
            encouragements = data["encouragements"]
        await message.channel.send(encouragements)

    if msg.startswith("/list"):
        encouragements = []
        if "encouragements" in data:
            encouragements = data["encouragements"]
        await message.channel.send(encouragements)

    if msg.startswith("/responding"):
        value = msg.split("!responding ", 1)[1]
        data = load_data()
        data["responding"] = (value.lower() == "true")
        save_data(data)
    
        await message.channel.send(f"Responding is now {data['responding']}.")
        # if value.lower() == "true":
        #     data["responding"] = True
        #     await message.channel.send("Responding is on.")
        # else:
        #     data["responding"] = False
        #     await message.channel.send("Responding is off.")
    

@tree.command()
async def slash(interaction: discord.Interaction, number: int, string: str):
    await interaction.response.send_message(f'{number=} {string=}', ephemeral=True)
  


@tree.command(name = "quote", description = "Generate a random quote")
async def quote(interaction: discord.Interaction):
    quote = get_quote()
    await interaction.response.send_message(quote, ephemeral=False)


@tree.command(name = "dm", description = "Send a personal message to a user")
async def dm(interaction: discord.Interaction, member: discord.Member, *, message: str):
    await member.send(message)
    await interaction.response.send_message(":white_check_mark: Sent!")


@tree.command(name = "help", description = "Help Box")
async def help(interaction: discord.Interaction):
    embed = discord.Embed(title="Help Box",
                          description="Command lines that might work")
    embed.set_thumbnail(url="https://i.imgur.com/9wkETOh.jpeg")
    embed.set_image(
        url=
        "https://i.pinimg.com/originals/73/76/34/73763429c9f1adcdf7512338edecdad1.jpg"
    )
    embed.add_field(name="/quote",
                    value="gives you a random quote",
                    inline=False)
    embed.add_field(name="if you say sad, depressed things",
                    value="Bot will try to cheer you up",
                    inline=False)
    embed.add_field(name="/new [quote]",
                    value="Add inspiring quotes",
                    inline=False)
    embed.add_field(name="/del [index]",
                    value="Delete inspiring quotes",
                    inline=False)
    embed.add_field(name="/list ",
                    value="see all added inspiring quotes",
                    inline=False)
    embed.add_field(name="/dm @user <message>",
                   value="Personally message a user",
                   inline=False)
    embed.set_footer(
        text=
        "Hope it works, you can add new inspiring quotes by using /new [quote]"
    )
    await interaction.response.send_message(embed=embed)

keep_alive()
client.run(os.environ['TOKEN'])

# while __name__ == '__main__':
#   try:
#     keep_alive()
#     client.run(os.environ['TOKEN'])
#   except discord.errors.HTTPException as e:
#     print(e)
#     print("\n\n\nBLOCKED BY RATE LIMITS\nRESTARTING NOW\n\n\n")
#     os.system('kill 1')
