from pyrogram.errors import YouBlockedUser
from riobot import HELP
from rionify.core import PyroConversation, edit, get_translation, riobot


@riobot(pattern='^.sangmata$', compat=False)
def sangmata(client, message):
    reply = message.reply_to_message
    if reply and reply.text:
        edit(message, f'`{get_translation("processing")}`')
    else:
        edit(message, f'`{get_translation("replyMessage")}`')
        return

    chat = 'SangMataInfo_bot'

    with PyroConversation(client, chat) as conv:
        response = None
        try:
            conv.forward_msg(reply)
            response = conv.recv_msg()
        except YouBlockedUser:
            edit(message, get_translation('unblockChat', ['**', '`', chat]))
            return
        except Exception as e:
            raise e

        if not response:
            edit(message, f'`{get_translation("answerFromBot")}`')
        elif 'Forward' in response.text:
            edit(message, f'`{get_translation("privacySettings")}`')
        else:
            edit(message, response.text)


HELP.update({'sangmata': get_translation('sangmataInfo')})
