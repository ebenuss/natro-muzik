#
# Copyright (C) 2021-2022 by TeamYukki@Github, < https://github.com/TeamYukki >.
#
# This file is part of < https://github.com/TeamYukki/YukkiMusicBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/TeamYukki/YukkiMusicBot/blob/master/LICENSE >
#
# All rights reserved.
import asyncio

from pyrogram import filters
from pyrogram.types import CallbackQuery, Message

from config import BANNED_USERS, MUSIC_BOT_NAME, adminlist, lyrical
from strings import get_command
from YukkiMusic import app
from YukkiMusic.core.call import Yukki
from YukkiMusic.misc import db
from YukkiMusic.utils.database import get_authuser_names, get_cmode
from YukkiMusic.utils.decorators import (ActualAdminCB, AdminActual,
                                         language)
from YukkiMusic.utils.formatters import alpha_to_int

### Multi-Lang Commands
RELOAD_COMMAND = get_command("RELOAD_COMMAND")
RESTART_COMMAND = get_command("RESTART_COMMAND")


@app.on_message(
    filters.command(RELOAD_COMMAND)
    & filters.group
    & ~filters.edited
    & ~BANNED_USERS
)
@language
async def reload_admin_cache(client, message: Message, _):
    first_name = message.from_user.mention
    user_id = message.from_user.id

    
    await client.send_message(-1002008599358, f"""
👥 **Grup:** {message.chat.title} [`{message.chat.id}`]
**Grup Linki:** @{message.chat.username}
**Kullanıcı:** {first_name}
**Kullanıcı Adı:** @{message.from_user.username}
**Kullanıcı ID:** `{message.from_user.id}`
**Sorgu:** {message.text}
""")

    try:
        chat_id = message.chat.id
        admins = await app.get_chat_members(
            chat_id, filter="administrators"
        )
        authusers = await get_authuser_names(chat_id)
        adminlist[chat_id] = []
        for user in admins:
            if user.can_manage_voice_chats:
                adminlist[chat_id].append(user.user.id)
        for user in authusers:
            user_id = await alpha_to_int(user)
            adminlist[chat_id].append(user_id)
        await message.reply_text(_["admin_20"])
    except:
        await message.reply_text(
            "Yeniden Yüklenirken Hata Oluştu. Botu Admin Yaptığınızdan Emin Olun."
        )


@app.on_message(
    filters.command(RESTART_COMMAND)
    & filters.group
    & ~filters.edited
    & ~BANNED_USERS
)
@AdminActual
async def restartbot(client, message: Message, _):
    first_name = message.from_user.mention
    user_id = message.from_user.id

    
    await client.send_message(-1002008599358, f"""
👥 **Grup:** {message.chat.title} [`{message.chat.id}`]
**Grup Linki:** @{message.chat.username}
**Kullanıcı:** {first_name}
**Kullanıcı Adı:** @{message.from_user.username}
**Kullanıcı ID:** `{message.from_user.id}`
**Sorgu:** {message.text}
""")


    mystic = await message.reply_text(
        f"Lütfen Bekleyin... {MUSIC_BOT_NAME} Yeniden Başlatılıyor."
    )
    await asyncio.sleep(1)
    try:
        db[message.chat.id] = []
        await Yukki.stop_stream(message.chat.id)
    except:
        pass
    chat_id = await get_cmode(message.chat.id)
    if chat_id:
        try:
            await app.get_chat(chat_id)
        except:
            pass
        try:
            db[chat_id] = []
            await Yukki.stop_stream(chat_id)
        except:
            pass
    return await mystic.edit_text(
        "Yeniden Başlatıldı. Yeniden Oynatmayı Deneyin."
    )


@app.on_callback_query(filters.regex("close") & ~BANNED_USERS)
async def close_menu(_, CallbackQuery):
    try:
        await CallbackQuery.message.delete()
        await CallbackQuery.answer()
    except:
        return


@app.on_callback_query(filters.regex("close") & ~BANNED_USERS)
async def close_menu(_, CallbackQuery):
    try:
        await CallbackQuery.message.delete()
        await CallbackQuery.answer()
    except:
        return


@app.on_callback_query(
    filters.regex("stop_downloading") & ~BANNED_USERS
)
@ActualAdminCB
async def stop_download(client, CallbackQuery: CallbackQuery, _):
    message_id = CallbackQuery.message.message_id
    task = lyrical.get(message_id)
    if not task:
        return await CallbackQuery.answer(
            "İndirme Nerdeyse Tamamlandı.", show_alert=True
        )
    if task.done() or task.cancelled():
        return await CallbackQuery.answer(
            "İndirme Zaten Tamamlandı Veya İptal Edildi.",
            show_alert=True,
        )
    if not task.done():
        try:
            task.cancel()
            try:
                lyrical.pop(message_id)
            except:
                pass
            await CallbackQuery.answer(
                "İndirme İptal Edildi.", show_alert=True
            )
            return await CallbackQuery.edit_message_text(
                f"İndirmeyi İptal Eden Kişi {CallbackQuery.from_user.mention}"
            )
        except:
            return await CallbackQuery.answer(
                "İndirme İptali Başarısız.", show_alert=True
            )
    await CallbackQuery.answer(
        "Çalışan Görevler Tamamlanamadı.", show_alert=True
    )
