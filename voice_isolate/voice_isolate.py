#!/usr/bin/env python3
import sys

from spleeter.separator import Separator
from spleeter.audio.adapter import AudioAdapter


def main():
    separator = Separator('spleeter:5stems')

    separator.separate_to_file( './test.webm', './', duration = 3159 )



if __name__ == '__main__':
    sys.exit( main() )
