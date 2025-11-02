# ETT stands for Eliana's Textgrid Tools

for the convencience of myself (eliana) and others (but mostly myself (eliana))

## Requirements
definitely you'll need [ffmpeg](https://www.ffmpeg.org/) and the [textgrid python package](https://github.com/kylebgorman/textgrid) for all of these.
there's more specific requirements for specific tools but they are Few i think and will only be specified when the tool is brought up

## Slicer
a command line tool to slice wav and textgrid files into slices of your desired length. you use it like this
```
slicer.py textgrid_folder wav_foler length_in_seconds
```
or you can use it with no arguments as long as you have your textgrids and wavs in 2 separate folders and also no other textgrids and wavs in subfolders and also you're okay with 120 second slices

## Transcriber
a command line tool to transcribe wav files into textgrids with interval tiers. you use it like this
```
transcriber.py file.wav
```
to-do:
 - have forced alignment done in the tool
 - option for doing an entire folder's worth of audio
