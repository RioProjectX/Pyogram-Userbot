from PIL import Image, ImageColor
from riobot import HELP
from rionify.core import edit, extract_args, get_translation, reply_img, riobot


@riobot(pattern='^.color')
def color(message):
    input_str = extract_args(message)

    if input_str.startswith('#'):
        try:
            usercolor = ImageColor.getrgb(input_str)
        except Exception as e:
            edit(message, str(e))
            return False
        else:
            im = Image.new(mode='RGB', size=(1920, 1080), color=usercolor)
            im.save('sedencik.png', 'PNG')
            reply_img(
                message,
                'sedencik.png',
                caption=input_str,
                delete_file=True,
                delete_orig=True,
            )
    else:
        edit(message, f'`{get_translation("colorsUsage")}`')


HELP.update({'color': get_translation('colorsInfo')})
