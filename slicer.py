import glob
import os
import random
import subprocess
import sys
import textgrid

def sliceTg(tg, start, length):
  nutg = textgrid.TextGrid()
  print(tg[0][0])

  duration = start + length

  print(len(tg))
  for i in range(0, len(tg)):

    # append corresponding tier to nutg
    nutg.append(textgrid.IntervalTier(name=tg[i].name))

    for j in tg[i]:
      if j.minTime > start and j.maxTime < duration:

        # copy intervals with modified times
        n = j
        n.minTime = n.minTime - start
        n.maxTime = n.maxTime - start
        nutg[i].add(n.minTime, n.maxTime, n.mark)
  return nutg

def sliceAudio(audiofile, start, length, output):

  command = [
      'ffmpeg',
      '-i', audiofile,
      '-ss', str(start),  
      '-t', str(length),
      output           # Output
  ]

  subprocess.run(command, check=True)


# start of main function
if sys.argv[1] == 'help':
    sys.exit('''usage: slicer.py your_textgrid_folder your_wav_folder length_in_seconds
ex: slicer.py tgs wavs 120''')

length = 120 # default value

if not os.path.exists('out'):
    os.mkdir('out')

# load files
textgrids = glob.glob(sys.argv[1] + "/*TextGrid")
audio = glob.glob(sys.argv[2] + "/*wav")
# default options
if len(sys.argv) == 1:
    textgrids = glob.glob("*/*TextGrid")
    audio = glob.glob("*/*wav")
elif len(sys.argv) == 4:
    textgrids = glob.glob(sys.argv[1] + "/*TextGrid")
    audio = glob.glob(sys.argv[2] + "/*wav")
    length = int(sys.argv[3])
# error checking
else:
    sys.exit('''ensure you run with the correct number of arguments.
ex: slicer.py 'your textgrid folder' 'your wav folder' 'length of slices in seconds'
(will glob for all textgrids and wav files and assume 120 seconds by default)''')
if (len(textgrids) != len(audio)):
  baud = []
  btg = []
  for i in audio:
      baud.append(os.path.basename(i[:-4]))
  for i in textgrids:
      btg.append(os.path.basename(i[:-9]))
  for i in baud:
      if i not in btg:
          print(i + " does not have a corresponding textgrid")
  for i in btg:
      if i not in baud:
          print(i + "does not have a corresponding wav file")
  sys.exit("ensure that each textgrid has matching audio")

for i in range(0,len(textgrids)):
  tg = textgrid.TextGrid.fromFile(textgrids[i])
  audiofile = sys.argv[2] + "/" + os.path.basename(textgrids[i])[:-9] + '.wav'
  if not os.path.exists(audiofile):
    print("hey where's the wav file for " + textgrids[i] + "?")
    break
  
  # list wav and textgrid for debugging
  print(textgrids[i])
  print(audiofile)

  # get times to do random time
  max = tg[0][-1].maxTime

  # if the file is shorter than the slice length, that's a problem
  if max > length:
      print(textgrids[i] + " and " + audiofile + " are less than " + str(length) + " seconds long.")
  ubound = int(max*0.8) - length
  lbound = int(max*0.2)

  start = random.randrange(lbound, ubound)

  tg_out = "out/" + os.path.basename(textgrids[i])[:-9] + "_sliced.TextGrid"
  au_out = "out/" + os.path.basename(textgrids[i])[:-9] + "_sliced.wav"

  # gaming
  sliceTg(tg, start, length).write(tg_out)
  sliceAudio(audiofile, start, length, au_out)
