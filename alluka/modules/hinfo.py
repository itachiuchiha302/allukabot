import html
import json
import os
import psutil
import random
import time
import datetime
from typing import Optional, List
import re
import requests
from telegram.error import BadRequest
from telegram import Message, Chat, Update, Bot, MessageEntity
import alluka.modules.helper_funcs.cas_api as cas
from telegram import ParseMode
from telegram.ext import CommandHandler, run_async, Filters
from telegram.utils.helpers import escape_markdown, mention_html
from alluka.modules.helper_funcs.chat_status import user_admin, sudo_plus, is_user_admin
from alluka import dispatcher, OWNER_ID, SUDO_USERS, SUPPORT_USERS, DEV_USERS, WHITELIST_USERS, BAN_STICKER
from alluka.__main__ import STATS, USER_INFO, TOKEN
from alluka.modules.disable import DisableAbleCommandHandler, DisableAbleRegexHandler
from alluka.modules.helper_funcs.extraction import extract_user
from alluka.modules.helper_funcs.filters import CustomFilters
import alluka.modules.sql.users_sql as sql
import alluka.modules.sql.antispam_sql as get_gbanned_user 

@run_async
def hinfo(bot: Bot, update: Update, args: List[str]):
    message = update.effective_message
    chat = update.effective_chat
    user_id = extract_user(update.effective_message, args)

    if user_id:
        user = bot.get_chat(user_id)

    elif not message.reply_to_message and not args:
        user = message.from_user

    elif not message.reply_to_message and (not args or (
            len(args) >= 1 and not args[0].startswith("@") and not args[0].isdigit() and not message.parse_entities(
        [MessageEntity.TEXT_MENTION]))):
        message.reply_text("I can't extract a user from this.")
        return

    else:
        return

    text = (f"<b>Characteristics :-</b>\n\n"
            f"ID :- <code>{user.id}</code>\n"
            f"First Name :- {html.escape(user.first_name)}")

    if user.last_name:
        text += f"\nLast Name :- {html.escape(user.last_name)}"

    if user.username:
        text += f"\nUsername  :- @{html.escape(user.username)}"

    text += f"\nUser Link    :- {mention_html(user.id, ' Here 🤡')}"

    
    num_chats = sql.get_user_num_chats(user.id)
    text += f"\n\nMutual Chats :-  <code>{num_chats}</code> \n"

    try:
        user_member = chat.get_member(user.id)
        if user_member.status == 'administrator':
            result = requests.post(f"https://api.telegram.org/bot{TOKEN}/getChatMember?chat_id={chat.id}&user_id={user.id}")
            result = result.json()["result"]
            if "custom_title" in result.keys():
                custom_title = result['custom_title']
                text += f"\nAdmin Title    :-  <b>{custom_title}</b> \n"
    except BadRequest:
        pass

   
    if user.id == OWNER_ID:
        text += "\nThis Person is my owner - I would never do anything against them!."
        
    elif user.id in DEV_USERS:
        text += "\nDEV USER :  <b> YES </b> "
        
    elif user.id in SUDO_USERS:
        text += "\nSUDO USER :  <b> YES </b> " 
        
    elif user.id in SUPPORT_USERS:
        text += "\nSUPPORT USER :  <b> YES </b>"
        
  
       
    elif user.id in WHITELIST_USERS:
        text += "\nWHITELIST USER :  <b> YES </b>"
       

    text +="\n"
    text += "\nCAS Banned : "
    result = cas.banchecker(user.id)
    text += str(result)
    

    
    text +="\n"
    is_gbanned = sql.is_user_gbanned(user_id)

    text += "Globally Banned :  <b>{}</b>"
    if is_gbanned:
        text += text.format("Yes")
        user = sql.get_gbanned_user(user_id)
        if user.reason:
            text += "\nReason: <code>{}</code>".format(html.escape(user.reason))
    else:
        text += text.format("No")
    return text

    update.effective_message.reply_text(text, parse_mode=ParseMode.HTML, disable_web_page_preview=True)

HINFO_HANDLER = DisableAbleCommandHandler("hinfo", hinfo, pass_args=True)
dispatcher.add_handler(HINFO_HANDLER)
