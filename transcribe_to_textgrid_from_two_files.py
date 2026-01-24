# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import textgrid
import csv


csvfilename1 = "Transcription 1 (small.en-tdrz).txt"
csvfilename2 = "Transcription 2 (small.en-tdrz).txt"
wavfilename = "3000-p02-l-ff_test"

tg = textgrid.TextGrid(name="tg")
tier1 = textgrid.IntervalTier(name="1")
tier2 = textgrid.IntervalTier(name="2")

with open(csvfilename1) as csv_file1:
    reader1 = csv.reader(csv_file1, delimiter='\t')
    for row in reader1:
        starttime = max(float(row[0]),0)
        #print(f"starttime={starttime}")
        endtime = float(row[1])
        #print(f"endtime={endtime}")
        text = row[2].strip()
        #print(text)
        tier1.add(minTime=starttime, maxTime=endtime, mark=text)

with open(csvfilename2) as csv_file2:
    reader2 = csv.reader(csv_file2, delimiter='\t')
    for row in reader2:
        starttime = max(float(row[0]),0)
        #print(f"starttime={starttime}")
        endtime = float(row[1])
        #print(f"endtime={endtime}")
        text = row[2].strip()
        #print(text)
        tier2.add(minTime=starttime, maxTime=endtime, mark=text)

print(tier1)
print(tier2)
tg.append(tier1)
tg.append(tier2)
print(tg)
tg.write(wavfilename + ".TextGrid")