from ast import Add, BinOp, BitXor, Div, Mult, Num, Pow, Sub, UnaryOp, USub, parse
from datetime import datetime
from getpass import getuser
from operator import add, mul, neg, pow, sub, truediv, xor
from shutil import which

from pyrogram.raw.functions.help import GetNearestDc
from riobot import ALIVE_MSG, BOT_VERSION, CHANNEL, HELP, HOSTNAME, USER
from riobot.modules.ecem import ecem
from rionify.core import (
    edit,
    extract_args,
    get_translation,
    reply,
    reply_doc,
    riobot,
    send_log,
)

# ================= CONSTANT =================
CUSTOM_MSG = ALIVE_MSG or f"`{get_translation('sedenAlive')}`"
# ============================================


@riobot(pattern='^.neofetch$')
def neofetch(message):
    try:
        from subprocess import PIPE, Popen

        process = Popen(
            ['neofetch', f'HOSTNAME={HOSTNAME}', f'USER={USER}', '--stdout'],
            stdout=PIPE,
            stderr=PIPE,
        )
        result, _ = process.communicate()
        edit(message, f'`{result.decode()}`')
    except BaseException:
        edit(message, f'`{get_translation("neofetchNotFound")}`')


@riobot(pattern='^.botver$')
def bot_version(message):
    if which('git'):
        from subprocess import PIPE, Popen

        changes = Popen(
            ['git', 'rev-list', '--all', '--count'],
            stdout=PIPE,
            stderr=PIPE,
            universal_newlines=True,
        )
        result, _ = changes.communicate()

        edit(
            message,
            get_translation(
                'sedenShowBotVersion',
                ['**', '`', CHANNEL, BOT_VERSION, result],
            ),
            preview=False,
        )
    else:
        edit(message, f'`{get_translation("rioGitNotFound")}`')


@riobot(pattern='^.ping$')
def ping(message):
    start = datetime.now()
    edit(message, '**Pong!**')
    finish = datetime.now()
    time = (finish - start).microseconds / 1000
    edit(message, f'**Pong!**\n`{time}ms`')


@riobot(pattern='^.alive$')
def alive(message):
    if CUSTOM_MSG.lower() == 'ecem':
        ecem(message)
        return
    edit(message, f'{CUSTOM_MSG}')


@riobot(pattern='^.echo')
def test_echo(message):
    args = extract_args(message)
    if len(args) > 0:
        message.delete()
        reply(message, args)
    else:
        edit(message, f'`{get_translation("echoHelp")}`')


@riobot(pattern='^.dc$', compat=False)
def data_center(client, message):
    result = client.invoke(GetNearestDc())

    edit(
        message,
        get_translation(
            'rioNearestDC',
            ['**', '`', result.country, result.nearest_dc, result.this_dc],
        ),
    )


@riobot(pattern='^.term')
def terminal(message):
    command = extract_args(message)

    if len(command) < 1:
        edit(message, f'`{get_translation("termUsage")}`')
        return

    curruser = getuser()
    try:
        from os import geteuid

        uid = geteuid()
    except ImportError:
        uid = 0

    if not command:
        edit(message, f'`{get_translation("termHelp")}`')
        return

    result = get_translation("termNoResult")
    try:
        from sedenecem.core.misc import __status_out__

        _, result = __status_out__(command)
    except BaseException as e:
        pass

    if len(result) > 4096:
        output = open('output.txt', 'w+')
        output.write(result)
        output.close()
        reply_doc(
            message,
            'output.txt',
            caption=f'`{get_translation("outputTooLarge")}`',
            delete_after_send=True,
        )
        return

    edit(message, f'`{curruser}:~{"#" if uid == 0 else "$"} {command}\n{result}`')

    send_log(get_translation('termLog', [command]))


@riobot(pattern='^.eval')
def eval(message):
    args = extract_args(message)
    if len(args) < 1:
        edit(message, f'`{get_translation("evalUsage")}`')
        return

    try:
        evaluation = safe_eval(args)
        if evaluation:
            if isinstance(evaluation, str):
                if len(evaluation) >= 4096:
                    file = open('output.txt', 'w+')
                    file.write(evaluation)
                    file.close()
                    reply_doc(
                        message,
                        'output.txt',
                        caption=f'`{get_translation("outputTooLarge")}`',
                        delete_after_send=True,
                    )
                    return
                edit(
                    message,
                    get_translation('rioQuery', ['**', '`', args, evaluation]),
                )
        else:
            edit(
                message,
                get_translation(
                    'rioQuery', ['**', '`', args, get_translation('sedenErrorResult')]
                ),
            )
    except Exception as err:
        edit(message, get_translation('sedenQuery', ['**', '`', args, str(err)]))

    send_log(get_translation('evalLog', [args]))


operators = {
    Add: add,
    Sub: sub,
    Mult: mul,
    Div: truediv,
    Pow: pow,
    BitXor: xor,
    USub: neg,
}


def safe_eval(expr):
    expr = expr.lower().replace('x', '*').replace(' ', '')
    return str(_eval(parse(expr, mode='eval').body))


def _eval(node):
    if isinstance(node, Num):
        return node.n
    elif isinstance(node, BinOp):
        return operators[type(node.op)](_eval(node.left), _eval(node.right))
    elif isinstance(node, UnaryOp):
        return operators[type(node.op)](_eval(node.operand))
    else:
        raise TypeError(f'`{get_translation("safeEval")}`')


HELP.update({'system': get_translation('systemInfo')})
