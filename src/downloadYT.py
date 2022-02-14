#!/usr/bin/env python3
import sys
import urllib
import json
import os

from yt_dlp import YoutubeDL


def make_url ( base_url, params ):
    return '%s?%s' % ( base_url, urllib.parse.urlencode( params ) )

def downloadAudio( videoId ):

    if not len( videoId ): return 0

    yt_watch_url = 'https://youtube.com/watch/'
    params = {
        'v': videoId,
    }

    url = make_url( yt_watch_url, params )

    ydl_opts = {
        'format': 'bestaudio',
        'writeautomaticsub': True,
        'writeinfojson': True,
        "outtmpl": {
            "default": ( "data/%s" % videoId ) + ".%(ext)s",
        },
        "postprocessors": [
            {
                "key": "Exec",
                "when": "after_move",
                "exec_cmd": "echo",
            },
        ],
    }

    with YoutubeDL( ydl_opts ) as ydl:
        ydl.download( [
            url,
        ] )

if __name__ == '__main__':
    for videoId in sys.argv[1:]:
        downloadAudio( videoId )
    sys.exit()
