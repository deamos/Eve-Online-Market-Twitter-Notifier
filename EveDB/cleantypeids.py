import csv
import os
import sys

cwp=sys.path[0]
sys.path.append(cwp)

csvFile = csv.reader(open("invTypes.csv", "rb" ))
replacementArray={}
for line in csvFile:
	if line[12]=="1":
		listItem=[]
		listItem = line
		replacementArray[line[0]]=listItem
		#print replacementArray[line[0]]

newFile=open("newinvTypes.csv", 'w')
for row in replacementArray:
	#print replacementArray[row]
	#newFile.write(replacementArray[id])
	newFile.write(replacementArray[row][0] + "," + replacementArray[row][1] + "," +replacementArray[row][2] + "," + "," +replacementArray[row][4] + "," +replacementArray[row][5] + "," +replacementArray[row][6] + "," +replacementArray[row][7] + "," +replacementArray[row][8] + "," + replacementArray[row][9] + "," +replacementArray[row][10] + "," +replacementArray[row][11] + "," +replacementArray[row][12] + "," + replacementArray[row][13])
	newFile.write("\n")

newFile.close()