import html

from telegram import ParseMode, Update
from telegram.error import BadRequest
from telegram.ext import CallbackContext, CommandHandler, Filters, run_async
from telegram.utils.helpers import mention_html

from Shikimori import (
    DEMONS,
    DEV_USERS,
    DRAGONS,
    LOGGER,
    OWNER_ID,
    TIGERS,
    WOLVES,
    dispatcher,
)
from Shikimori.modules.disable import DisableAbleCommandHandler
from Shikimori.modules.helper_funcs.chat_status import (
    bot_admin,
    can_delete,
    can_restrict,
    connection_status,
    is_user_admin,
    is_user_ban_protected,
    is_user_in_chat,
    user_admin,
    user_can_ban,
)
from Shikimori.modules.helper_funcs.extraction import extract_user_and_text
from Shikimori.modules.helper_funcs.string_handling import extract_time
from Shikimori.modules.log_channel import gloggable, loggable


@run_async
@connection_status
@bot_admin
@can_restrict
@user_admin
@user_can_ban
@loggable
def ban(update: Update, context: CallbackContext) -> str:
    chat = update.effective_chat
    user = update.effective_user
    message = update.effective_message
    log_message = ""
    bot = context.bot
    args = context.args
    user_id, reason = extract_user_and_text(message, args)

    if not user_id:
        message.reply_text("I Doubt That's A User.")
        return log_message
    try:
        member = chat.get_member(user_id)
    except BadRequest as excp:
        if excp.message != "User Not Found":
            raise
        message.reply_text("Can't Seem To Find This Person.")
        return log_message
    if user_id == bot.id:
        message.reply_text("Oh Yeah, Ban Myself, Noob 😏!")
        return log_message

    if is_user_ban_protected(chat, user_id, member) and user not in DEV_USERS:
        if user_id == OWNER_ID:
            message.reply_text("Trying To Put Me Against A God Level Disaster Huh 😒?")
        elif user_id in DEV_USERS:
            message.reply_text("I Can't Act Against Our Own.")
        elif user_id in DRAGONS:
            message.reply_text(
                "Fighting This Dragon Here Will Put Civilian Lives At Risk."
            )
        elif user_id in DEMONS:
            message.reply_text(
                "Bring An Order From Heroes Association To Fight A Demon Disaster."
            )
        elif user_id in TIGERS:
            message.reply_text(
                "Bring An Order From Heroes Association To Fight A Tiger Disaster."
            )
        elif user_id in WOLVES:
            message.reply_text("Wolf Abilities Make Them Ban Immune!")
        else:
            message.reply_text("This User Has Immunity And Cannot Be Banned.")
        return log_message
    if message.text.startswith("/s"):
        silent = True
        if not can_delete(chat, context.bot.id):
            return ""
    else:
        silent = False
    log = (
        f"<b>{html.escape(chat.title)}:</b>\n"
        f"#{'S' if silent else ''}ʙᴀɴɴᴇᴅ\n"
        f"<b>Banned By:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
        f"<b>User:</b> {mention_html(member.user.id, html.escape(member.user.first_name))}"
    )
    if reason:
        log += "\n<b>Reason:</b> {}".format(reason)

    try:
        chat.kick_member(user_id)

        if silent:
            if message.reply_to_message:
                message.reply_to_message.delete()
            message.delete()
            return log

        # bot.send_sticker(chat.id, BAN_STICKER)  # banhammer marie sticker
        reply = (
            f"<code>❕</code><b>Ban Event</b>\n"
            f"<code> </code><b>•  Banned By:</b> {mention_html(user.id, user.first_name)}\n"
            f"<code> </code><b>•  User:</b> {mention_html(member.user.id, html.escape(member.user.first_name))}"
        )
        if reason:
            reply += f"\n<code> </code><b>•  Reason:</b> \n{html.escape(reason)}"
        bot.sendMessage(chat.id, reply, parse_mode=ParseMode.HTML, quote=False)
        return log

    except BadRequest as excp:
        if excp.message == "Reply Message Not Found":
            # Do not reply
            if silent:
                return log
            message.reply_text("Banned!", quote=False)
            return log
        else:
            LOGGER.warning(update)
            LOGGER.exception(
                "ERROR Banning User %s In Chat %s (%s) Due To %s",
                user_id,
                chat.title,
                chat.id,
                excp.message,
            )
            message.reply_text("Uhm... That Didn't Work...")

    return log_message


@run_async
@connection_status
@bot_admin
@can_restrict
@user_admin
@user_can_ban
@loggable
def temp_ban(update: Update, context: CallbackContext) -> str:
    chat = update.effective_chat
    user = update.effective_user
    message = update.effective_message
    log_message = ""
    bot, args = context.bot, context.args
    user_id, reason = extract_user_and_text(message, args)

    if not user_id:
        message.reply_text("I Doubt That's A User.")
        return log_message

    try:
        member = chat.get_member(user_id)
    except BadRequest as excp:
        if excp.message != "User Not Found":
            raise
        message.reply_text("I Can't Seem To Find This User.")
        return log_message
    if user_id == bot.id:
        message.reply_text("I'm Not Gonna BAN Myself, Are You Crazy Noob 😏?")
        return log_message

    if is_user_ban_protected(chat, user_id, member):
        message.reply_text("I Don't Feel Like It.")
        return log_message

    if not reason:
        message.reply_text("You Haven't Specified A Time To Ban This User For!")
        return log_message

    split_reason = reason.split(None, 1)

    time_val = split_reason[0].lower()
    reason = split_reason[1] if len(split_reason) > 1 else ""
    bantime = extract_time(message, time_val)

    if not bantime:
        return log_message

    log = (
        f"<b>{html.escape(chat.title)}:</b>\n"
        "Temp Ban\n"
        f"<b>Banned By:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
        f"<b>User:</b> {mention_html(member.user.id, html.escape(member.user.first_name))}\n"
        f"<b>Time:</b> {time_val}"
    )
    if reason:
        log += "\n<b>Reason:</b> {}".format(reason)

    try:
        chat.kick_member(user_id, until_date=bantime)
        # bot.send_sticker(chat.id, BAN_STICKER)  # banhammer marie sticker
        bot.sendMessage(
            chat.id,
            f"Banned! User {mention_html(member.user.id, html.escape(member.user.first_name))} "
            f"Is Now Banned For {time_val}.",
            parse_mode=ParseMode.HTML,
        )
        return log

    except BadRequest as excp:
        if excp.message == "Reply Message Not Found":
            # Do not reply
            message.reply_text(
                f"Banned! User Will Be Banned For {time_val}.", quote=False
            )
            return log
        else:
            LOGGER.warning(update)
            LOGGER.exception(
                "ERROR Banning User %s In Chat %s (%s) Due To %s",
                user_id,
                chat.title,
                chat.id,
                excp.message,
            )
            message.reply_text("Well Damn, I Can't Ban That User.")

    return log_message


@run_async
@connection_status
@bot_admin
@can_restrict
@user_admin
@user_can_ban
@loggable
def kick(update: Update, context: CallbackContext) -> str:
    chat = update.effective_chat
    user = update.effective_user
    message = update.effective_message
    log_message = ""
    bot, args = context.bot, context.args
    user_id, reason = extract_user_and_text(message, args)

    if not user_id:
        message.reply_text("I Doubt That's A User.")
        return log_message

    try:
        member = chat.get_member(user_id)
    except BadRequest as excp:
        if excp.message != "User Not Found":
            raise

        message.reply_text("I Can't Seem To Find This User.")
        return log_message
    if user_id == bot.id:
        message.reply_text("Yeahhh I'm Not Gonna Do That.")
        return log_message

    if is_user_ban_protected(chat, user_id):
        message.reply_text("I Really Wish I Could Kick This User....")
        return log_message

    res = chat.unban_member(user_id)  # unban on current user = kick
    if res:
        # bot.send_sticker(chat.id, BAN_STICKER)  # banhammer marie sticker
        bot.sendMessage(
            chat.id,
            f"One Kicked! {mention_html(member.user.id, html.escape(member.user.first_name))}.",
            parse_mode=ParseMode.HTML,
        )
        log = (
            f"<b>{html.escape(chat.title)}:</b>\n"
            f"Kicked\n"
            f"<b>Kicked By:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
            f"<b>User:</b> {mention_html(member.user.id, html.escape(member.user.first_name))}"
        )
        if reason:
            log += f"\n<b>Reason:</b> {reason}"

        return log

    else:
        message.reply_text("Well Damn, I Can't Kick That User.")

    return log_message


@run_async
@bot_admin
@can_restrict
def kickme(update: Update, context: CallbackContext):
    user_id = update.effective_message.from_user.id
    if is_user_admin(update.effective_chat, user_id):
        update.effective_message.reply_text("I Wish I Could, But You've An Admin.")
        return

    res = update.effective_chat.unban_member(user_id)  # unban on current user = kick
    if res:
        update.effective_message.reply_text("*Kicks You Out Of The Group*")
    else:
        update.effective_message.reply_text("Huh? I Can't </>")


@run_async
@connection_status
@bot_admin
@can_restrict
@user_admin
@user_can_ban
@loggable
def unban(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    log_message = ""
    bot, args = context.bot, context.args
    user_id, reason = extract_user_and_text(message, args)

    if not user_id:
        message.reply_text("I Doubt That's A User.")
        return log_message

    try:
        member = chat.get_member(user_id)
    except BadRequest as excp:
        if excp.message != "User Not Found":
            raise
        message.reply_text("I Can't Seem To Find This User.")
        return log_message
    if user_id == bot.id:
        message.reply_text("How Would I Unban Myself if I Wasn't Here?")
        return log_message

    if is_user_in_chat(chat, user_id):
        message.reply_text("Isn't This Person Already Here?")
        return log_message

    chat.unban_member(user_id)
    message.reply_text("Yep, This User Can Join 🥳!")

    log = (
        f"<b>{html.escape(chat.title)}:</b>\n"
        f"Unbanned\n"
        f"<b>Unbanned By:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
        f"<b>User:</b> {mention_html(member.user.id, html.escape(member.user.first_name))}"
    )
    if reason:
        log += f"\n<b>Reason:</b> {reason}"

    return log


@run_async
@connection_status
@bot_admin
@can_restrict
@gloggable
def selfunban(context: CallbackContext, update: Update) -> str:
    message = update.effective_message
    user = update.effective_user
    bot, args = context.bot, context.args
    if user.id not in DRAGONS or user.id not in TIGERS:
        return

    try:
        chat_id = int(args[0])
    except:
        message.reply_text("Give A Valid Chat ID.")
        return

    chat = bot.getChat(chat_id)

    try:
        member = chat.get_member(user.id)
    except BadRequest as excp:
        if excp.message == "User Not Found":
            message.reply_text("I Can't Seem To Find This User.")
            return
        else:
            raise

    if is_user_in_chat(chat, user.id):
        message.reply_text("Aren't You Akready In The Chat?")
        return

    chat.unban_member(user.id)
    message.reply_text("Yep, I Have Unbanned You 🥳.")

    log = (
        f"<b>{html.escape(chat.title)}:</b>\n"
        f"Unbanned\n"
        f"<b>Unbanned By:</b> {mention_html(user.id, user.first_name)}\n"
        f"<b>User:</b> {mention_html(member.user.id, html.escape(member.user.first_name))}"
    )

    return log


__help__ = """
 ❍ /kickme*:* kicks the user who issued the command

*𝗢𝗻𝗹𝘆 𝗔𝗱𝗺𝗶𝗻𝘀:*
 ❍ /ban <userhandle>*:* bans a user. (via handle, or reply)
 ❍ /sban <userhandle>*:* Silently ban a user. Deletes command, Replied message and doesn't reply. (via handle, or reply)
 ❍ /tban <userhandle> x(m/h/d)*:* bans a user for `x` time. (via handle, or reply). `m` = `minutes`, `h` = `hours`, `d` = `days`.
 ❍ /unban <userhandle>*:* unbans a user. (via handle, or reply)
 ❍ /kick <userhandle>*:* kicks a user out of the group, (via handle, or reply)

❏ 𝗣𝗼𝘄𝗲𝗿𝗲𝗱 𝗕𝘆
┗ @MaximXRobot
"""

BAN_HANDLER = CommandHandler(["ban", "sban"], ban)
TEMPBAN_HANDLER = CommandHandler(["tban"], temp_ban)
KICK_HANDLER = CommandHandler("kick", kick)
UNBAN_HANDLER = CommandHandler("unban", unban)
ROAR_HANDLER = CommandHandler("roar", selfunban)
KICKME_HANDLER = DisableAbleCommandHandler("kickme", kickme, filters=Filters.group)

dispatcher.add_handler(BAN_HANDLER)
dispatcher.add_handler(TEMPBAN_HANDLER)
dispatcher.add_handler(KICK_HANDLER)
dispatcher.add_handler(UNBAN_HANDLER)
dispatcher.add_handler(ROAR_HANDLER)
dispatcher.add_handler(KICKME_HANDLER)

__mod_name__ = "Bᴀɴs​"
__handlers__ = [
    BAN_HANDLER,
    TEMPBAN_HANDLER,
    KICK_HANDLER,
    UNBAN_HANDLER,
    ROAR_HANDLER,
    KICKME_HANDLER,
]
