import glob
import os
import subprocess
import sys
import textgrid

def split_textgrid(input, left_output, right_output):
  tg = textgrid.TextGrid.fromFile(input)
  halfmarker = int(len(tg)/2)
  tg_l = textgrid.TextGrid()
  tg_r = textgrid.TextGrid()

  for i in tg[:halfmarker]:
    tg_l.append(i)
  for i in tg[halfmarker:]:
    tg_r.append(i)
  
  tg_l.write(left_output)
  tg_r.write(right_output)

  print(f"Left channel saved to {left_output}")
  print(f"Right channel saved to {right_output}")

def split_stereo_audio(input_file, left_output_file, right_output_file):

    # Command to extract the left channel
    left_command = [
        'ffmpeg',
        '-i', input_file,          # Input file
        '-filter_complex', "pan=mono|c0=c0",   # Map left channel
        left_output_file           # Output file for left channel
    ]

    # Command to extract the right channel
    right_command = [
        'ffmpeg',
        '-i', input_file,          # Input file
        '-filter_complex', "pan=mono|c0=c1",   # Map right channel
        right_output_file          # Output file for right channel
    ]

    # Run the commands
    subprocess.run(left_command, check=True)
    subprocess.run(right_command, check=True)

    print(f"Left channel saved to {left_output_file}")
    print(f"Right channel saved to {right_output_file}")

# start of main function
if sys.argv[1] == 'help':
    sys.exit('''usage: splitter.py your_textgrid_folder your_wav_folder
ex: splitter.py tgs wavs''')

# load files
textgrids = glob.glob(sys.argv[1] + "/*TextGrid")
audio = glob.glob(sys.argv[2] + "/*wav")
# default options
if len(sys.argv) == 1:
    textgrids = glob.glob("*/*TextGrid")
    audio = glob.glob("*/*wav")
elif len(sys.argv) == 3:
    textgrids = glob.glob(sys.argv[1] + "/*TextGrid")
    audio = glob.glob(sys.argv[2] + "/*wav")
# error checking
else:
    sys.exit('''ensure you run with the correct number of arguments.
ex: splitter.py 'your textgrid folder' 'your wav folder'
(will glob for all textgrids and wav files in subfolders by default)''')

if not os.path.exists('out'):
    os.mkdir('out')

for i in textgrids:
  split_textgrid(i, 'out/' + i[:-9] + '_l.TextGrid', 'out/' + i[:-9] + '_r.TextGrid')
for i in audio:
  split_stereo_audio(i, 'out/' + i[:-4] + '_l.wav', 'out/' + i[:-4] + '_r.wav')
