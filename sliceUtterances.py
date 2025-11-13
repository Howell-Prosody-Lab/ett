import glob
import os
import subprocess
import sys
import textgrid
import traceback
from convert_dict import *

def sliceTg(tg, start, end, tiers):
  """
  # Copies all relevant slices of textgrid into fresh ones.
  # Args: textgrid.TextGrid item tg, timestamp str start, timestamp str end,
  # tuple tiers (contains names of phone-tier and word-tier)
  # Returns: textgrid.TextGrid item nu_tg
  """
  #print("sliceTg:")
  #print(start, end)
  #creating blank textgrid with only relevant tiers
  nu_tg = textgrid.TextGrid()
  for t in tiers:
    nu_tg.append(textgrid.IntervalTier(name=t))
  #print("number of tiers in nu_tg:",len(nu_tg))

  #for tier in list of tiers: #if it's one of the relevant tiers
  for i in range(0, len(tg)): 
    #print(f'i={i}',tg[i])
    source_tier_name = tg[i].name
    if source_tier_name in tiers: 
      #print(source_tier_name, "yes, relevant tier")
      for j in tg[i]: #for interval in tier      
        jmintime = j.minTime
        jmaxtime = j.maxTime
        if ((jmintime >= start) and (jmaxtime <= end)):
          #print(j)
          # copy intervals with modified times
          nmintime = jmintime - start
          if nmintime < 0:
            nmintime = 0
          nmaxtime = jmaxtime - start          
          n = j
          n.minTime = nmintime
          n.maxTime = nmaxtime
          #print(f"{jmintime}-{start}={nmintime}")
          #print(f"{jmaxtime}-{start}={nmaxtime}")
          #print("number of tiers in nu_tg:",len(nu_tg))
          try:
            nu_tg_tier=nu_tg.getFirst(source_tier_name)
            nu_tg_tier.add(nmintime, nmaxtime, n.mark)
          except IndexError:
            print(f"source_tier_name={source_tier_name}, time={nmintime}-{nmaxtime} derived from {jmintime}-{start}={nmintime} and {jmaxtime}-{start}={nmaxtime}")
            print(traceback.format_exc())
            quit()
    #else:
      #print(tg[i].name, "no, not relevant tier")
  #print("now check to see if any of them are still empty")
  for t in nu_tg.tiers:
    #print(t, not not t)
    assert t, f"{t} is still empty"
  #print("end sliceTg\n")
  return nu_tg

def sliceAudio(audiofile, start, end, output):
  """
  # Slices sections of audio based on provided timestamps.
  # Args: path-like string audiofile, timestamp string start, timestamp
  #   str end, path-like string output
  # Returns: none. Outputs .wav files.
  """
  #print("sliceAudio running")
  length = end-start
  if os.path.isfile(output):
    os.remove(output)
    
  command = [
      'ffmpeg',
      '-i', audiofile,
      '-ss', str(start),  
      '-t', str(length),
      output           # Output
  ]

  subprocess.run(command, check=True)
  #print("sliceAudio end")

def just_one_moneypenney(audiofile, tg_file_path, save_file_gen_path, d, word_tier, phone_tier):
  """
  # Runs on a single file instead of a folder full of them, allows for
  # integration into autorpt. Splits a wav file into its component utterances
  # and transcript by pulling from its combined csv file.
  # Args: path-like string wav_file_path, path-like string tg_file_path,
  #   path-like string save_file_gen_path, dictionary d, string word_tier,
  #   string phone_tier.
  # Returns: none. Outputs a folder of audio, textgrid, and txt files.
  """
  #print("begin just_one_moneypenney")
  tg = textgrid.TextGrid.fromFile(tg_file_path)
  #print("files:",tg, audiofile)
  file_name = os.path.basename(wav_file_path)[:-4] 
  file_dir = os.path.join(save_file_gen_path, "sliced-utterance-output",file_name)
  #print(file_name)
  #print(file_dir)
  if not os.path.exists(file_dir):
    os.makedirs(file_dir)
  os.chdir(file_dir)

  #print("switching to process_utterances")
  data, transcript = convert_dict.process_utterances(d, file_name, word_tier[0:4]) #word_tier[0:4] is the speaker ID
  #print("back from process_utterances\n")
  
  f = open(f"{file_name}.txt", "w")   
  length = len(data)
  tiers = (word_tier, phone_tier)
  for i in range(length):
    utterance_name = file_name + f"_int{i}"
    tg_out = os.path.join(file_dir,(utterance_name + ".TextGrid"))
    au_out = os.path.join(file_dir,(utterance_name + ".wav"))
    #print(f"about to call sliceTg on utterance {i} with {data[i].start}, {data[i].end}")
    sliced_text_object = sliceTg(tg, data[i].start, data[i].end, tiers)
    sliced_text_object.write(tg_out)
    sliceAudio(audiofile, data[i].start, data[i].end, au_out)
    f.write(f'{i}\n')
    for j in range(len(transcript[i])):
      f.write(transcript[i][j])
      f.write(' ')
    f.write('\n')
    
  f.close()
  #print("end just_one_moneypenney")                        
    
def main():
  # Not done yet. Intending to add functionality to pull the csv and convert to
  # dictionary.
  f = open("slicy.txt")
  txt_file_path = f.readline()[0:-1]
  wav_file_path = f.readline()[0:-1]
  save_path = f.readline()[0:-1]
  start = float(f.readline()[0:-1])
  end = float(f.readline()[0:-1])

  # load files
  textgrids = glob.glob(txt_file_path + "/*TextGrid")
  print("length of textgrids =", len(textgrids))
  audio = glob.glob(wav_file_path + "/*wav")
  print("length of audio =", len(audio))

##  for i in range(0,len(textgrids)):
##    tg = textgrid.TextGrid.fromFile(textgrids[i])
##    audiofile = wav_file_path + "/" + os.path.basename(textgrids[i])[:-9] + '_1.wav'
  for i in range(0,len(audio)):
    audiofile = audio[i]
    tg = textgrid.TextGrid.fromFile(wav_file_path + "/" + os.path.basename(audio[i])[:-6] + '.TextGrid')
    # list wav and textgrid for debugging
    #print("file:")
    #print(tg)
    #print(audiofile)

##    tg_out = os.path.join(save_path,textgrids[i])[:-9] + f"_int{i}.TextGrid"
##    print("tg_out:",tg_out)
##    au_out = os.path.basename(textgrids[i])[:-9] + f"_int{i}.wav"
    tg_out = os.path.join(save_path,audio[i])[:-4] + f"_int{i}.TextGrid"
    print("tg_out:",tg_out)
    au_out = os.path.basename(audio[i])[:-4] + f"_int{i}.wav"

  # gaming
  sliced_text_object = sliceTg(tg, start, end)
  sliced_text_object.write(tg_out)
  sliceAudio(audiofile, start, end, au_out)

import convert_dict
import os

def test():
  #allows us to test this module without running rpt
  f = open("pull_files_from_drive.txt")
  gen_textgrid_path = f.readline()[0:-1]
  gen_wav_path = f.readline()[0:-1]
  save_file_gen_path = f.readline()[0:-1]
  f.close()
  tg_file_path = os.path.join(gen_textgrid_path, "1213p48mx92zr82pv.TextGrid")
  wav_file_path = os.path.join(gen_wav_path, "1213p48mx92zr82pv_1.wav")
  word_tier = "92zr - words"
  phone_tier = "92zr - phones"
  d = convert_dict.open_csv()
  just_one_moneypenney(wav_file_path, tg_file_path, save_file_gen_path, d, word_tier, phone_tier)
    
if __name__ == "__main__":
    test()
