# ETT stands for Eliana's Textgrid Tools

for the convencience of myself (eliana) and others (but mostly myself (eliana))

## Requirements
definitely you'll need [ffmpeg](https://www.ffmpeg.org/) and the [textgrid python package](https://github.com/kylebgorman/textgrid) for all of these.
there's more specific requirements for specific tools but they are Few i think and will only be specified when the tool is brought up.

ffmpeg is a separate tool that has os-dependent ways to install it but the textgrid library can be installed with the pip package manager as follows: `pip install textgrid`

## Slicer
a command line tool to slice wav and textgrid files into slices of your desired length. you use it like this
```
slicer.py textgrid_folder wav_foler length_in_seconds
```
or you can use it with no arguments as long as you have your textgrids and wavs in 2 separate folders and also no other textgrids and wavs in subfolders and also you're okay with 120 second slices

## Splitter (WIP)
a command line tool used to split wav and textgrid files into their left and right components. this tool assumes you are using stereo wav files and textgrids with at least two interval tiers.
```
splitter.py textgrd_folder wav_foley
```
to-do:
 - option to split individual wav/textgrids
 - better way of checking if textgrid tiers are meant for the left or right channel

## Transcriber
a command line tool to transcribe wav files into textgrids with interval tiers. you use it like this
```
transcriber.py file.wav
```
### requirements:
alongside the requirements listed at the beginning, this tool also makes use of OpenAI's first actual open source model, [whisper](https://github.com/openai/whisper), which by consequence also requires the [pytorch](https://pytorch.org/) package. you can install them like this
```
pip install pytorch
pip install -U openai-whisper
```

to-do:
 - have forced alignment done in the tool
 - option for doing an entire folder's worth of audio

# More Soon
