import requests
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from Shikimori import BOT_NAME, BOT_USERNAME
from Shikimori import pbot as fallen


@fallen.on_message(filters.command("write"))
async def handwrite(_, message: Message):
    if not message.reply_to_message:
        text = message.text.split(None, 1)[1]
        m = await fallen.send_message(
            message.chat.id, "`Please wait...,\n\nWriting your text...`"
        )
        API = f"https://api.sdbots.tk/write?text={text}"
        req = requests.get(API).url
        caption = f"""
Successfully Written Text π

β¨ **Written By :** [{BOT_NAME}](https://t.me/{BOT_USERNAME})
π₯ **Requested by :** {message.from_user.mention}
β **Link :** `{req}`
"""
        await m.delete()
        await fallen.send_photo(
            message.chat.id,
            photo=req,
            caption=caption,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("β’ α΄α΄Κα΄Ι’Κα΄α΄©Κ β’", url=f"{req}")]]
            ),
        )
    else:
        lol = message.reply_to_message.text
        m = await fallen.send_message(
            message.chat.id, "`Please wait...,\n\nWriting your text...`"
        )
        API = f"https://api.sdbots.tk/write?text={lol}"
        req = requests.get(API).url
        caption = f"""
Successfully Written Text π

β¨ **Written By :** [{BOT_NAME}](https://t.me/{BOT_USERNAME})
π₯ **Requested by :** {message.from_user.mention}
β **Link :** `{req}`
"""
        await m.delete()
        await fallen.send_photo(
            message.chat.id,
            photo=req,
            caption=caption,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("β’ α΄α΄Κα΄Ι’Κα΄α΄©Κ β’", url=f"{req}")]]
            ),
        )


__mod_name__ = "WΚΙͺα΄α΄Tα΄α΄Κ"

__help__ = """

 Writes the given text on white page with a pen π

β /write <text> *:* Writes the given text.

β π£πΌππ²πΏπ²π± ππ
β @MaximXRobot
 """
