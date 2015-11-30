from pymongo import MongoClient

client = MongoClient()
db = client.lolMatchesDB

"""
this functions prints out a divider made "=" for the length it is handed.
"""
def divider(length):
	string = "="
	for i in range(0,length):
		string = string + "="
	print string 

"""
this function gets the matchId and game winner from the database, it then outputs all the results of each game.
"""
def returnAllWinners():
	gameResult = db.games.find({"teams.winner":True},{"matchId":1,"teams.winner":1,})

	for i in gameResult:
		print i['matchId']
		j = i['teams']
		k = j[0]
		l = j[1]
		if k['winner'] == True:
			print "Winner: Team 1"
		else:
			print "Winner: Team 2"

"""
This functions takes a matchId as a paramerter then returns which team won.
"""
def getGameResult(matchId):
	gameResult = db.games.find({"matchId":matchId},{"teams.winner":1})
	for i in gameResult:
		j = i['teams']
		k = j[0]
		if k['winner'] == True:
			return "Team 1"
		else:
			return "Team 2"

"""
This fucntion is handed a matchId and playerId then returns there Id with the game result (win/loss).
"""
def getPlayerWin(matchId,playerId):
	winsToRetrun = []
	playerToReturn = []
	playerWinDict = db.games.find({"matchId":matchId},{"participants.stats.winner":1,"_id":0})
	playerIdDict = db.games.find({"matchId":matchId},{"participantIdentities.player.summonerId":1,"_id":0})
	a=0
	b=0
	for i in playerWinDict:
		j = i['participants']
		k = j[a]
		l = k['stats']
		winsToRetrun.append(l['winner'])
		a += 1
	for i in playerIdDict:
		j = i ['participantIdentities']	
		k = j[b]
		l = k['player']
		playerToReturn.append(l['summonerId'])
	for i in range(len(playerToReturn)):
		return playerToReturn[i],winsToRetrun[i]

"""
This functions is handed a playerId, it then returns the players cs different delta when compared to there dellow laner
"""
def getPlayerCsDiff(playerId):
	listOfSummoners = []
	listOfCsDiff = []
	playersCsDiff = db.games.find(
		{"participantIdentities.player.summonerId":playerId},
		{"participants.timeline.csDiffPerMinDeltas":1,"participantIdentities.player.summonerId":1,"_id":0}
		)
		
	for i in playersCsDiff:
		j = i['participantIdentities']
		for a in range(0,10):
			k = j[a]
			l = k['player']
			listOfSummoners.append(l['summonerId'])
		j = i['participants']
		for b in range(0,10):
			k = j[b]
			l = k['timeline']
			m = l['csDiffPerMinDeltas']
			listOfCsDiff.append(m)
		
		for i in range(len(listOfSummoners)):
			print listOfSummoners[i]
			j = listOfCsDiff[i]
			if j['zeroToTen'] != None:
				print j['zeroToTen']
			try:
				print j['tenToTwenty']
			except KeyError:
				pass
			try:
				print j['twentyToThrity']
			except KeyError:
				pass
			try:
				print j['thirtyToEnd']
			except KeyError:
				pas
			divider(50)

"""
this function retrun what position in the list a player is, this is needed beause in the database players and there names are stored in the array participantIdentities but all the stats (champoins, CS, spells, wins/loss) is stored in the participants array so the location in the array is needed to find players stats.
"""
def getPlayerListNum(playerId):
	playerListNum = db.games.find({"participantIdentities.player.summonerId":playerId},{"participantIdentities.player.summonerId":1,"_id":0})
	
	for i in playerListNum:
		j = i['participantIdentities']
		a=0
		
		for a in range(0,(len(j))):
			k = j[a]
			l = k['player']
			#print l['summonerId']
			if l['summonerId'] == playerId:
				return a
			a += 1

"""
This function takes a players Id then calls the getPlayerListNum to get its position the array so it can then return the players total damage to champions.
"""
def getPlayerDmg(playerId):
	playerDmg = db.games.find({"participantIdentities.player.summonerId":playerId},{"participants.stats.totalDamageDealtToChampions":1,"_id":0})
	playListNum = getPlayerListNum(playerId)
	#print playListNum
	for i in playerDmg:
		j = i['participants']
		k = j[playListNum]
		m = k['stats']
		#print m['totalDamageDealtToChampions']
		return m['totalDamageDealtToChampions']

"""
This function will return a players estimated position (TOP/MID/DUO_SUPPORT/DUO_CARRY)
"""
def getPlayerPos(playerId):
	playerPos = db.games.find({"participantIdentities.player.summonerId":playerId},{"participants.timeline.role":1,"_id":0})
	pListNum = getPlayerListNum(playerId)
	for i in playerPos:
		j = i['participants']
		k = j[pListNum]
		l = k['timeline']
		print l['role']

	
	
"""
This function will return all the stats of the playerId it is handed. outputs stats in a dict. It will also print out the stats in a readable format if the parameter "printOut" is true
"""
def getAllPlayerStats(playerId,printOut):
	playerStat = db.games.find({"participantIdentities.player.summonerId":playerId},{"participants.stats":1,"_id":0})
	pListNum = getPlayerListNum(playerId)
	for i in playerStat:
		j = i['participants'] 
		k = j[pListNum]
		l = k['stats']
		if printOut == True:
			for a, b in l.items():
				print a,":",b
			divider(50)
		return l

"""
This function will return the average player damage for each position, it must be handed the desired postion(TOP/MID/DUO_SUPPORT/DUO_CARRY).
"""
def getPlayerAvgDmg(pos,outputDmgList):
	listToAvg = []
	allPlayerDmg = db.games.find({"participants.timeline.role":pos},{"participants.stats.totalDamageDealtToChampions":1,"_id":0})
	for i in allPlayerDmg:
		j = i['participants']
		k = j[0]
		l = k['stats']
		for a,b in l.items():
			if outputDmgList == True:
				print a,":",b
			listToAvg.append(b)
		
	#print len(listToAvg)
	avg = 0

	for x in range(0,(len(listToAvg))):
		avg = avg + listToAvg[x]
	avg = avg/(len(listToAvg))
	return avg
	print "not finished"""

"""
This function will return the averge gold for each position. must be handed desired position 
"""
def getPlayerAvgGold(pos,outputGoldList):
	listToAvg = []
	allPlayerDmg = db.games.find({"participants.timeline.role":pos},{"participants.stats.goldEarned":1,"_id":0})
	for i in allPlayerDmg:
		j = i['participants']
		k = j[0]
		l = k['stats']
		for a,b in l.items():
			if outputGoldList == True:
				print a,":",b
			listToAvg.append(b)
	#print len(listToAvg)
	avg = 0

	for x in range(0,(len(listToAvg))):
		avg = avg + listToAvg[x]
	avg = avg/(len(listToAvg))
	return avg

"""
gets a list of champions played by everyone, all positions. There may be an issue with the printout of Id(might be hitting output limit in python)
"""
def getChampions(printChamps):
	listToOutput = []
	champs = db.games.find({"matchMode":"CLASSIC"},{"participants.championId":1,"_id":0})
	a = 0
	for i in champs:
		j = i['participants']
		while a<10:
			k = j[a] 
			if printChamps == True:
				print k['championId']
			listToOutput.append(k['championId'])
			#print a
			a += 1
		if a>9:
			a = 0
	#print len(listToOutput)
	return listToOutput
	
"""
This function returns a list of all the wins 
"""
def getWinList():
	wins = db.games.find({"matchMode":"CLASSIC"},{"participants.stats.winner"})
	winsList = []
	a = 0
	for i in wins:
		j = i['participants']
		while a<10:
			k = j[a]
			l = k['stats']
			m = l['winner']
			winsList.append(m)
			a += 1
		if a>9:
			a = 0
	return winsList
	print ""

	
"""
This function will return most common position in each role. IMPORTANT: item is returned is a list with only 1 item
"""
def mostCommonChamp():
	champs = getChampions(False)
	toReturn = findMostCommon(champs,1)
	return toReturn
	"""
	champCount = {}
	for champ in champs:
		if champ in champCount:
			champCount[champ] += 1
		else:
			champCount[champ] = 1
	mostPopchamp = sorted(champCount, key = champCount.get, reverse = True)
	return mostPopchamp[:1]
	print """

"""
This will return a list of all the playerId in all the games
"""
def getPlayerId():
	listOfPlayers = []
	players = db.games.find({"matchMode":"CLASSIC"},{"participantIdentities.player.summonerId":1,"_id":0})
	a = 0
	for i in players:
		j = i['participantIdentities']
		while a<10:
			k = j[a]
			l = k['player']
			m = l['summonerId']
			#print m
			listOfPlayers.append(m)
			a += 1
		if a>9:
			a = 0
	return(listOfPlayers)

"""
This function will find the most common items in a list handed to it, the "numToOutput" is how many of the most common to return, eg "2" will return the 2 most common items in the list.
"""
def findMostCommon(listToUse,numToOutput):
	a = {}
	for i in listToUse:
		if i in a:
			a[i] += 1
		else:
			a[i] = 1
	mostCommon = sorted(a, key = a.get, reverse = True)
	return mostCommon[:numToOutput]	
	print""	
	
"""
This funciton will return the highest win rate champion, if "returnLooser" is True then it will retrun the most common looser instead of the winner. (will return a list)
"""
def highestWinRateChampion(numToList,returnLoosers):
	onlyWinners = []
	onlyLoosers = []
	champsList = getChampions(False)
	winList = getWinList()
	print len(winList)
	print len(champsList)
	print winList[5]
	for i in range (0,10000):
		if winList[i] == True:
			onlyWinners.append(champsList[i])
		else:
			onlyLoosers.append(champsList[i])
	mostCommonWinner = findMostCommon(onlyWinners,numToList)
	if returnLoosers == True:
		mostCommonLooser = findMostCommon(onlyLoosers,numToList)
		return mostCommonLooser
	return mostCommonWinner
	
"""
This function will return a list with all the items bought in the all the games
"""
def getItems(printItems):
	listToOutput = []
	item0 = db.games.find({"matchMode":"CLASSIC"},{"participants.stats":1,"_id":0})
		
	a = 0
	for i in item0:
		j = i['participants']
		while a<10:
			k = j[a]
			l = k['stats']
			if printItems == True:
				print "item 0: ",l['item0']
				print "item 1: ",l['item1']
				print "item 2: ",l['item2']
				print "item 3: ",l['item3']
				print "item 4: ",l['item4']
				print "item 5: ",l['item5']
			if l['item0'] != 0:
				listToOutput.append(l['item0'])
			if l['item1'] != 0:
				listToOutput.append(l['item1'])
			if l['item2'] != 0:
				listToOutput.append(l['item2'])
			if l['item3'] != 0:
				listToOutput.append(l['item3'])
			if l['item4'] != 0:
				listToOutput.append(l['item4'])
			if l['item5'] != 0:
				listToOutput.append(l['item5'])
			a += 1
		if a>9:
			a = 0
	return listToOutput	
	
"""
This function will return the most popular items
"""
def mostCommonItem(numToList):
	items = getItems(False)
	
	mostCommon = findMostCommon(items,numToList)
	return mostCommon
	
"""

"""
def highestWinRateItem():
	onlyWinners = []
	onlyLoosers = []
	
"""
This function will find out if the team that gets first blood wins (this can then be used to see if getting first and winning is a trend)
"""
def firstBloodWin(outputTF):
	listWinners = []
	listFirstBloods =[]
	firstBlood = db.games.find({"matchMode":"CLASSIC"},{"teams.firstBlood":1,"teams.winner":1,"_id":0})
	for i in firstBlood:
		j = i['teams']
		k = j[0]
		l = k['winner']
		m = k['firstBlood']
		n = j[1]
		o = n['winner']
		p = n['firstBlood']
		if outputTF == True:
			print "Win Team1:        ",l
			print "FirstBlood Team1: ",m
			print "Win Team 2:       ",o
			print "FirstBlood Team2 :",p
		listWinners.append(l)
		listFirstBloods.append(m)
		listWinners.append(o)
		listFirstBloods.append(p)
	return listFirstBloods,listWinners
		

"""
This function will find out if the team that gets first baron wins (this can then be used to see if getting first and winning is a trend)
"""
def firstBaronWin():
	print ""
	#test

"""
This function will find out if the team that gets first dragon wins (this can then be used to see if getting first and winning is a trend)
"""	
def firstDragonWin():
	print ""

"""
This function will find out if the team that gets first tower wins (this can then be used to see if getting first and winning is a trend)
"""	
def firstTowerWin():
	print ""

"""
This function will compare winnign teams towers to loosing team towers, does winnign team normally have more towers?
"""
def winTeamTower():
	print ""	

"""
This function will find what bans coralate with winning
"""
def winningBans():
	print ""
"""
This function will show if there is a trend with how many wards winning teams bought and how many wards a loosing team bought
"""
def wardBoughtTrend():
	print ""




firstBloodWin()
divider(50)
print mostCommonItem(1)[0]


client.close()


"""
abcdefghijklmnopqrst
"""