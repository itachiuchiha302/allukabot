import time
from typing import List

import requests
from telegram import Bot, Update, ParseMode
from telegram.ext import run_async

from alluka import dispatcher
from alluka.modules.helper_funcs.chat_status import sudo_plus
from alluka.modules.disable import DisableAbleCommandHandler

sites_list = {
    "Telegram": "https://api.telegram.org"
}


def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        if count < 3:
            remainder, result = divmod(seconds, 60)
        else:
            remainder, result = divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "

    time_list.reverse()
    ping_time += ":".join(time_list)

    return ping_time


def ping_func(to_ping: List[str]) -> List[str]:
    ping_result = []

    for each_ping in to_ping:

        start_time = time.time()
        site_to_ping = sites_list[each_ping]
        r = requests.get(site_to_ping)
        end_time = time.time()
        ping_time = str(round((end_time - start_time), 2)) + "s"

        pinged_site = f"<b>{each_ping}</b>"

        if each_ping == "Telegram":
            pinged_site = f'<a href="{sites_list[each_ping]}">{each_ping}</a>'
            ping_time = f"<code>{ping_time} (Status:{r.status_code})</code>"

        ping_text = f"╽ \n┣⊸ {pinged_site} : <code>{ping_time}</code>"
        ping_result.append(ping_text)

    return ping_result


@run_async 
def ping(bot: Bot, update: Update):
    msg = update.effective_message
    
    start_time = time.time()
    bot.sendChatAction(update.effective_chat.id, "typing")
    message = msg.reply_text("Pinging")
    bot.sendChatAction(update.effective_chat.id, "typing")
    message.edit_text("Pinging.")
    message.edit_text("Pinging..")
    end_time = time.time()
    message.edit_text("Pinging...")
    telegram_ping = str(round((end_time - start_time) * 1000, 3)) + " ms"
    
    message.edit_text(
        "PONG!!\n"
        "<b>Time Taken : </b> <code>{}</code>\n".format(telegram_ping),
        parse_mode=ParseMode.HTML)


@run_async
@sudo_plus
def pingall(bot: Bot, update: Update):
    to_ping = ["Telegram"]
    pinged_list = ping_func(to_ping)
    pinged_list.insert(2, '')
    start_time = time.time()
    end_time = time.time()
    hinata_ping = str(round((end_time - start_time) * 1000, 3)) + " ms"
    
    reply_msg = "╭─⌈ Ping Results Are \n"
    reply_msg += "\n".join(pinged_list)
    reply_msg += "┗⊸ My Ping   : <code>{}</code>".format(hinata_ping)
    update.effective_message.reply_text(
        reply_msg, parse_mode=ParseMode.HTML, disable_web_page_preview=True)


PING_HANDLER = DisableAbleCommandHandler("ping", ping)
PINGALL_HANDLER = DisableAbleCommandHandler("pingall", pingall)

dispatcher.add_handler(PING_HANDLER)
dispatcher.add_handler(PINGALL_HANDLER)

__command_list__ = ["ping", "pingall"]
__handlers__ = [PING_HANDLER, PINGALL_HANDLER]
