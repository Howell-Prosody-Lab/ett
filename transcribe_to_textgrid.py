import textgrid
import csv


csvfilename = "p02_xscript_med.txt"
wavfilename = "3000-p02-l-ff_test"

tg = textgrid.TextGrid(name="tg")
tier1 = textgrid.IntervalTier(name="1")
tier2 = textgrid.IntervalTier(name="2")
binary_tier = True

with open(csvfilename) as csv_file:
    reader = csv.reader(csv_file, delimiter='\t')
    for row in reader:
        starttime = max(float(row[0]),0)
        #print(f"starttime={starttime}")
        endtime = float(row[1])
        #print(f"endtime={endtime}")
        text = row[2].strip()
        #print(text)
        #print(text[0])
        if text[0] == '-':
            #print(f"Is a switch. binary_tier was {binary_tier}.")
            text = text[2:]
            binary_tier = not binary_tier
            #print(f"binary_tier is now {binary_tier}.")
        if binary_tier:
            tier1.add(minTime=starttime, maxTime=endtime, mark=text)
            #print("Added to tier1")
        else:
            tier2.add(minTime=starttime, maxTime=endtime, mark=text)
            #print("Added to tier2")
    print(tier1)
    print(tier2)
    tg.append(tier1)
    tg.append(tier2)
    print(tg)
    tg.write(wavfilename + ".TextGrid")
