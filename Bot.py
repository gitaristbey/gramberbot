# Coder by Ahmet Tokka ♥ 
# Coder by Ahmet Tokka ♥ 
# Coder by Ahmet Tokka ♥ 
# Coder by Ahmet Tokka ♥ 
# Coder by Ahmet Tokka ♥ 
# Coder by Ahmet Tokka ♥ 


from ast import pattern
import os, logging, asyncio
from telethon import Button
from telethon import TelegramClient, events
from telethon.tl.types import ChannelParticipantAdmin
from telethon.tl.types import ChannelParticipantCreator
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.errors import UserNotParticipantError
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from telethon.tl.types import ChannelParticipantsAdmins


logging.basicConfig(
    level=logging.INFO,
    format='%(name)s - [%(levelname)s] - %(message)s'
)
LOGGER = logging.getLogger(__name__)

api_id = os.environ.get("APP_ID")
api_hash = os.environ.get("API_HASH")
bot_token = os.environ.get("TOKEN")
client = TelegramClient('client', api_id, api_hash).start(bot_token=bot_token)
spam_chats = []

@client.on(events.NewMessage(pattern="^/start$"))
async def start(event):
  await event.reply(
    "Merhaba tatlım ben telegramdaki tüm grup üyelerini etiketlemek için tasarlandım ismim MENTION GRAMBER \n**Yardım Almak İçin Buraya Tıkla** /grhelp\n\n**Seni Seviyoruz** [♥](https://t.me/SohbetTurkSancagi)",
    link_preview=False,
    buttons=(
      [
        Button.url('⚙️ Beni Gruplara Ekle ⚙️', 'https://t.me/MentionGramberBot?startgroup=true'),
        Button.url('👥 Grubumuz 👥︎', 'https://t.me/SohbetTurkSancagi'),
        ],
        [
        Button.url('❤️ Yapan Kişi ❤️️', 'https://t.me/gitaristbey'),
      ]
    )
  )
                    
                    
@client.on(events.NewMessage(pattern="^/grhelp$"))
async def help(event):
  helptext = "**Mention Gramber Yardım Menüsü**\n\n**Komutlar**: /grall **Herkesi Etiketler** \n**Komut**: /cancel **Etiketlemeyi Durdurur**\n**__Bu komutun yanında herkese istediğiniz şeylerden bahsedebilirsiniz.__**\n**/gradmin: Sadece Adminleri Etiketler**\n`Örneğin: /grall Günaydıın!`\n**__Bu komutu herhangi bir mesaja cevap olarak verebilirsiniz. Bot, kullanıcıları bu yanıtlanan mesaja etiketleyecek__**."
  await event.reply(
    helptext,
    link_preview=False,
    buttons=(
      [
        Button.url('❤️ Grubumuz ❤️', 'https://t.me/SohbetTurkSancagi'),
      ]
    )
  )

  @client.on(events.NewMessage(pattern="^/cancel@MentionGramberBot"))
async def deletemessage(event):
  deletemessage = "Botu Durdurmak İçin Lütfen Buna Tıklayın => /cancel"
  await event.reply(
    deletemessage
    link_preview=False,
    buttons=(
      [
        Button.url('❤️ Grubumuz ❤️', 'https://t.me/SohbetTurkSancagi'),
      ]
    )
    
@client.on(events.NewMessage(pattern="^/owner$"))
async def help(event):
  helptext = "**Gramber Botun Sahip Menüsü**\n\n**Sahibim [GitaristBey](https://t.me/gitaristbey)**"
  await event.reply(
    helptext,
    link_preview=False,
    )


@client.on(events.NewMessage(pattern="^/grall ?(.*)"))
async def mentionall(event):
  chat_id = event.chat_id
  if event.is_private:
    return await event.respond("__Bu komut gruplarda ve kanallarda kullanılabilir.!__")
  
  is_admin = False
  try:
    partici_ = await client(GetParticipantRequest(
      event.chat_id,
      event.sender_id
    ))
  except UserNotParticipantError:
    is_admin = False
  else:
    if (
      isinstance(
        partici_.participant,
        (
          ChannelParticipantAdmin,
          ChannelParticipantCreator
        )
      )
    ):
      is_admin = True
  if not is_admin:
    return await event.respond("__Yalnızca yöneticiler Kullanabilir!__")
  
  if event.pattern_match.group(1) and event.is_reply:
    return await event.respond("__Bana bir argüman ver!__")
  elif event.pattern_match.group(1):
    mode = "text_on_cmd"
    msg = event.pattern_match.group(1)
  elif event.is_reply:
    mode = "text_on_reply"
    msg = await event.get_reply_message()
    if msg == None:
        return await event.respond("__Eski mesajlar için üyelerden bahsedemem! (gruba eklenmeden önce gönderilen mesajlar)__")
  else:
    return await event.respond("__Bir mesajı yanıtlayın veya başkalarından bahsetmem için bana bir metin verin!__")
  
  spam_chats.append(chat_id)
  usrnum = 0
  usrtxt = ''
  async for usr in client.iter_participants(chat_id):
    if not chat_id in spam_chats:
      break
    usrnum += 1
    usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) "
    if usrnum == 5:
      if mode == "text_on_cmd":
        txt = f"{usrtxt}\n\n{msg}"
        await client.send_message(chat_id, txt)
      elif mode == "text_on_reply":
        await msg.reply(usrtxt)
      await asyncio.sleep(2)
      usrnum = 0
      usrtxt = ''
  try:
    spam_chats.remove(chat_id)
  except:
    pass

@client.on(events.NewMessage(pattern="^/cancel$"))
async def cancel_spam(event):
  if not event.chat_id in spam_chats:
    return await event.respond('__Devam eden bir süreç yok...__')
  else:
    try:
      spam_chats.remove(event.chat_id)
    except:
      pass
    return await event.respond('__Durduruldu.__')

print(">> Gramber Bot Çalışıyor <<")
client.run_until_disconnected()
