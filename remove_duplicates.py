import math
import os
import pyloudnorm as pyln
import soundfile as sf
import subprocess
import sys
import textgrid

tgFile = argv[1]
audiofle = argv[2]
tg = textgrid.TextGrid.fromFile(tgFile)

# psa: loudness != intensity, but thansk to science this is good enough
# but for some reason checking for loudness is easier?
def check_loudness(start, duration, audiofile):

  # bandpass filter and noise gate
  filter = "highpass=f=90,afftdn=nr=18:nt=w,lowpass=f=14000,agate=ratio=30:range=0.015:threshold=0.015"
 
  tempfile = audiofile[:-4] + '_temp.wav'
  # make temporary audio file to run through
  command = [
      'ffmpeg',
      '-i', audiofile,
      '-filter_complex', filter,
      '-ss', str(start),
      '-t', str(duration),
      tempfile           # Output
  ]

  subprocess.run(command, check=True)

  # check loudness
  data, rate = sf.read(tempfile)
  meter = pyln.Meter(rate) #
  loudness = meter.integrated_loudness(data)

  # delete temporary audio file
  os.remove(tempfile)

  #return loudness
  return loudness

def split_stereo_audio(input_file, left_output_file, right_output_file):
    # Command to extract the left channel
    left_command = [
        'ffmpeg',
        '-i', input_file,          # Input file
        '-map_channel', '0.0.0',   # Map left channel
        left_output_file           # Output file for left channel
    ]

    # Command to extract the right channel
    right_command = [
        'ffmpeg',
        '-i', input_file,          # Input file
        '-map_channel', '0.0.1',   # Map right channel
        right_output_file          # Output file for right channel
    ]

    # Run the commands
    subprocess.run(left_command, check=True)
    subprocess.run(right_command, check=True)


# split into mono channels
left_channel = audiofile.split('.')[0] + '_l.wav'
right_channel = audiofile.split('.')[0] + '_r.wav'
split_stereo_audio(audiofile, left_channel, right_channel)

# iterate to find duplicate marks
j = 0 # iterator for words L (index 2)
for i in range(len(tg[0])):
  while (tg[2][j].minTime < tg[0][i].minTime - .05) and (j < len(tg[2])-1):
    j = j + 1
  
  if (tg[2][j].mark == tg[0][i].mark) and (tg[2][j].mark != ''):
    #print(tg[2][j].mark)

    duration = math.ceil(tg[0][i].maxTime - tg[0][i].minTime)
    init = tg[0][i].minTime

    l_loud = check_loudness(init, duration, left_channel)
    r_loud = check_loudness(init, duration, right_channel)

    if l_loud > r_loud:
      tg[0][i].mark = ''
    else:
      tg[2][j].mark = ''

os.remove(left_channel)
os.remove(right_channel)
tg.write(tgFile[:-9]+'_corrected.TextGrid')
