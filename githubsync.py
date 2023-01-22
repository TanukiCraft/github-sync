from sultan.api import Sultan
from quart import Quart
from quart import request
import json
import os
import subprocess
import disnake
import asyncio
import threading
from disnake.ext import commands
from signal import signal, SIGPIPE, SIG_DFL  
signal(SIGPIPE,SIG_DFL)
from multiprocessing import Process, Value
from ftplib import FTP
import time
s = Sultan()
servers = ['11', '2', '3', '6', '14', '4']
megserer = ['4']
global lastservertransfer
global notifychannel

bot = commands.Bot(command_prefix='.', test_guilds=[REDACTED], sync_commands_debug=True)
app = Quart(__name__)


@bot.slash_command(description="force a resync of shop files")
async def forcesyncshop(inter):
    await inter.response.defer()
    print("got notified of updated github files, pulling and logging into ftp")
    print("logged in! cloning files from github")
    s.git("clone", "https://github.com/Worst-Server-Ever/shop-files.git").run()
    shopfiles = os.listdir('shop-files')
    print("everything setup begining file transfer")
    for i in shopfiles:
        if i == '.git':
            pass
        else:
            for se in servers:
                print(f"begining transfer of {i} to server {se}...")
                subprocess.run(f'./bashftp {i} /plugins/DeluxeMenus/gui_menus {se} shop-files', shell=True)
                print(f"{i} transfered to server {se}!")
    for se in servers:            
        s.php("phpscripts/sendservercmd.php", se, "'dm reload'")
        print(f"reloaded dm on {se}")
    s.rm("-rf", "shop-files").run()
    await inter.edit_original_message(content=f"Force sync of shop files finished!")

@bot.slash_command(description="force a resync of model engine files")
async def forcesyncmeg(inter):
    await inter.response.defer()
    print("got notified of updated github files, pulling and logging into ftp")
    print("logged in! cloning files from github")
    s.git("clone", "https://github.com/Worst-Server-Ever/model-engine-wsefiles.git").run()
    meganimations = os.listdir('model-engine-wsefiles/animations')
    megblueprints = os.listdir('model-engine-wsefiles/blueprints')
    megtextures = os.listdir('model-engine-wsefiles/textures')
    print("everything setup begining file transfer")
    for i in meganimations:
        if i == '.git':
            pass
        else:
            for se in megserer:
                print(f"begining transfer of {i} to server {se}...")
                subprocess.run(f'./bashftp {i} /plugins/ModelEngine/animations {se} model-engine-wsefiles/animations', shell=True)
                print(f"{i} transfered to server {se}!") 
                lastservertransfer = se
    for i in megblueprints:
        if i == '.git':
            pass
        else:
            for se in megserer:
                print(f"begining transfer of {i} to server {se}...")
                subprocess.run(f'./bashftp {i} /plugins/ModelEngine/blueprints {se} model-engine-wsefiles/blueprints', shell=True)
                print(f"{i} transfered to server {se}!")
                lastservertransfer = se
    for i in megtextures:
        if i == '.git':
            pass
        else:
            for se in megserer:
                print(f"begining transfer of {i} to server {se}...")
                subprocess.run(f'./bashftp {i} /plugins/ModelEngine/textures {se} model-engine-wsefiles/textures', shell=True)
                print(f"{i} transfered to server {se}!")
                
                lastservertransfer = se
    subprocess.run(f'./bashftp config.yml /plugins/ModelEngine {lastservertransfer} model-engine-wsefiles', shell=True)
    s.php("phpscripts/sendservercmd.php", lastservertransfer, "'meg reload'")
    print(f"reloaded meg on {lastservertransfer}")
    s.rm("-rf", "model-engine-wsefiles").run()
    print("finished!")
    await inter.edit_original_message(content=f"Force sync of model engine finished!")

#@bot.slash_command(description="get the current model engine texture pack for testing server")
@bot.command()
async def getmegpack(ctx):
    #await inter.response.defer()
    subprocess.run(f'./getmegpack \'"resource pack.zip"\' /plugins/ModelEngine 4', shell=True)
    await ctx.send(file=disnake.File(str('resource pack.zip'))) 
    if os.path.exists("resource pack.zip"):
             os.remove("resource pack.zip")
    else:
        pass

@app.before_serving
async def before_serving():
    loop = asyncio.get_event_loop()
    await bot.login('REDACTED')
    loop.create_task(bot.connect())

@app.route('/wseshopsync',methods=['POST'])
async def githubIssue():
    print("got notified of updated github files, pulling and logging into ftp")
    data = await request.json
    print(data)
    notifychannel = bot.get_channel(846164507582922782)
    commitname = data['sender']['login']
    avatarurl = data['sender']['avatar_url']
    embed=disnake.Embed(title="Sync Triggered!", description=f"A sync has been triggered on the repo {data['repository']['name']} by {commitname} with the reason {data['commits'][0]['message']}", color=0xfff700)
    embed.set_thumbnail(url=avatarurl)
    embed.set_footer(text="🤔 working on the sync...")
    msgtoedit = await notifychannel.send(embed=embed)
    print("logged in! cloning files from github")
    s.git("clone", "https://github.com/Worst-Server-Ever/shop-files.git").run()
    shopfiles = os.listdir('shop-files')
    print("everything setup begining file transfer")
    for i in shopfiles:
        if i == '.git':
            pass
        else:
            for se in servers:
                print(f"begining transfer of {i} to server {se}...")
                subprocess.run(f'./bashftp {i} /plugins/DeluxeMenus/gui_menus {se} shop-files', shell=True)
                print(f"{i} transfered to server {se}!")
    for se in servers:            
        s.php("phpscripts/sendservercmd.php", se, "'dm reload'")
        print(f"reloaded dm on {se}")
    print(f"reloaded dm on {se}")
    s.rm("-rf", "shop-files").run()
    print("finished!")
    embed=disnake.Embed(title="Sync Triggered!", description=f"A sync has been triggered on the repo {data['repository']['name']} by {commitname} with the reason {data['commits'][0]['message']}", color=0x00ff04)
    embed.set_thumbnail(url=avatarurl)
    embed.set_footer(text="👌 sync finished!")
    await msgtoedit.edit(embed=embed)
    return data

@app.route('/wsemegsync',methods=['POST'])
async def meggithub():
    print("got notified of updated github files, pulling and logging into ftp")
    data = await request.json
    print(data)
    print('aaaaaaaaaaaaaaaaaa')
    notifychannel = bot.get_channel(846164507582922782)
    commitname = data['sender']['login']
    avatarurl = data['sender']['avatar_url']
    embed=disnake.Embed(title="Sync Triggered!", description=f"A sync has been triggered on the repo {data['repository']['name']} by {commitname} with the reason {data['commits'][0]['message']}", color=0xfff700)
    embed.set_thumbnail(url=avatarurl)
    embed.set_footer(text="🤔 working on the sync...")
    msgtoedit = await notifychannel.send(embed=embed)
    print("logged in! cloning files from github")
    s.git("clone", "https://github.com/Worst-Server-Ever/model-engine-wsefiles.git").run()
    meganimations = os.listdir('model-engine-wsefiles/animations')
    megblueprints = os.listdir('model-engine-wsefiles/blueprints')
    megtextures = os.listdir('model-engine-wsefiles/textures')
    print("everything setup begining file transfer")
    for i in meganimations:
        if i == '.git':
            pass
        else:
            for se in megserer:
                print(f"begining transfer of {i} to server {se}...")
                subprocess.run(f'./bashftp {i} /plugins/ModelEngine/animations {se} model-engine-wsefiles/animations', shell=True)
                print(f"{i} transfered to server {se}!") 
                lastservertransfer = se
    for i in megblueprints:
        if i == '.git':
            pass
        else:
            for se in megserer:
                print(f"begining transfer of {i} to server {se}...")
                subprocess.run(f'./bashftp {i} /plugins/ModelEngine/blueprints {se} model-engine-wsefiles/blueprints', shell=True)
                print(f"{i} transfered to server {se}!")
                lastservertransfer = se
    for i in megtextures:
        if i == '.git':
            pass
        else:
            for se in megserer:
                print(f"begining transfer of {i} to server {se}...")
                subprocess.run(f'./bashftp {i} /plugins/ModelEngine/textures {se} model-engine-wsefiles/textures', shell=True)
                print(f"{i} transfered to server {se}!")
    subprocess.run(f'./bashftp config.yml /plugins/ModelEngine {lastservertransfer} model-engine-wsefiles', shell=True)
    for se in megserer:            
        s.php("phpscripts/sendservercmd.php", se, "'meg reload'")
        print(f"reloaded dm on {se}")
    print(f"reloaded meg on {se}")
    s.rm("-rf", "model-engine-wsefiles").run()
    print("finished!")
    embed=disnake.Embed(title="Sync Triggered!", description=f"A sync has been triggered on the repo {data['repository']['name']} by {commitname} with the reason {data['commits'][0]['message']}", color=0x00ff04)
    embed.set_thumbnail(url=avatarurl)
    embed.set_footer(text="👌 sync finished!")
    await msgtoedit.edit(embed=embed)
    return data


#def flaskstart():
app.run(debug=False, host='0.0.0.0', port='6942', use_reloader=False)

#if __name__ == '__main__':
    #p = Process(target=flaskstart())
    #p.start()
    #app.run(debug=False, host='0.0.0.0', port='6942', use_reloader=False)
    #bot.run('REDACTED')
    #bot.loop.create_task(app.run(debug=False, host='0.0.0.0', port='6942', use_reloader=False))
    #app.run(debug=False, host='0.0.0.0', port='6942', use_reloader=False)
    #p.join()