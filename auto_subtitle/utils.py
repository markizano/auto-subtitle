import os
from typing import Iterator, TextIO
from kizano import getLogger
log = getLogger(__name__)

def str2bool(string):
    string = string.lower()
    str2val = {"true": True, "false": False}

    if string in str2val:
        return str2val[string]
    else:
        raise ValueError(
            f"Expected one of {set(str2val.keys())}, got {string}")


def format_timestamp(seconds: float, always_include_hours: bool = False):
    assert seconds >= 0, "non-negative timestamp expected"
    milliseconds = round(seconds * 1000.0)

    hours = milliseconds // 3_600_000
    milliseconds -= hours * 3_600_000

    minutes = milliseconds // 60_000
    milliseconds -= minutes * 60_000

    seconds = milliseconds // 1_000
    milliseconds -= seconds * 1_000

    hours_marker = f"{hours}:" if always_include_hours or hours > 0 else ""
    return f"{hours_marker}{minutes:02d}:{seconds:02d}.{milliseconds:03d}"


def write_srt(transcript: Iterator[dict], file: TextIO):
    i = 1
    srt_tpl = '%d\n%s --> %s\n%s\n\n'
    for segment in transcript:
        # log.debug(segment)
        buffer = []
        for word in segment['words']:
            buffer.append(word)
            text = ''.join([ x['word'] for x in buffer ]).strip().replace('-->', '->')
            charlen = len(text)
            stime = format_timestamp(buffer[0]['start'], always_include_hours=True)
            etime = format_timestamp(buffer[-1]['end'], always_include_hours=True)
            if len(buffer) > 5 or charlen > 32:
                file.write( srt_tpl % ( i, stime, etime, text ) )
                i += 1
                buffer = []
        if len(buffer) > 0:
            file.write( srt_tpl % ( i, stime, etime, text ) )
            i += 1
    file.flush()


def filename(path):
    return os.path.splitext(os.path.basename(path))[0]
