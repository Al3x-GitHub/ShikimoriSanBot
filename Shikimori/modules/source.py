from platform import python_version as y

from pyrogram import __version__ as z
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import __version__ as o
from telethon import __version__ as s

from Shikimori import OWNER_USERNAME, dispatcher
from Shikimori import pbot as client

ANON = "https://te.legra.ph/file/0c13eb00aaba21dd2f541.jpg"


@client.on_message(filters.command(["repo", "source"]))
async def repo(client, message):
    await message.reply_photo(
        photo=ANON,
        caption=f"""**Hey {message.from_user.mention()},\n\nI'm [{dispatcher.bot.first_name}](t.me/{dispatcher.bot.username})**

**» My Baby :** [I𝗓υɱi 和泉](tg://user?id=5409743649)
**» Python Version :** `{y()}`
**» Library Version  :** `{o}` 
**» Telethon Version  :** `{s}` 
**» Pyrogram Version :** `{z}`
""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "• ᴏᴡɴᴇʀ •", url=f"https://t.me/{OWNER_USERNAME}"
                    ),
                    InlineKeyboardButton(
                        "• sᴏᴜʀᴄᴇ •",
                        url="https://t.me/+vBu5aXlocTkwNGM1",
                    ),
                ]
            ]
        ),
    )


__mod_name__ = "Rᴇᴩᴏ"
