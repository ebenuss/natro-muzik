#
# Copyright (C) 2021-2022 by TeamYukki@Github, < https://github.com/TeamYukki >.
#
# This file is part of < https://github.com/TeamYukki/YukkiMusicBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/TeamYukki/YukkiMusicBot/blob/master/LICENSE >
#
# All rights reserved.

from config import LOG, LOG_GROUP_ID
from YukkiMusic import app
from YukkiMusic.utils.database import is_on_off
from YukkiMusic.utils.database.memorydatabase import (
    get_active_chats, get_active_video_chats)
from YukkiMusic.utils.database import (get_global_tops,
                                       get_particulars, get_queries,
                                       get_served_chats,
                                       get_served_users, get_sudoers,
                                       get_top_chats, get_topp_users)



async def play_logs(message, streamtype):
    chat_id = message.chat.id
    sayı = await app.get_chat_members_count(chat_id)
    toplamgrup = len(await get_served_chats())
    aktifseslisayısı = len(await get_active_chats())

    if await is_on_off(LOG):
        if message.chat.username:
            chatusername = f"@{message.chat.username}"
        else:
            chatusername = "Gizli Grup"
        logger_text = f"""


**Grup:** {message.chat.title} [`{message.chat.id}`]
**Üye Sayısı: 👉{sayı}**
**Kullanıcı:** {message.from_user.mention}
**Kullanıcı Adı:** @{message.from_user.username}
**Kullanıcı ID:** `{message.from_user.id}`
**Grup Linki:** {chatusername}
**Sorgu:** {message.text}

**Toplam Grup Sayısı: 👉{toplamgrup}**
**Aktif Ses: 👉{aktifseslisayısı}**"""
        if message.chat.id != LOG_GROUP_ID:
            try:
                await app.send_message(
                    LOG_GROUP_ID,
                    f"{logger_text}",
                    disable_web_page_preview=True,
                )
                await app.set_chat_title(LOG_GROUP_ID, f"MÜZİK LOG - {aktifseslisayısı}")
            except:
                pass
        return
