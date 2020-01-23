import asyncio
import datetime
import discord
from discord.ext import commands
import json
import os
import urllib.request
from discord import File
import glob

bot = commands.Bot(command_prefix='!')

id_to_username = {}

filename = "C:/projects/Slackord/export/users.json"
with open(filename, encoding='utf-8') as f:
    for user in json.load(f):
        required_fields_image = ["id", "name"]
        if all(x in user for x in required_fields_image):
            id_to_username[user["id"]] = user["name"]


# When !bort is typed in a channel, iterate through the JSON file and post each message.
@bot.command(pass_context=True)
async def bort(ctx):
    folder_name = "C:/projects/Slackord/export/av-workshop/"
    os.chdir(folder_name)
    # filename = "C:/projects/Slackord/export/adas-project/2019-09-04.json"
    for file in glob.glob("*.json"):
        filename = folder_name + file
        print("Processing " + filename)
        with open(filename, encoding='utf-8') as f:
            for message in json.load(f):
                # Images
                required_fields_image = ["files", "user", "ts"]
                if all(x in message for x in required_fields_image):
                    time = datetime.datetime.fromtimestamp(
                        float(message['ts'])).strftime('%Y-%m-%d %H:%M:%S')
                    rn = id_to_username[message['user']]
                    for uploaded_file in message["files"]:
                        pretty_type = str(uploaded_file["pretty_type"]).lower()

                        image_types = ["jpeg", "jpg", "png", "gif", "bmp", "pdf", "docx", "xlsx", "pptx", "txt", "md",
                                       "mp3"]
                        if not any(x in pretty_type for x in image_types):
                            continue
                        uploaded_filename = uploaded_file["name"]
                        url = uploaded_file["url_private"]
                        local_filename, headers = urllib.request.urlretrieve(url)

                        better_name = local_filename + "." + pretty_type
                        os.rename(local_filename, better_name)
                        local_filename = better_name

                        print("local_filename = " + local_filename)
                        messageToSend = time + " " + rn + " " + uploaded_filename
                        await ctx.send(content=messageToSend, file=File(local_filename))
                        print(messageToSend + " " + url)

                # Normal Messages
                required_fields_normal_message = ["user_profile", "ts", "text"]
                if all(x in message for x in required_fields_normal_message):
                    time = datetime.datetime.fromtimestamp(
                        float(message['ts'])).strftime('%Y-%m-%d %H:%M:%S')

                    rn = (message['user_profile']['real_name'])
                    mess = (message['text'])

                    if "attachments" in message:
                        for attachment in message["attachments"]:
                            mess += " " + attachment["fallback"]

                    messageToSend = (time) + (": ") + \
                                    (rn) + (" - ") + (mess)
                    await ctx.send(content=messageToSend)
                    print(messageToSend)


bot.run("NjY5NDg3ODA2NDE4MjU1ODk2.XinqGg.Ow6y7s7YmV5SCtmx1SSV83dwpYY")
