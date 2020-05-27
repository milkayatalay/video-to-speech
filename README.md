# video-to-speech
A tool for extracting text from speech on videos 

SpeechRecognition and MoviePy libraries used in this script.
You need to install them first.

```bash
pip install SpeechRecognition
```
```bash
pip install moviepy
```

Here is the "video-to-speech.py -h" command output

```bash
usage: video-to-speech [-h] [--slicing_amount SLICING_AMOUNT]
                     [--thread_amount THREAD_AMOUNT] [--language LANGUAGE]
                     video_path

A tool for extracting texts from speech videos

positional arguments:
  video_path            Source video path for extracting text

optional arguments:
  -h, --help            show this help message and exit
  --slicing_amount SLICING_AMOUNT
                        Audio slicing amount (Default: 20)
  --thread_amount THREAD_AMOUNT
                        Worker thread amount (Default: 10)
  --language LANGUAGE   Enter language definition (Default: tr-TR) (en-EN for
                        English,tr-TR for Turkish, click adress for more:
                        https://cloud.google.com/speech-to-text/docs/languages)

example usage: video_to_speech video.mp4 --slicing_amount=25 --thread_amount=15 --language=en-EN
```
