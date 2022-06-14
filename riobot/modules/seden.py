from collections import OrderedDict

from riobot import HELP
from rionify.core import edit, extract_args, get_translation, reply, riobot


@riobot(pattern='^.(seden|help)')
def seden(message):
    seden = extract_args(message).lower()
    cmds = OrderedDict(sorted(HELP.items()))
    if len(seden) > 0:
        if seden in cmds:
            edit(message, str(cmds[seden]))
        else:
            edit(message, f'**{get_translation("sedenUsage")}**')
    else:
        edit(message, get_translation('sedenUsage2', ['**', '`']))
        metin = f'{get_translation("sedenShowLoadedModules", ["**", "`", len(cmds)])}\n'
        for item in cmds:
            metin += f'• `{item}`\n'
        reply(message, metin)
