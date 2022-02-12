import os
import sys
from datetime import datetime, timedelta

import webvtt
from pydub import AudioSegment

'''
Assumes file is less than 24 hrs in length.
'''

MS_PAD = 0

def parse_to_ms( timestr ):
    timestr = timestr + '000'
    dt = datetime.strptime( timestr, '%H:%M:%S.%f' )
    td = timedelta( hours = dt.hour, minutes = dt.minute, seconds = dt.second, milliseconds = int( dt.microsecond / 1000 ) )
    result = int( td / timedelta( milliseconds = 1 ) )
    return result

def split( videoId ):

    print( "Splitting %s" % videoId )
    audio_fn = 'data/%s.webm' % videoId
    full_audio = AudioSegment.from_file( audio_fn, "webm" )
    print( "%s audio loaded." % audio_fn )

    caption_fn = 'data/%s.en.vtt' % videoId
    print( "%s caption loaded." % caption_fn )

    folder_dn = 'data/%s.split' % videoId
    if not os.path.exists( folder_dn ):
        os.makedirs( folder_dn )

    for caption in webvtt.read( caption_fn )[::2]:
        start = parse_to_ms( caption.start )
        end = parse_to_ms( caption.end )

        split_fn = folder_dn + ( '/%s.split.%08d-%08d' % ( videoId, start, end ) )
        print( "Generating %s" % split_fn )

        if ( start < MS_PAD ): start = 0
        split = full_audio[ start - MS_PAD : end + MS_PAD ]
        split.export( split_fn + '.wav', format='wav' )

        # Generate associated text file

        lines = caption.text.split('\n')
        if ( len( lines ) > 1 ):
            caption_text_parsed = lines[1].strip()
        else: caption_text_parsed = lines[0]

        with open( split_fn + '.txt', 'w' ) as text_file:
            text_file.write( caption_text_parsed )

    print( "Done." )

if __name__ == '__main__':
    for videoId in sys.argv[1:]:
        split( videoId )
    sys.exit()
