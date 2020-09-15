from telegram import Update, Bot, ParseMode
from telegram.ext import run_async

from alluka.modules.disable import DisableAbleCommandHandler
from alluka import dispatcher

from requests import get

@run_async
def ud(bot: Bot, update: Update):
  message = update.effective_message
  text = message.text[len('/familylist '):]
  
  Divuimg = "https://telegra.ph/file/4aee5cfe2ba8a3fa503d0.jpg"
  Divu = """[Mr.Divu」](https://telegram.dog/imDivu) As *Hisoka Morow*.\n To Get More About Him Do `/info @imDivu`"""

  Ayanokojiimg = "https://telegra.ph/file/1cf42dcd39ff264f5a2f1.jpg"
  Ayanokoji = """[Ayanokōji](https://telegram.dog/Ayanokoji_op) As Ayanokōji.\n To Get More About Him Do `/info @Ayanokoji_op`"""


 

  message.reply_photo(Ayanokojiimg, Ayanokoji, parse_mode=ParseMode.MARKDOWN)
  message.reply_photo(Divuimg, Divu, parse_mode=ParseMode.MARKDOWN)  


  
ud_handle = DisableAbleCommandHandler("familylist", ud)

dispatcher.add_handler(ud_handle)
