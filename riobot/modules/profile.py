from os import remove
from time import sleep

from PIL import Image
from pyrogram import enums
from pyrogram.errors import UsernameOccupied
from pyrogram.raw.functions.account import UpdateProfile, UpdateStatus, UpdateUsername
from pyrogram.raw.functions.channels import GetAdminedPublicChannels
from riobot import HELP, TEMP_SETTINGS
from rionify.core import (
    download_media_wc,
    edit,
    extract_args,
    get_download_dir,
    get_translation,
    riobot,
    send_log,
)

# ====================== CONSTANT ===============================
ALWAYS_ONLINE = 'offline'
# ===============================================================


@riobot(pattern='^.reserved$', compat=False)
def reserved(client, message):
    sonuc = client.invoke(GetAdminedPublicChannels())
    mesaj = ''
    for channel_obj in sonuc.chats:
        mesaj += f'{channel_obj.title}\n@{channel_obj.username}\n\n'
    edit(message, mesaj)


@riobot(pattern='^.name', compat=False)
def name(client, message):
    newname = extract_args(message)
    if ' ' not in newname:
        firstname = newname
        lastname = ''
    else:
        namesplit = newname.split(' ', 1)
        firstname = namesplit[0]
        lastname = namesplit[1]

    client.invoke(UpdateProfile(first_name=firstname, last_name=lastname))
    edit(message, f'`{get_translation("nameOk")}`')


@riobot(pattern='^.setpfp$', compat=False)
def set_profilepic(client, message):
    reply = message.reply_to_message
    photo = None
    if (
        reply
        and reply.media
        and (
            reply.photo
            or (reply.sticker and not reply.sticker.is_animated)
            or (reply.document and 'image' in reply.document.mime_type)
        )
    ):
        photo = download_media_wc(reply, 'profile_photo.jpg')
    else:
        edit(message, f'`{get_translation("mediaInvalid")}`')

    if photo:
        image = Image.open(photo)
        width, height = image.size
        maxSize = (640, 640)
        ratio = min(maxSize[0] / width, maxSize[1] / height)
        image = image.resize((int(width * ratio), int(height * ratio)))
        new_photo = f'{get_download_dir()}/profile_photo_new.png'
        image.save(new_photo)
        client.set_profile_photo(photo=new_photo)
        remove(photo)
        remove(new_photo)
        edit(message, f'`{get_translation("ppChanged")}`')
    else:
        edit(message, f'`{get_translation("ppError")}`')


@riobot(pattern='^.delpfp', compat=False)
def remove_profilepic(client, message):
    group = extract_args(message)
    if group == 'all':
        lim = 0
    elif group.isdigit():
        lim = int(group)
    else:
        lim = 1

    count = 0
    for photo in client.get_chat_photos('me', limit=lim):
        client.delete_profile_photos(photo.file_id)
        count += 1
    edit(message, f'`{get_translation("ppDeleted", [count])}`')


@riobot(pattern='^.setbio', compat=False)
def setbio(client, message):
    newbio = extract_args(message)
    client.invoke(UpdateProfile(about=newbio))
    edit(message, f'`{get_translation("bioSuccess")}`')


@riobot(pattern='^.username', compat=False)
def username(client, message):
    newusername = extract_args(message)
    try:
        client.invoke(UpdateUsername(username=newusername))
        edit(message, f'`{get_translation("usernameSuccess")}`')
    except UsernameOccupied:
        edit(message, f'`{get_translation("usernameTaken")}`')


@riobot(pattern='^.block$', compat=False)
def blockpm(client, message):
    if message.reply_to_message:
        reply = message.reply_to_message
        replied_user = reply.from_user
        if replied_user.is_self:
            edit(message, f'`{get_translation("cannotBlockMyself")}`')
            return
        aname = replied_user.id
        name0 = str(replied_user.first_name)
        uid = replied_user.id
    else:
        aname = message.chat
        if not aname.type == enums.ChatType.PRIVATE:
            edit(message, f'`{get_translation("pmApproveError")}`')
            return
        name0 = aname.first_name
        uid = aname.id

    client.block_user(uid)

    edit(message, f'`{get_translation("pmBlocked")}`')

    try:
        from sedenecem.sql.pm_permit_sql import dissprove

        dissprove(uid)
    except BaseException:
        pass

    send_log(get_translation('pmBlockedLog', [name0, uid]))


@riobot(pattern='^.unblock$', compat=False)
def unblockpm(client, message):
    if message.reply_to_message:
        reply = message.reply_to_message
        replied_user = reply.from_user
        if replied_user.is_self:
            edit(message, f'`{get_translation("cannotUnblockMyself")}`')
            return
        name0 = str(replied_user.first_name)
        uid = replied_user.id
        client.unblock_user(uid)
        edit(message, f'`{get_translation("pmUnblocked")}`')

        send_log(get_translation('pmUnblockedLog', [name0, replied_user.id]))
    else:
        edit(message, f'`{get_translation("pmUnblockedUsage")}`')


@riobot(pattern='^.online', compat=False)
def online(client, message):
    args = extract_args(message)
    offline = ALWAYS_ONLINE in TEMP_SETTINGS
    if args == 'disable':
        if offline:
            del TEMP_SETTINGS[ALWAYS_ONLINE]
            edit(message, f'`{get_translation("alwaysOnlineOff")}`')
            return
        else:
            edit(message, f'`{get_translation("alwaysOnlineOff2")}`')
            return
    elif offline:
        edit(message, f'`{get_translation("alwaysOnline2")}`')
        return

    TEMP_SETTINGS[ALWAYS_ONLINE] = True

    edit(message, f'`{get_translation("alwaysOnline")}`')

    while ALWAYS_ONLINE in TEMP_SETTINGS:
        try:
            client.invoke(UpdateStatus(offline=False))
            sleep(5)
        except BaseException:
            return


@riobot(pattern='^.stats$', compat=False)
def user_stats(client, message):
    edit(message, f'`{get_translation("processing")}`')
    chats = 0
    channels = 0
    groups = 0
    sgroups = 0
    pms = 0
    bots = 0
    unread = 0
    user = []
    for i in client.get_dialogs():
        chats += 1
        if i.chat.type == enums.ChatType.CHANNEL:
            channels += 1
        elif i.chat.type == enums.ChatType.GROUP:
            groups += 1
        elif i.chat.type == enums.ChatType.SUPERGROUP:
            sgroups += 1
        else:
            pms += 1
            user.append(i.chat.id)

        if i.unread_messages_count > 0:
            unread += 1

    users = client.get_users(user)
    for i in users:
        if i.is_bot:
            bots += 1

    edit(
        message,
        get_translation(
            'statsResult',
            ['**', '`', chats, channels, groups, sgroups, bots, pms, unread],
        ),
    )


HELP.update({'profile': get_translation('profileInfo')})
