import sys
import downloadYT
import split

def process( videoId ):
    downloadYT.downloadAudio( videoId )
    # TODO: add voice isolation here
    split.split( videoId )

if __name__ == '__main__':
    for videoId in sys.argv[1:]:
        process( videoId )
    sys.exit()
