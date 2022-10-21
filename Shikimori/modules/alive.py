import random

from pyrogram import __version__ as pyrover
from telegram import __version__ as telever
from telethon import Button
from telethon import __version__ as tlhver

from Shikimori import OWNER_USERNAME, SUPPORT_CHAT, dispatcher
from Shikimori import telethn as tbot
from Shikimori.events import register

PHOTO = [
"https://te.legra.ph/file/0325da0c1422acc1ee7a3.jpg",
"https://te.legra.ph/file/a9f0df8afe53e8b8154a5.jpg",
"https://te.legra.ph/file/7cf3fcf1778acc3184997.jpg",
"https://te.legra.ph/file/b7322de19b8c94d3fc6f3.jpg",
"https://te.legra.ph/file/95e7dc37f427a0a2e5e64.jpg",
"https://te.legra.ph/file/c1a5426d0e0fc8e893c99.jpg",
"https://te.legra.ph/file/24465e3cbd9767aab29ea.jpg",
"https://te.legra.ph/file/d9e3166c983d690d378c5.jpg",
"https://te.legra.ph/file/67864aa1f1a1a79714a0f.jpg",
"https://te.legra.ph/file/17dd53b6a5922431bf01e.jpg",
"https://te.legra.ph/file/cb101461c47f25f088ed3.jpg",
"https://te.legra.ph/file/2e0a00b2545ba2e8ff0cd.jpg",
"https://te.legra.ph/file/86037156a878c0273df07.jpg",
"https://te.legra.ph/file/1bcbec5bd64dd502afff2.jpg",
"https://te.legra.ph/file/ed3d3b5fc1cdb6626c4a5.jpg",
"https://te.legra.ph/file/19a6b6842a5e0e8a510e1.jpg",
"https://te.legra.ph/file/af3f9a03186608f0d56cf.jpg",
"https://te.legra.ph/file/3fd1351cbd218e1047773.jpg",
"https://te.legra.ph/file/d3827183fdecbe0bf313f.jpg",
"https://te.legra.ph/file/77e4388f1d68a6557755f.jpg",
"https://te.legra.ph/file/f83b2a809d9424ffc6485.jpg",
"https://te.legra.ph/file/230ee12a06cd0f42bbe63.jpg",
"https://te.legra.ph/file/230ee12a06cd0f42bbe63.jpg"
]


@register(pattern=("/alive"))
async def awake(event):
    TEXT = f"**Hey [{event.sender.first_name}](tg://user?id={event.sender.id}),\n\nI'm {dispatcher.bot.first_name}**\n━━━━━━━━━━━━━━━━━━━\n\n"
    TEXT += f"» **My Baby : [I𝗓υɱi 和泉](https://t.me/{OWNER_USERNAME})** \n\n"
    TEXT += f"» **Library Version :** `{telever}` \n\n"
    TEXT += f"» **Telethon Version :** `{tlhver}` \n\n"
    TEXT += f"» **Pyrogram Version :** `{pyrover}` \n━━━━━━━━━━━━━━━━━\n\n"
    BUTTON = [
        [
            Button.url("ʜᴇʟᴘ​", f"https://t.me/{dispatcher.bot.username}?start=help"),
            Button.url("sᴜᴘᴘᴏʀᴛ​", f"https://t.me/{SUPPORT_CHAT}"),
        ]
    ]
    ran = random.choice(PHOTO)
    await tbot.send_file(event.chat_id, ran, caption=TEXT, buttons=BUTTON)


__mod_name__ = "Aʟɪᴠᴇ"
