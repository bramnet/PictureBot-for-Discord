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
import requests
from googleapiclient.discovery import build
import pprint
from html.parser import HTMLParser
import urllib
import json
import io
import aiohttp

#Below is a little add-on for searching on google based on a keyword

my_api_key = "<Google API>"
my_cse_id = "<Google CSE ID>"

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
        return ">.>... So... Google had an issue with that... Not sure why, but if you get this error 2 times in a row, we might have gotten over our daily quota. 'Daily quotas reset at midnight Pacific Time (PT)'... Sorry ;-;"

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
    if channel == '<custom channel>':
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
        if "<custome tag>" not in pict.lower():
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
    if channel == '<Custom Channel>':
        show = 0
    else:
        show = 1
    openfile = open("pictures.txt", 'r')
    for i in range(0, int(idcode) + 1):
        pic = openfile.readline()
    openfile.close()
    if "<Custom Tag>" not in pic.lower():
        show = 1
    if show != 1:
        return "I'm sorry, but I can't show this in this channel"
    if len(pic) < 5:
        return "Well, I'm sorry to say this, but we don't have that anymore. Try adding it again if you happen to have it"
    return pic

def tag(tagger, channel):
    if channel == '<Custom channel>':
        if tagger.lower() == '<Custom tag>':
            return "I'm sorry, but I can't show these images in this channel"
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
    if len(taglist) == 1:
        return taglist[0]
    while True:
        pic = taglist[random.randrange(0, len(taglist) - 1)]
        if "<Custom Tag>" not in pic.lower():
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
            try:
                if int(check[0]) != i:
                    return "We have a problem at " + str(i)
            except:
                print(str(i) + " " + str(idnum))
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
#Just a dice roller I added
def rolldice(time, dice):
    if int(time) == 1:
        return random.randrange(1, int(dice))
    else:
        return random.randrange(1, int(dice)) + rolldice(int(time) - 1, dice)
def printall():
    openfile = open("pictures.txt", 'r')
    contents = openfile.readlines()
    return contents
def helper():
    openfile = open("help.txt", 'r')
    contents = openfile.readlines()
    return contents

#From Klaus Byskov Pedersen https://stackoverflow.com/questions/17340922/how-to-search-if-dictionary-value-contains-certain-string-with-python
def search(values, searchFor):
    for k in values:
        print(k)
        for v in values[k]:
            print(v)
            if searchFor in v:
                return k
            return None
#This is a little thing I built that utalizes Hydrus. It's mostly fuctional for the most part.
def hydrustest(tag):
    if tag == "random":
        url = "http://<hydrus server>/get_files/search_files?system_archive=true&Hydrus-Client-API-Access-Key=<key>"
    else:
        url = "http://<hydrus server>/get_files/search_files?system_archive=true&tags=%5B%22" + tag + "%22%5D&Hydrus-Client-API-Access-Key=<key>"
    r = requests.get(url = url)
    data = r.json()
    dataparse = str([k for k in data.items()])
    datapar = dataparse[15:-3]
    if datapar.isdigit():
        hyid = datapar
        url = "http://<hydrus server>/get_files/file_metadata?file_ids=" + hyid + "&Hydrus-Client-API-Access-Key=<key>"
        t = requests.get(url = url)
        tdata = t.json()
        if "<Custom tag>" in str(tdata):
            return 0
        url = "http://<hydrus server>/get_files/file?system_archive=true&file_id=%5B" + hyid + "%5D&Hydrus-Client-API-Access-Key=<key>"
        return url
    else:
        onemoretime = datapar.split(',')
        while True:
            hyid = onemoretime[random.randrange(0, len(onemoretime) - 1)]
            print(hyid)
            url = "http://<hydrus server>/get_files/file_metadata?file_ids=%5B" + hyid + "%5D&Hydrus-Client-API-Access-Key=<key>"
            t = requests.get(url = url)
            tdata = t.json()
            tags = 0
            print(tags)
            if '<custom tag>' in str(tdata):
                tags = 1
                print(tags)
            elif tags == 0:
                print(tags)
                url = "http://<hydrus server>/get_files/file?system_archive=true&file_id=" + hyid + "&Hydrus-Client-API-Access-Key=<key>"
                return url
            tags = 0
    
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
        tmp = await message.channel.send('Calculating messages...')
        try:
            for log in client.logs_from(message.channel, limit=100):
                if log.author == message.author:
                    counter += 1
            await client.edit_message(tmp, 'You have {} messages.'.format(counter))
        except:
            await message.channel.send("This, didn't work very well. I don't think the author updated this code yet.")
    elif message.content.startswith('!sleep'):
        await asyncio.sleep(5)
        await message.channel.send('Done sleeping')

    elif message.content.lower().startswith('!pic'):
        await message.channel.send(pic(str(message.channel)))

    elif message.content.lower().startswith('!add'):
        if(message.attachments == []):
            await message.channel.send(add(message.content[5:], message.author))
        else:
            content = message.attachments[0]
            await message.channel.send( add(str(content['url'] + " " + message.content[5:]), message.author))

    elif message.content.lower().startswith('!id'):
        await message.channel.send( idreturn(message.content[4:], str(message.channel)))

    elif message.content.lower().startswith('!tag'):
        try:
            await message.channel.send( tag(message.content[5:], str(message.channel)))
        except:
            await message.channel.send( "uhm... Sorry about this, but we don't HAVE any " + str(message.content[5:]) + ". How about you add one of your own using !pic?")
        
    elif message.content.startswith('!systemcheck'):
        await message.channel.send( syscheck())

    elif message.content.startswith('!del'):
        await message.channel.send( delete(message.content[5:]))
    elif message.content.startswith('!roll'):
        dcon = message.content[6:].split('d')
        try:
            await message.channel.send( rolldice(dcon[0], dcon[1]))
        except:
            await message.channel.send( "Whoa there, that's too many dice for me to handle at one time. Could you split it up into reasonably sized chunks? Thanks!")
    elif message.content.startswith('!simage'):
        await message.channel.send( searchimage(message.content[8:]))
    elif message.content.startswith('!printall'):
        await message.channel.send( "Please type the following: !Confirmation") #Honestly, This is just to make sure someone didn't type it by accident because too many calls will definitly make the bot spam
    elif message.content.startswith("!Confirmation"):
        content = printall()
        for items in content:
            try:
                await message.channel.send( items)
                time.sleep(3)
            except:
                time.sleep(1)
    elif message.content.startswith("!hydrus"):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(hydrustest(message.content[8:])) as resp:
                    if resp.status != 200:
                        return await channel.send('Could not download file...')
                    data = io.BytesIO(await resp.read())
                    await message.channel.send(file=discord.File(data, 'image.png'))
        except: await message.channel.send("Uhm... That came back with a 0... Either that, or something's wrong")
    elif message.content.startswith("!help"):
        content = helper()
        for items in content:
            try:
                await message.channel.send( items)
                time.sleep(1)
            except:
                time.sleep(1)
        
while True:
    try:
        client.run('<Discord key>')
    except ConnectionResetError:
        print("reconnect")
    except Exception as error:
        print(error)
        client.close()
