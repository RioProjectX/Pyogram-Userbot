from time import sleep

from pyrogram.errors import FloodWait
from riobot import HELP, TEMP_SETTINGS
from rionify.core import (
    edit,
    extract_args,
    get_translation,
    reply,
    riobot,
    send_log,
)


@riobot(pattern='^.purge$', compat=False, admin=True)
def purge(client, message):
    msg = message.reply_to_message
    if msg:
        itermsg = list(range(msg.id, message.id))
    else:
        edit(message, f'`{get_translation("purgeUsage")}`')
        return

    count = 0

    for i in itermsg:
        try:
            count = count + 1
            client.delete_messages(chat_id=message.chat.id, message_ids=i, revoke=True)
        except FloodWait as e:
            sleep(e.x)
        except Exception as e:
            edit(message, get_translation('purgeError', ['`', '**', e]))
            return

    done = reply(message, get_translation('purgeResult', ['**', '`', str(count)]))
    send_log(get_translation('purgeLog', ['**', '`', str(count)]))
    sleep(2)
    message.delete()
    done.delete()


@riobot(pattern='^.purgeme', compat=False)
def purgeme(client, message):
    me = TEMP_SETTINGS['ME']
    count = extract_args(message)
    if not count.isdigit():
        return edit(message, f'`{get_translation("purgemeUsage")}`')
    i = 1

    itermsg = client.get_chat_history(message.chat.id)
    for message in itermsg:
        if i > int(count) + 1:
            break
        if message.from_user.id == me.id:
            i = i + 1
            message.delete()

    smsg = reply(message, get_translation('purgeResult', ['**', '`', str(count)]))
    send_log(get_translation('purgeLog', ['**', '`', str(count)]))
    sleep(2)
    i = 1
    smsg.delete()


@riobot(pattern='^.del$', compat=False, admin=True)
def delete(client, message):
    msg_src = message.reply_to_message
    if msg_src:
        if msg_src.from_user.id:
            try:
                client.delete_messages(message.chat.id, msg_src.id)
                message.delete()
                send_log(f'`{get_translation("delResultLog")}`')
            except BaseException:
                send_log(f'`{get_translation("delErrorLog")}`')
    else:
        edit(message, f'`{get_translation("wrongCommand")}`')


HELP.update({'purge': get_translation('purgeInfo')})
HELP.update({'purgeme': get_translation('purgemeInfo')})
HELP.update({'del': get_translation('delInfo')})
