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

    index_fn = "data/index.json"

    # Update data/index.json

    # ensure file exists and is readable and create it if not
    if not ( os.path.isfile( index_fn ) and os.access( index_fn, os.R_OK ) ):
        with open( index_fn, 'w+' ) as index_file:
            json.dump( {
                'files': [],
            }, index_file, indent = 4 )

    # Read existing
    with open( index_fn, 'r' ) as index_file:
        index_data = json.load( index_file )

    # if existing data already contains this file, delete the old before adding
    # the new metadata
    index_data["files"] = list( filter( lambda a: a["yt_id"] != videoId, index_data["files"] ) )

    # add the new metadata
    index_data["files"].append( {
        "name": "",
        "yt_id": videoId,
        "filename": "",
        "subtitle": "",
        "processing": [],
    } )

    # Overwrite existing file with new file with modified data
    with open( "data/index.json", "w" ) as index:
        json.dump( index_data, index, indent = 4 )

if __name__ == '__main__':
    for videoId in sys.argv[1:]:
        downloadAudio( videoId )
    sys.exit()
