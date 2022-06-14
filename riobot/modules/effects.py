from os import path, remove
from subprocess import Popen

from riobot import HELP
from rionify.core import (
    download_media_wc,
    edit,
    extract_args,
    get_translation,
    reply_audio,
    reply_video,
    sedenify,
)


@riobot(pattern='^.earrape')
def earrape(message):
    args = extract_args(message).split(' ', 1)
    reply = message.reply_to_message

    util = args[0].lower()
    if util == 'mp4':
        if not (
            reply
            and (
                reply.video
                or reply.video_note
                or (reply.document and 'video' in reply.document.mime_type)
            )
        ):
            edit(message, f'`{get_translation("wrongMedia")}`')
        else:
            edit(message, f'`{get_translation("applyEarrape")}`')
            media = download_media_wc(reply)
            process = Popen(
                [
                    'ffmpeg',
                    '-i',
                    f'{media}',
                    '-af',
                    'acrusher=.1:1:64:0:log',
                    f'{media}.mp4',
                ]
            )
            process.communicate()
            edit(message, f'`{get_translation("uploadMedia")}`')
            reply_video(reply or message, f'{media}.mp4', delete_file=True)
            remove(media)
            message.delete()
    elif util == 'mp3':
        if not (
            reply
            and (
                reply.video
                or reply.video_note
                or (
                    reply.audio
                    or reply.voice
                    or (reply.document and 'video' in reply.document.mime_type)
                )
            )
        ):
            edit(message, f'`{get_translation("wrongMedia")}`')
        else:
            edit(message, f'`{get_translation("applyEarrape")}`')
            media = download_media_wc(reply)
            process = Popen(
                [
                    'ffmpeg',
                    '-i',
                    f'{media}',
                    '-af',
                    'acrusher=.1:1:64:0:log',
                    f'{media}.mp3',
                ]
            )
            process.communicate()
            edit(message, f'`{get_translation("uploadMedia")}`')
            reply_audio(reply or message, f'{media}.mp3', delete_file=True)
            remove(media)
            message.delete()
    else:
        edit(message, f'`{get_translation("wrongCommand")}`')
        return


@riobot(pattern='^.nightcore$')
def nightcore(message):
    # Copyright (c) @kisekinopureya | 2021
    reply = message.reply_to_message

    if not (
        reply
        and (
            reply.audio
            or reply.voice
            or (reply.document and 'audio' in reply.document.mime_type)
        )
    ):
        edit(message, f'`{get_translation("wrongMedia")}`')
    else:
        edit(message, f'`{get_translation("applyNightcore")}`')
        media = download_media_wc(reply)

        filename = f'{media}.mp3'
        if path.exists(filename):
            remove(filename)

        process = Popen(
            [
                'ffmpeg',
                '-i',
                media,
                '-af',
                'asetrate=44100*1.16,aresample=44100,atempo=1',
                filename,
            ]
        )
        process.communicate()
        edit(message, f'`{get_translation("uploadMedia")}`')
        reply_audio(reply or message, f'{media}.mp3', delete_file=True)
        remove(media)
        message.delete()


@riobot(pattern='^.slowedtoperfection$')
def slowedtoperfection(message):
    # Copyright (c) @kisekinopureya | 2021
    reply = message.reply_to_message

    if not (
        reply
        and (
            reply.audio
            or reply.voice
            or (reply.document and 'audio' in reply.document.mime_type)
        )
    ):
        edit(message, f'`{get_translation("wrongMedia")}`')
    else:
        edit(message, f'`{get_translation("applySlowedtoperfection")}`')
        media = download_media_wc(reply)

        filename = f'{media}.mp3'
        if path.exists(filename):
            remove(filename)

        process = Popen(
            [
                'ffmpeg',
                '-i',
                media,
                '-af',
                'aecho=1.0:0.7:20:0.5,asetrate=44100*0.84,aresample=44100,atempo=1',
                filename,
            ]
        )
        process.communicate()
        edit(message, f'`{get_translation("uploadMedia")}`')
        reply_audio(reply or message, f'{media}.mp3', delete_file=True)
        remove(media)
        message.delete()


HELP.update({'effects': get_translation('effectsInfo')})
