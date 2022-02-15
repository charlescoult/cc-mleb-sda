# Sir David Attenborough Voice Model (cc-mleb-sda)

## Relevant Documents
* [Notion Page](https://charlescoult.notion.site/Sir-David-Attenborough-Voice-Model-8a0628a1dee049368b48fb42dddcb617)

## How to use
* `7z x data.7z` - Unzip allready processed data
* `process.py <YouTube video UID>...` - Process a video from YouTube and add it to the dataset
  * `<YouTube video UID>` can be found in the YouTube video's URL: `https://www.youtube.com/watch?v=<YouTube video UID>`
  * Performs the following tasks on each supplied `<YouTube video UID>` argument:
    * Downloads the audio to a `webm` file (`data/<YouTube video UID>.webm`) and auto-generated closed captions to a `vtt` file (`data/<YouTube video UID>.en.vtt`).
    * Uses `webvtt` to parse `vtt` file and for each caption object returned:
      * Uses `pydub` to split the audio file according to the timestamps provided in the caption (`data/<YouTube video UID>.split/<YouTube video UID>.<start index in ms>-<end index in ms>.wav`)
      * Creates an associated text file with the caption text for that excerpt (`data/<YouTube video UID>.split/<YouTube video UID>.<start index in ms>-<end index in ms>.txt`).
* `7z a data.7z data` - Rezip processed data after changes
* `rm -rf ./data/<YouTube video UID>.*` - Remove a video from the dataset

