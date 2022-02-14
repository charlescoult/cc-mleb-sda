import os
import sys
from datetime import datetime, timedelta
import numpy as np

import webvtt
from pydub import AudioSegment

import librosa

import webrtcvad

vad = webrtcvad.Vad( 2 )

'''
Assumes file is less than 24 hrs in length.
'''

MS_PAD = 0 # number of milliseconds to pad on either side of each split

def parse_to_ms( timestr ):
    timestr = timestr + '000'
    dt = datetime.strptime( timestr, '%H:%M:%S.%f' )
    td = timedelta( hours = dt.hour, minutes = dt.minute, seconds = dt.second, milliseconds = int( dt.microsecond / 1000 ) )
    result = int( td / timedelta( milliseconds = 1 ) )
    return result

def to_bitstream( sig, dtype='int16' ):
    sig = np.asarray(sig)
    if sig.dtype.kind != 'f':
        raise TypeError("'sig' must be a float array")
    dtype = np.dtype(dtype)
    if dtype.kind not in 'iu':
        raise TypeError("'dtype' must be an integer type")

    i = np.iinfo(dtype)
    abs_max = 2 ** (i.bits - 1)
    offset = i.min + abs_max
    return (sig * abs_max + offset).clip(i.min, i.max).astype(dtype)

def split_pydub( videoId ):

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

        # parse caption text and generate associated text file
        lines = caption.text.split('\n')
        if ( len( lines ) > 1 ):
            caption_text_parsed = lines[1].strip()
        else: caption_text_parsed = lines[0]

        with open( split_fn + '.txt', 'w' ) as text_file:
            text_file.write( caption_text_parsed )

    print( "Done." )

def split_librosa( videoId ):

    audio_fn = 'data/%s.webm' % videoId
    y, sr = librosa.load( audio_fn, sr = None )

    caption_fn = 'data/%s.en.vtt' % videoId
    print( "%s caption loaded." % caption_fn )

    folder_dn = 'data/%s.split' % videoId
    if not os.path.exists( folder_dn ):
        os.makedirs( folder_dn )

    for caption in webvtt.read( caption_fn )[::2]:

        start_ms = parse_to_ms( caption.start )
        end_ms = parse_to_ms( caption.end )

        start_samples = int( ( start_ms / 1000 ) * sr )
        end_samples = int( ( end_ms / 1000 ) * sr )

        split = y[ start_samples : end_samples ]
        # split.export( split_fn + '.wav', format='wav' )

        frame_duration = 30 # 10, 20 or 30 ms in duration
        bitstream = to_bitstream( split[ int( sr * frame_duration / 1000 ) ] )
        print( 'Result: %s' % vad.is_speech( bitstream, sr ) )

        split_fn = folder_dn + ( '/%s.split.%08d-%08d' % ( videoId, start_ms, end_ms ) )
        # print( "Generating %s" % split_fn )

        # parse caption text and generate associated text file
        lines = caption.text.split('\n')
        if ( len( lines ) > 1 ):
            caption_text_parsed = lines[1].strip()
        else: caption_text_parsed = lines[0]

        with open( split_fn + '.txt', 'w' ) as text_file:
            text_file.write( caption_text_parsed )

    print( "Done." )

# use pydub for default
split = split_pydub

# for testing
if __name__ == '__main__':
    for videoId in sys.argv[1:]:
        split_librosa( videoId )
    sys.exit()
