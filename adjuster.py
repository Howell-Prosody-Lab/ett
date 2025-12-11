import sys
import textgrid

tgFile = sys.argv[1]

if not tgFile.endswith('.TextGrid'):
    sys.exit("Error: expected a '.TextGrid' file")

tg = textgrid.TextGrid.fromFile(tgFile)

rtier = 0 #reference tier, 0 for words, 3 for phones

j = 0
for i in range(len(tg[4])):
  point = tg[4][i]

  while j < len(tg[rtier]) and tg[rtier][j].maxTime < point.time:
    j += 1

# prominence is centered
  if j < len(tg[rtier]) and tg[rtier][j].minTime <= point.time <= tg[rtier][j].maxTime and '*' in point.mark:
    tg[4][i].time = (tg[rtier][j].minTime + tg[rtier][j].maxTime) / 2
# boundaries are put at the End
  elif j < len(tg[rtier]) and tg[rtier][j].minTime <= point.time <= tg[rtier][j].maxTime and ']' in point.mark:
    tg[4][i].time = tg[rtier][j].maxTime

tg.write(tgFile[:-9]+'_adjusted.TextGrid')
