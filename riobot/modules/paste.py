from requests import post
from rionify.core import edit, get_translation, riobot


@riobot(pattern="^.paste")
def paste(message):

    text = message.text.strip()
    if len(text) <= 6:
        return edit(message, f'`{get_translation("pasteErr")}`')

    paste = text.replace('.paste ', '').encode('utf-8')

    url = "https://www.toptal.com/developers/hastebin/documents"

    try:
        r = post(
            url=url,
            data=paste,
        )
    except BaseException as e:
        edit(message, f'`{get_translation("pasteConErr")}`')

    try:
        resp = r.json()
        key = resp['key']
        new_url = f"https://www.toptal.com/developers/hastebin/{key}"
        return edit(message, new_url, False)
    except BaseException as e:
        raise e
