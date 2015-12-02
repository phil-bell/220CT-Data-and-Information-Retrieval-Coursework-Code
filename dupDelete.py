from pymongo import MongoClient
import pprint
import collections
import re
client = MongoClient()
db = client.lolMatchesDB
game = db.games.find({"region":"NA"},{"_id":0, "matchId":1})

tempList = []
dupTempList = []
idTempList = []
matchIdList = []
listOfItemsToBeRemoved = []
for i in game:
	tempList.append(i)
	
for i in xrange(len(tempList)):
	for j in xrange(i+1,len(tempList)):
		if tempList[i] == tempList[j]:
			dupTempList.append(tempList[i])

print len(tempList)
print len(dupTempList)	
print "--------------------" 
for i in range(len(dupTempList)):
	tempString = dupTempList[i]
	tempVal = tempString['matchId']
	print tempVal
	matchIdList.append(tempVal)
print "--------------------" 
temp = int(matchIdList[0])
print temp
print type (temp)
print "--------------------"
for i in range(len(matchIdList)):	
	toBeRemoved = db.games.find({"matchId":matchIdList[i]},{"_id":1})
	for i in toBeRemoved:
		print i['_id']
		listOfItemsToBeRemoved.append(i)
print "--------------------"
for i in range(len(listOfItemsToBeRemoved)):
	print listOfItemsToBeRemoved[i]
print "--------------------"
print len(listOfItemsToBeRemoved)
listOfItemsToBeRemoved = listOfItemsToBeRemoved[1::2]
print len(listOfItemsToBeRemoved)
print "--------------------"
for i in range(len(listOfItemsToBeRemoved)):
	print listOfItemsToBeRemoved[i]

for i in range(len(listOfItemsToBeRemoved)):
	tempString = listOfItemsToBeRemoved[i]
	tempVal = tempString['_id']
	print tempVal
	results = db.games.remove({"_id":tempVal})
