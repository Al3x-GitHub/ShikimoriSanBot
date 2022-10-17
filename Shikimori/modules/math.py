from requests import request

from FallenRobot.events import register


@register(pattern="^/math ?(.*)")
async def ss(event):
    input_str = event.pattern_match.group(1)
    if not input_str:
        return await event.reply("ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴛʜᴇ ᴍᴀᴛʜᴀᴍᴀᴛɪᴄᴀʟ ᴇǫᴜᴀᴛɪᴏɴ.")
    url = "https://evaluate-expression.p.rapidapi.com/"
    querystring = {"expression": input_str}
    headers = {
        "x-rapidapi-key": "fef481fee3mshf99983bfc650decp104100jsnbad6ddb2c846",
        "x-rapidapi-host": "evaluate-expression.p.rapidapi.com",
    }
    response = request("GET", url, headers=headers, params=querystring)
    if not response or not response.text:
        return await event.reply("ɪɴᴠᴀʟɪᴅ ᴍᴀᴛʜᴀᴍᴀᴛɪᴄᴀʟ ᴇǫᴜᴀᴛɪᴏɴ ᴘʀᴏᴠɪᴅᴇᴅ.")
    await event.reply(response.text)
