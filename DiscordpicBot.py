#!/usr/bin/env python3

# ircecho.py
# Copyright (C) 2011 : Robert L Szkutak II - http://robertszkutak.com
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import sys
import socket
import string
import random
import time
import select
import discord
import asyncio
from googleapiclient.discovery import build
import pprint

my_api_key = "<google-api-key>"
my_cse_id = "<cse-id>"

def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res['items']

def searchimage(key):
    try:
        results = google_search(key, my_api_key, my_cse_id, searchType="image", safe="off")
        retur = []
        for result in results:
            retur.append(result["link"])
        pic = retur[random.randrange(0, len(retur) - 1)]
        return pic
    except:
        return "Something weird happened there... Check the API key."

def cleanup(file):
    openfile = open(file, 'r')
    contents = openfile.readlines()
    num = 0
    oldnum = 0
    try:
        for line in contents:
            if num != 0:
                if line[0] != num:
                    if line[0].isnumeric() == False:
                        line = ''
                    print(line[0])
            num += 1
    except:
        pass
    try:
        for line in contents:
            for chunk in line.split():
                if num != 0:
                    if chunk != num:
                        if chunk == oldnum:
                            line == ''
                        print(chunk)
                try:
                    oldnum = chunk
                    num = num + 1
                except:
                    pass
    except:
        pass
    try:
        for worthless in range(0, len(contents)):
            try:
                contents.remove('')
            except:
                pass
    except:
        pass
    openfile.close()
    openfile = open(file, 'w')
    newcontents = ''
    for line in contents:
        newcontents += line
    openfile.write(newcontents)

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
            pict = openfile.readline()
        openfile.close()
        if "nsfw" not in pict.lower():
            show = 1
        if str(idnum) == pict.replace('\n', ''):
            show = 1
        if len(pict.split()) == 1:
            return pic(channel)
        if show == 1:
            break
    return pict

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

def rolldice(time, dice):
    if int(time) == 1:
        return random.randrange(1, int(dice))
    else:
        return random.randrange(1, int(dice)) + rolldice(int(time) - 1, dice)
def printall():
    openfile = open("pictures.txt", 'r')
    contents = openfile.readlines()
    return contents

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
    elif message.content.startswith('!roll'):
        dcon = message.content[6:].split('d')
        await client.send_message(message.channel, rolldice(dcon[0], dcon[1]))
    elif message.content.startswith('!simage'):
        await client.send_message(message.channel, searchimage(message.content[8:]))
    elif message.content.startswith('!website'):
        website(message.content[9:])
    elif message.content.startswith('!printall'):
        await client.send_message(message.channel, "Please type the following: !Confirmation") #This is just to make sure someone didn't type the message by accident and cause the bot to spam.
    elif message.content.startswith("!Confirmation"):
        content = printall()
        for items in content:
            try:
                await client.send_message(message.channel, items)
                time.sleep(3)
            except:
                time.sleep(1)
        
while True:
    try:
        client.run('<DISCORD TOKEN>')
    except ConnectionResetError:
        print("reconnect")
    except Exception as error:
        print(error)
        client.close()
