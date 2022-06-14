from requests import get
from riobot import HELP, SEDEN_LANG, WEATHER
from rionify.core import edit, extract_args, get_translation, riobot

# ===== CONSTANT =====
if WEATHER:
    DEFCITY = WEATHER
else:
    DEFCITY = None
# ====================


@riobot(pattern='^.(havadurumu|w(eathe|tt)r)')
def havadurumu(message):
    args = extract_args(message)

    if len(args) < 1:
        CITY = DEFCITY
        if not CITY:
            edit(message, f'`{get_translation("weatherErrorCity")}`')
            return
    else:
        CITY = args

    if ',' in CITY:
        CITY = CITY[: CITY.find(',')].strip()

    try:
        req = get(
            f'http://wttr.in/{CITY}?mqT0',
            headers={'User-Agent': 'curl/7.66.0', 'Accept-Language': SEDEN_LANG},
        )
        data = req.text
        if '===' in data:
            raise Exception
        data = data.replace('`', '‛')
        edit(message, f'`{data}`')
    except Exception:
        edit(message, f'`{get_translation("weatherErrorServer")}`')


HELP.update({'weather': get_translation('infoWeather')})
