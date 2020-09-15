from telegram import Update, Bot, ParseMode
from telegram.ext import run_async

from alluka.modules.disable import DisableAbleCommandHandler
from alluka import dispatcher

from requests import get

@run_async
def ud(bot: Bot, update: Update):
  message = update.effective_message
  text = message.text[len('/familylist '):]
  
  Devimg = "https://telegra.ph/file/4aee5cfe2ba8a3fa503d0.jpg"
  Dev = """[Sed Lyf](https://telegram.dog/Ayanokoji_op) as Hisoka Morow.\n To get more about him do `!info @Ayanokoji_op`"""

  Divuimg = "https://telegra.ph/file/520c4b38b71f82e312f5b.png"
  Divu = """[Mr.Divu」](https://telegram.dog/imDivu) as Kite.\n To get more about him do `!info @imDivu`"""


 

  message.reply_photo(Devimg, Dev, parse_mode=ParseMode.MARKDOWN)
  message.reply_photo(Divuimg, Divu, parse_mode=ParseMode.MARKDOWN)  


  
ud_handle = DisableAbleCommandHandler("familylist", ud)

dispatcher.add_handler(ud_handle)
