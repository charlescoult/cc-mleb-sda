#!/usr/bin/env python3
import sys
import urllib

from yt_dlp import YoutubeDL


def make_url ( base_url, params ):
    return '%s?%s' % ( base_url, urllib.parse.urlencode( params ) )

def main( params ):

    if not len( params ): return 0

    yt_watch_url = 'https://youtube.com/watch/'
    videoID = params[0]
    params = {
        'v': videoID,
    }

    url = make_url( yt_watch_url, params )

    ydl_opts = {
        'format': 'bestaudio',
        'writeautomaticsub': True,
    }

    with YoutubeDL( ydl_opts ) as ydl:
        ydl.download( [
            url,
        ] )



if __name__ == '__main__':
    sys.exit( main( sys.argv[1:] ) )
