import pickle
import subprocess
import sys
import textgrid
import time
import whisper
import os
import torch
# my gpu is bad :(
torch.cuda.is_available = lambda : False
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

input_audio = sys.argv[1]
input_basename = input_audio[:-4]
start_time = time.time()

def split_stereo_audio(input_file, left_output_file, right_output_file):

    filter = "highpass=f=90,afftdn=nr=18:nt=w,lowpass=f=14000,agate=ratio=30:range=0.015:threshold=0.015" # bandpass filter and noise gate

    # Command to extract the left channel
    left_command = [
        'ffmpeg',
        '-i', input_file,          # Input file
        '-filter_complex', "pan=mono|c0=c0,"+filter,   # Map left channel
        left_output_file           # Output file for left channel
    ]

    # Command to extract the right channel
    right_command = [
        'ffmpeg',
        '-i', input_file,          # Input file
        '-filter_complex', "pan=mono|c0=c1,"+filter,   # Map right channel + Noise Gate
        right_output_file          # Output file for right channel
    ]

    # Run the commands
    subprocess.run(left_command, check=True)
    subprocess.run(right_command, check=True)

    print(f"Left channel saved to {left_output_file}")
    print(f"Right channel saved to {right_output_file}")

left_output = input_basename + "_l.wav"
right_output = input_basename + "_r.wav"

split_stereo_audio(input_audio, left_output, right_output)

# whisper time
model = whisper.load_model("medium.en")
print("model loaded!")

result_l = model.transcribe(left_output)
print("left channel transcribed!")
''''
with open('result_l.pkl', 'wb') as f:
    pickle.dump(result_l, f)
print("left channel transcription dumped to result_l.pkl")
'''
result_r = model.transcribe(right_output)
print("right channel transcribed!")
''''
with open('result_r.pkl', 'wb') as f:
    pickle.dump(result_r, f)
print("left channel transcription dumped to result_r.pkl")
'''

# make new textgrid and new tiers L and R
tg = textgrid.TextGrid(name="tg")
ltier = textgrid.IntervalTier(name="L")
rtier = textgrid.IntervalTier(name="R")

print("textgrid initialized. populating textgrid")

# populate "l" tier
pmax = 0
for i in result_l["segments"]: #this needs checking for whisper might mess up some textgrids
  if i["start"] < pmax:
    start = pmax
    print("shifted!")
    print(i)
  else:
    start = i["start"]
  ltier.add(minTime=start, maxTime=i["end"], mark=i["text"])
  pmax=i["end"]

# populate "r" tier
pmax = 0
for i in result_r["segments"]: 
  if i["start"] < pmax:
    start = pmax
    print("shifted!")
    print(i)
  else:
    start = i["start"]
  rtier.add(minTime=start, maxTime=i["end"], mark=i["text"])
  pmax=i["end"]

tg.append(ltier)
tg.append(rtier)
tg.write(input_basename + ".TextGrid")
print("textgrid populated")

# remove temp files
os.remove(left_output)
os.remove(right_output)
print("took " + str(time.time()-start_time) + " time")
