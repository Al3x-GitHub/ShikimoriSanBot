from datetime import datetime

from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from Shikimori import OWNER_ID
from Shikimori import OWNER_USERNAME as uWu
from Shikimori import START_IMG, SUPPORT_CHAT, pbot
from Shikimori.utils.errors import capture_err


def content(msg: Message) -> [None, str]:
    text_to_return = msg.text

    if msg.text is None:
        return None
    if " " in text_to_return:
        try:
            return msg.text.split(None, 1)[1]
        except IndexError:
            return None
    else:
        return None


@pbot.on_message(filters.command("bug"))
@capture_err
async def bug(_, msg: Message):
    if msg.chat.username:
        chat_username = f"@{msg.chat.username}/`{msg.chat.id}`"
    else:
        chat_username = f"Private Group/`{msg.chat.id}`"

    bugs = content(msg)
    user_id = msg.from_user.id
    mention = (
        "[" + msg.from_user.first_name + "](tg://user?id=" + str(msg.from_user.id) + ")"
    )
    datetimes_fmt = "%d-%m-%Y"
    datetimes = datetime.utcnow().strftime(datetimes_fmt)

    bug_report = f"""
**#Bug :** @{uWu}

**Reported By :** {mention}
**User ID :** {user_id}
**Chat : {chat_username}

**Bug :** {bugs}

**Event Stamp :** {datetimes}"""

    if msg.chat.type == "private":
        await msg.reply_text("<b>» This Command Is Only For Groups.</b>")
        return

    if user_id == OWNER_ID:
        if bugs:
            await msg.reply_text(
                "<b>» Are You Comedy Me 😂, You're The Owner Of The Bot 🤖.</b>",
            )
            return
        else:
            await msg.reply_text("Owner")
    elif user_id != OWNER_ID:
        if bugs:
            await msg.reply_text(
                f"<b>Bug Report : {bugs}</b>\n\n"
                "<b>» Bug Successfully Reported At Support Group.</b>",
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("• ᴄʟᴏsᴇ •", callback_data=f"close_reply")]]
                ),
            )
            await pbot.send_photo(
                SUPPORT_CHAT,
                photo=START_IMG,
                caption=f"{bug_report}",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton("• ᴠɪᴇᴡ ʙᴜɢ •", url=f"{msg.link}")],
                        [
                            InlineKeyboardButton(
                                "• ᴄʟᴏsᴇ •", callback_data="close_send_photo"
                            )
                        ],
                    ]
                ),
            )
        else:
            await msg.reply_text(
                f"<b>» 👮🏻‍♀️ No Bug To Report.</b>",
            )


@pbot.on_callback_query(filters.regex("close_reply"))
async def close_reply(msg, CallbackQuery):
    await CallbackQuery.message.delete()


@pbot.on_callback_query(filters.regex("close_send_photo"))
async def close_send_photo(_, CallbackQuery):
    if CallbackQuery.from_user.id != OWNER_ID:
        return await CallbackQuery.answer(
            " You Don't Have Rights To Close This.", show_alert=True
        )
    else:
        await CallbackQuery.message.delete()


__help__ = """
*For Reporting A Bug In sʜɪᴋɪᴍᴏʀɪ ✘ ʙᴏᴛ*
 ❍ /bug *:* To Report A Bug At Support Group.

❏ 𝗣𝗼𝘄𝗲𝗿𝗲𝗱 𝗕𝘆
┗ @MaximXRobot
"""
__mod_name__ = "Bᴜɢ"
