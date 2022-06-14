from time import sleep

from riobot import HELP, LOGS
from rionify.core import edit, extract_args, get_translation, riobot, send_log


def chat_init():
    try:
        global sql
        from importlib import import_module

        sql = import_module('rionify.sql.keep_read_sql')
    except Exception as e:
        sql = None
        LOGS.warn(get_translation('chatSqlLog'))
        raise e


chat_init()


@riobot(pattern='^.unmutechat$')
def unmutechat(message):
    try:
        from sedenecem.sql.keep_read_sql import unkread
    except BaseException:
        edit(message, f'`{get_translation("nonSqlMode")}`')
        return
    status = unkread(str(message.chat.id))
    if status:
        edit(message, f'`{get_translation("chatUnmuted")}`')
    else:
        edit(message, f'`{get_translation("chatAlreadyUnmuted")}`')
    sleep(2)
    message.delete()


@riobot(pattern='^.mutechat$')
def mutechat(message):
    try:
        from sedenecem.sql.keep_read_sql import kread
    except BaseException:
        edit(message, f'`{get_translation("nonSqlMode")}`')
        return
    status = kread(str(message.chat.id))
    if status:
        edit(message, f'`{get_translation("chatMuted")}`')
    else:
        edit(message, f'`{get_translation("chatAlreadyMuted")}`')
    sleep(2)
    message.delete()

    send_log(get_translation('chatLog', [message.chat.id]))


@riobot(incoming=True, compat=False)
def keep_read(client, message):
    if message.from_user and message.from_user.is_self:
        message.continue_propagation()

    try:
        from sedenecem.sql.keep_read_sql import is_kread
    except BaseException:
        return

    if is_muted(message.chat.id):
        client.read_chat_history(message.chat.id)

    message.continue_propagation()


@riobot(pattern='^.call')
def call_notes(message):
    try:
        from sedenbot.modules.notes import get_note
        from sedenbot.modules.snips import get_snip
    except BaseException:
        edit(message, f'`{get_translation("nonSqlMode")}`')
        return

    args = extract_args(message)
    if args.startswith('#'):
        get_note(message)
    elif args.startswith('$'):
        get_snip(message)
    else:
        edit(message, f"`{get_translation('wrongCommand')}`")


def is_muted(chat_id):
    try:
        from sedenecem.sql.keep_read_sql import is_kread
    except BaseException:
        return False

    kread = is_kread()
    if kread:
        for i in kread:
            if i.groupid == str(chat_id):
                return True

    return False


HELP.update({'chat': get_translation('chatInfo')})
HELP.update({'call': get_translation('callInfo')})
