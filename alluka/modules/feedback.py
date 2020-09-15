import html
from telegram import Update, Bot, ParseMode
from telegram.ext import run_async
from alluka.modules.disable import DisableAbleCommandHandler
from alluka import dispatcher
from requests import get
from telegram import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton



@run_async
def feedback(bot: Bot, update: Update):
  name = update.effective_message.from_user.first_name
  message = update.effective_message
  userid=message.from_user.id
  text = message.text[len('/feedback '):]
   

  feed_text = f"HINATA'S *New* Feedback From [{name}](tg://user?id={userid})\n\nFeed→_→: {text}"
  

  bot.send_message(-1001237122568, feed_text, parse_mode=ParseMode.MARKDOWN)
 
  text = html.escape(text)
  reply_text=f"Thank-You For Giving Us Your Feedback."
  message.reply_text(reply_text, reply_markup=InlineKeyboardMarkup(
                                                [[InlineKeyboardButton(text="You Can See Your *Feedback* Here",url="t.me/MissLilly_Support")]]))
                                               
  

  





feed_handle = DisableAbleCommandHandler("feedback", feedback)

dispatcher.add_handler(feed_handle)
