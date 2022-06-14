from json import JSONDecodeError

from pyrogram import enums
from requests import get
from riobot import HELP
from rionify.core import edit, get_translation, riobot


def parseShipEntity(jsonEntity: dict) -> str:

    text = get_translation(
        'shippingResult',
        [
            '<b>',
            '</b>',
            '<code>',
            '</code>',
            jsonEntity['data']['company'].title(),
            jsonEntity['data']['tracking_no'],
            jsonEntity['data']['status'],
            jsonEntity['data']['sender_name'],
            jsonEntity['data']['receiver_name'],
            jsonEntity['data']['sender_unit'],
            jsonEntity['data']['receiver_unit'],
            jsonEntity['data']['sended_date'],
            jsonEntity['data']['delivered_date'] or get_translation('notFound'),
            '<u>',
            '</u>',
        ],
    )
    if jsonEntity['data']['movements']:
        movements = get_translation(
            'shippingMovements',
            [
                '<code>',
                '</code>',
                jsonEntity['data']['movements'][0]['unit'],
                jsonEntity['data']['movements'][0]['status'],
                jsonEntity['data']['movements'][0]['date'],
                jsonEntity['data']['movements'][0]['time'],
                jsonEntity['data']['movements'][0]['action'],
            ],
        )
        text += movements

    return text


def getShipEntity(company: str, trackId: int or str) -> dict or None:
    headers: dict = {
        'platform': 'Android',
        'public': 'lfJGmU9XpGZcMwyLtZBk',
        'secret': 'sMPMnQuc51nmcBbaeOK1',
        'unique': 'afb612018716663e',
    }
    response = get(f"https://tapi.kolibu.com/{company}/{trackId}", headers=headers)
    try:
        return response.json() if response.json()['success'] else None
    except JSONDecodeError:
        return None


@riobot(pattern='^.(rio|aras|ptt|mng|ups|surat|trendyol|hepsiburada)')
def shippingTrack(message):
    edit(message, f"`{get_translation('processing')}`")
    argv = message.text.split(' ')
    if len(argv) > 2:
        edit(message, f"`{get_translation('wrongCommand')}`")
        return

    try:
        comp, trackId = argv
    except ValueError:
        return edit(message, f"`{get_translation('wrongCommand')}`")

    if not trackId:
        edit(message, f"`{get_translation('wrongCommand')}`")
        return
    if comp == '.yurtici':
        kargo_data = getShipEntity(company="yurtici", trackId=trackId)
    if comp == '.aras':
        kargo_data = getShipEntity(company="aras", trackId=trackId)
    if comp == '.ptt':
        kargo_data = getShipEntity(company="ptt", trackId=trackId)
    if comp == '.mng':
        kargo_data = getShipEntity(company="mng", trackId=trackId)
    if comp == '.ups':
        kargo_data = getShipEntity(company="ups", trackId=trackId)
    if comp == '.surat':
        kargo_data = getShipEntity(company="surat", trackId=trackId)
    if comp == '.trendyol':
        kargo_data = getShipEntity(company="trendyolexpress", trackId=trackId)
    if comp == '.hepsiburada':
        kargo_data = getShipEntity(company="hepsijet", trackId=trackId)
    if kargo_data:
        text = parseShipEntity(kargo_data)
        edit(message, text, parse=enums.ParseMode.HTML)
        return
    edit(message, f"`{get_translation('shippingNoResult')}`")


HELP.update({'shippingtrack': get_translation("shippingTrack")})
