from pyrogram import filters

from Shikimori import pbot
from Shikimori.utils.errors import capture_err
from Shikimori.utils.functions import make_carbon


@pbot.on_message(filters.command("carbon"))
@capture_err
async def carbon_func(_, message):
    if not message.reply_to_message:
        return await message.reply_text("`Reply To A Text To Generat Carbon.`")
    if not message.reply_to_message.text:
        return await message.reply_text("`Reply To A Text To Generate Carbon.`")
    m = await message.reply_text("π` Generating Carbo...`")
    carbon = await make_carbon(message.reply_to_message.text)
    await m.edit("π€` Uploading Generated Carbon...`")
    await pbot.send_photo(message.chat.id, carbon)
    await m.delete()
    carbon.close()


__mod_name__ = "Cα΄ΚΚα΄Ι΄"

__help__ = """

Make A Carbon Of The Given Text And Sent It To You.

β /carbon *:* Makes Carbon If Replied To A Text.

β π£πΌππ²πΏπ²π± ππ
β @MaximXRobot
 """
