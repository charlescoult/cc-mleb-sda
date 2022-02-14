#!/usr/bin/env python3
import sys
import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display
import soundfile as sf


# Generate a spectogram visualization of the waveform
def gen_vis_spect( waveform, sr, save_fn ):

    S_full, phase = librosa.magphase(
        librosa.stft( waveform ) # short time fourier transform
    )

    plt.figure( figsize=( 12, 4 ) )

    librosa.display.specshow(
        librosa.amplitude_to_db(
            S_full,
            ref = np.max,
        ),
        y_axis = 'log',
        x_axis = 'time',
        sr = sr,
    )

    plt.colorbar()

    plt.tight_layout()
    plt.savefig( save_fn )
    plt.clf()

# Generate a waveform visualization of the waveform
def gen_vis_wave( waveform, sr, save_fn ):
    plt.figure( figsize=( 40, 2 ) )
    plt.plot( range( len( waveform ) ), waveform )

    plt.tight_layout()
    plt.savefig( save_fn )
    plt.clf()

# Generate a visualization of voice content probability of the waveform
def gen_vis_voice( waveform, sr, save_fn ):
    pass

# Vocal Activity Detector (VAD)
def isolate_voice( y, sr, save_fn ):
    S_full, phase = librosa.magphase(
        librosa.stft( y ) # short time fourier transform
    )

    S_filter = librosa.decompose.nn_filter(
        S_full,
        aggregate = np.median,
        metric = 'cosine',
        width = int( librosa.time_to_frames( 1, sr = sr ) )
    )

    S_filter = np.minimum(S_full, S_filter)

    # We can also use a margin to reduce bleed between the vocals and instrumentation masks.
    # Note: the margins need not be equal for foreground and background separation
    margin_i, margin_v = 2, 10
    power = 2

    mask_i = librosa.util.softmask(
        S_filter,
        margin_i * (S_full - S_filter),
        power=power
    )

    mask_v = librosa.util.softmask(
        S_full - S_filter,
        margin_v * S_filter,
        power=power
    )

    # Once we have the masks, simply multiply them with the input spectrum
    # to separate the components

    S_foreground = mask_i * S_full
    S_background = mask_v * S_full

    sf.write( 'foreground.wav', librosa.istft( S_foreground ), sr, subtype='PCM_24' )
    sf.write( 'background.wav', librosa.istft( S_background ), sr, subtype='PCM_24' )

    plt.figure(figsize=(12, 8))
    plt.subplot(3, 1, 1)
    librosa.display.specshow(
        librosa.amplitude_to_db( S_full, ref = np.max ),
                             y_axis='log',
        sr=sr
    )
    plt.title('Full spectrum')
    plt.colorbar()

    plt.subplot(3, 1, 2)
    librosa.display.specshow(
        librosa.amplitude_to_db( S_background, ref = np.max ),
        y_axis='log',
        sr=sr
    )
    plt.title('Background')

    plt.colorbar()
    plt.subplot(3, 1, 3)
    librosa.display.specshow(
        librosa.amplitude_to_db( S_foreground, ref=np.max),
        y_axis='log',
        x_axis='time',
        sr=sr
    )
    plt.title('Foreground')
    plt.colorbar()
    plt.tight_layout()
    plt.savefig( save_fn )

def main( audio_fn ):

    # load waveform (y) and sampling rate (sr)
    # waveform (y) contains an array of samples with each value being the
    # amplitude of the wave at that sampled time (float between -0.5 and 0.5)
    # Also converts stereo to mono unless mono is set to False
    # It might be worth looking into for analyzing multi-channel audio
    y, sr = librosa.load( audio_fn, sr = None )

    # gen_vis_wave( y, sr, 'wave2.png' )
    # gen_vis_spect( y, sr, 'spec2.png' )
    isolate_voice( y, sr, 'test.png' )

    # duration of the audio = # of sampled / sample rate
    print( '%0.2fs' % ( len( y ) / sr ) )

if __name__ == '__main__':
    sys.exit( main( sys.argv[1] ) )
