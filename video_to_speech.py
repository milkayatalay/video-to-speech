#!/usr/bin/env python3


import speech_recognition as sr
import moviepy.editor
import argparse
import concurrent.futures.thread
import time
import datetime

parser = argparse.ArgumentParser(description="A tool for extracting texts from speech videos",
                                 epilog="example usage: speech_to_text.py video.mp4 --slicing_amount=25 "
                                        "--thread_amount=15 --language=en-EN")  # name of the app prog="some name"
parser.add_argument("video_path", help="Source video path for extracting text")
parser.add_argument("--slicing_amount", help="Audio slicing amount (Default: 20)", type=int)
parser.add_argument("--thread_amount", help="Worker thread amount (Default: 10)", type=int)
parser.add_argument("--language", help="Enter language definition (Default: tr-TR) (en-EN for English,tr-TR for "
                                       "Turkish,\nclick adress for more: "
                                       "https://cloud.google.com/speech-to-text/docs/languages) ")
args = parser.parse_args()

r = sr.Recognizer()

starting_time = datetime.datetime.now()

inp = args.video_path
slicing_amount = 20
worker_thread_amount = 10
recognize_language = "tr-TR"
if args.slicing_amount:
    slicing_amount = args.slicing_amount

if args.thread_amount:
    worker_thread_amount = args.thread_amount

if args.language:
    recognize_language = args.language

print("\nSelecting \"" + args.video_path + "\" for extracting\n")

tarp = inp[:-4] + ".wav"

list_for_print = []


def extract_audio(inpath, tarpath):
    video = moviepy.editor.VideoFileClip(inpath)
    audioforextract = video.audio
    audio_duration = video.audio.duration
    audioforextract.write_audiofile(tarpath)
    return tarpath, audio_duration


def record_and_slice(audio_inp, audio_duration, slicing_a):
    i = 0
    print("\nAudio duration : " + str(audio_duration) + " second\n" + "Slicing amount : " + str(
        slicing_a) + " second\n" + "Worker thread amount : " + str(
        worker_thread_amount) + "\n\n" + "Started at : " + str(starting_time) + "\n")
    chunk_size = audio_duration / slicing_a
    audio_list = []
    while i < chunk_size:
        with sr.AudioFile(audio_inp) as source:
            audio_list.append(r.record(source, slicing_a, slicing_a * i))
        i = i + 1

    return audio_list


def func_for_thread(temp_object):
    list_for_print.append((str(temp_object[0]), r.recognize_google(temp_object[1], language=recognize_language)))
    print("Chunk: " + str(temp_object[0] + 1) + " DONE")


executor = concurrent.futures.thread.ThreadPoolExecutor(max_workers=worker_thread_amount)

for_inp = extract_audio(inp, tarp)

for obj in enumerate(record_and_slice(for_inp[0], for_inp[1], slicing_amount)):
    executor.submit(func_for_thread, obj)


def wait_for_end():
    time.sleep(20)
    print("\nSorting Chunks")
    list_for_print.sort(key=lambda tup: int(tup[0]))
    print("Chunks Sorted")
    # print(*list_for_print)
    write_list_to_file(list_for_print)
    print("\n" + inp[:-4] + ".txt created\n" + tarp + " created\n" + "\nSUCCESS - " + str(
        datetime.datetime.now() - starting_time))


def write_list_to_file(list_for_write):
    with open(inp[:-4] + ".txt", 'w') as file_handle:
        for list_item in list_for_write:
            file_handle.write('%s\n' % list_item[1])

        file_handle.close()


executor.submit(wait_for_end)