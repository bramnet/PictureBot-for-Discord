import sys
import socket
import string
import random
import time
import select
import discord
import asyncio

def pic(channel):
    if channel == 'general':
        show = 0
    else:
        show = 1
    while True:
        openfile = open("picturesnum.txt", 'r')
        idnum = int(openfile.readline())
        openfile.close()
        picid = int(random.randrange(1, idnum + 1))
        openfile = open("pictures.txt", 'r')
        for i in range(0, picid + 1):
            pic = openfile.readline()
        openfile.close()
        if "nsfw" not in pic.lower():
            show = 1
        if str(idnum) == pic.replace('\n', ''):
            show = 1
        if show == 1:
            break
    return pic

def add(link, user):
    openfile = open("picturesnum.txt", 'r')
    idnum = int(openfile.readline())
    idnum = idnum + 1
    openfile.close()
    openfile = open("pictures.txt", 'a')
    savmsg = str(link) + " | " + str(user)
    store = str("\n" + str(idnum) + " " + savmsg)
    openfile.write(store)
    openfile.close()
    sendmsg = "Saved, ID = " + str(idnum)
    openfile = open("picturesnum.txt", 'w')
    openfile.write(str(idnum))
    openfile.close()
    return sendmsg

def idreturn(idcode, channel):
    if channel == 'general':
        show = 0
    else:
        show = 1
    openfile = open("pictures.txt", 'r')
    for i in range(0, int(idcode) + 1):
        pic = openfile.readline()
    openfile.close()
    if "nsfw" not in pic.lower():
        show = 1
    if show != 1:
        return "I'm sorry, but I can't show this in this channel"
    if str(idcode) == pic.replace('\n', ''):
        return "Well, I'm sorry to say this, be we don't have that anymore. Try adding it again if you happen to have it"
    return pic

def tag(tagger, channel):
    if channel == 'general':
        if tagger.lower() == 'nsfw':
            return "I'm sorry, but I can't show NSFW images in this channel"
        show = 0
    else:
        show = 1
    openfile = open("picturesnum.txt", 'r')
    idnum = int(openfile.readline())
    openfile.close()
    truth = 0
    taglist = []
    openfile = open("pictures.txt", 'r')
    for i in range(0, idnum + 1):
        fileline = openfile.readline()
        test = fileline.lower().count(tagger.lower())
        if test != 0:
            taglist.append(fileline)
            test = 0
        elif fileline == '':
            openfile.close()
    while True:
        pic = taglist[random.randrange(0, len(taglist) - 1)]
        if "nsfw" not in pic.lower():
            show = 1
        if str(idnum) == pic.replace('\n', ''):
            show == 1
        if show == 1:
            break
    return pic
def syscheck():
    openfile = open("picturesnum.txt", 'r')
    idnum = int(openfile.readline())
    openfile.close()
    openfile = open("pictures.txt", 'r')
    i = 0
    for i in range(0, idnum + 1):
        fileline = openfile.readline()
        check = fileline.split()
        if i != 0:
            if int(check[0]) != i:
                return "We have a problem at " + str(i)
    return "Everything's good, captain!"
def delete(num):
    openfile = open("picturesnum.txt", 'r')
    idnum = int(openfile.readline())
    openfile.close()
    openfile = open("pictures.txt", 'r')
    content = openfile.readlines()
    content[int(num)] = str(num) + '\n'
    openfile.close()
    openfile = open("pictures.txt", "w")
    openfile.write('')
    openfile.close()
    openfile = open("pictures.txt", 'a')
    for link in content:
        openfile.write(link)
    return str(num) + ' has now been deleted'

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    if message.content.startswith('!test'):
        counter = 0
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        async for log in client.logs_from(message.channel, limit=100):
            if log.author == message.author:
                counter += 1

        await client.edit_message(tmp, 'You have {} messages.'.format(counter))
    elif message.content.startswith('!sleep'):
        await asyncio.sleep(5)
        await client.send_message(message.channel, 'Done sleeping')

    elif message.content.lower().startswith('!pic'):
        await client.send_message(message.channel, pic(str(message.channel)))

    elif message.content.lower().startswith('!add'):
        if(message.attachments == []):
            await client.send_message(message.channel, add(message.content[5:], message.author))
        else:
            content = message.attachments[0]
            await client.send_message(message.channel, add(str(content['url'] + " " + message.content[5:]), message.author))

    elif message.content.lower().startswith('!id'):
        await client.send_message(message.channel, idreturn(message.content[4:], str(message.channel)))

    elif message.content.lower().startswith('!tag'):
        await client.send_message(message.channel, tag(message.content[5:], str(message.channel)))
        
    elif message.content.startswith('!systemcheck'):
        await client.send_message(message.channel, syscheck())

    elif message.content.startswith('!del'):
        await client.send_message(message.channel, delete(message.content[5:]))


        
while True:
    try:
        client.run('<DISCORD TOKEN>')
    except ConnectionResetError:
        print("reconnect")
    except Exception as error:
        print(error)
        client.close()
