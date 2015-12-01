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
		if i['teams'][0]['winner'] == True:
			print "Winner: Team 1"
		else:
			print "Winner: Team 2"

"""
This functions takes a matchId as a paramerter then returns which team won.
"""
def getGameResult(matchId):
	gameResult = db.games.find({"matchId":matchId},{"teams.winner":1})
	for i in gameResult:
		if i['teams'][0]['winner'] == True:
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
		winsToRetrun.append(i['participants'][a]['stats']['winner'])
		a += 1
	for i in playerIdDict:
		playerToReturn.append(i['participantIdentities'][b]['player']['summonerId'])
	for i in range(len(playerToReturn)):
		return playerToReturn[i],winsToRetrun[i]

"""
This functions will return total of the winners CSdelta and the total of the loosers CSDelta, returns them in a list:
1st winners total CS delta
2nd looser total CS delfa
"""
def getCsDiff():
	listToReturn = []
	winningCS = 0
	loosingCS = 0
	playersCsDiff = db.games.find({"matchMode":"CLASSIC"},{"participants.timeline.csDiffPerMinDeltas":1,"participants.stats.winner":1,"_id":0})
	
	#for i in playersCsDiff:
		#print i
	b = 0
	for i in playersCsDiff:
		a = 0
		
		while a<10:
			if i['participants'][a]['stats']['winner'] == True:
				try:
					winningCS = winningCS + i['participants'][a]['timeline']['csDiffPerMinDeltas']['zeroToTen']
				except KeyError:
					pass
				try:
					winningCS = winningCS + i['participants'][a]['timeline']['csDiffPerMinDeltas']['tenToTwenty']
				except KeyError:
					pass
				try:
					winningCS = winningCS + i['participants'][a]['timeline']['csDiffPerMinDeltas']['twentyToThrity']
				except KeyError:
					pass
				try:
					winningCS = winningCS + i['participants'][a]['timeline']['csDiffPerMinDeltas']['thirtyToEnd']
				except KeyError:
					pass	
			else:
				try:
					loosingCS = loosingCS + i['participants'][a]['timeline']['csDiffPerMinDeltas']['zeroToTen']
				except KeyError:
					pass
				try:
					loosingCS = loosingCS + i['participants'][a]['timeline']['csDiffPerMinDeltas']['tenToTwenty']
				except KeyError:
					pass
				try:
					loosingCS = loosingCS + i['participants'][a]['timeline']['csDiffPerMinDeltas']['twentyToThrity']
				except KeyError:
					pass
				try:
					loosingCS = loosingCS + i['participants'][a]['timeline']['csDiffPerMinDeltas']['thirtyToEnd']
				except KeyError:
					pass
			a += 1
			b += 1
	#print b
	listToReturn.append(winningCS)
	listToReturn.append(loosingCS)
	return listToReturn
"""
this function retrun what position in the list a player is, this is needed beause in the database players and there names are stored in the array participantIdentities but all the stats (champoins, CS, spells, wins/loss) is stored in the participants array so the location in the array is needed to find players stats.
"""
def getPlayerListNum(playerId):
	playerListNum = db.games.find({"participantIdentities.player.summonerId":playerId},{"participantIdentities.player.summonerId":1,"_id":0})
	for i in playerListNum:
		a=0
		for a in range(0,9):
			if i['participantIdentities'][a]['player']['summonerId'] == playerId:
				return a
			a += 1

"""
This function takes a players Id then calls the getPlayerListNum to get its position the array so it can then return the players total damage to champions.
"""
def getPlayerDmg(playerId):
	playerDmg = db.games.find({"participantIdentities.player.summonerId":playerId},{"participants.stats.totalDamageDealtToChampions":1,"_id":0})
	playListNum = getPlayerListNum(playerId)
	for i in playerDmg:
		return i['participants'][playListNum]['stats']['totalDamageDealtToChampions']

"""
This function will return a players estimated position (TOP/MID/DUO_SUPPORT/DUO_CARRY)
"""
def getPlayerPos(playerId):
	playerPos = db.games.find({"participantIdentities.player.summonerId":playerId},{"participants.timeline.role":1,"_id":0})
	pListNum = getPlayerListNum(playerId)
	for i in playerPos:
		return i['participants'][pListNum]['timeline']['role']
	
	
"""
This function will return all the stats of the playerId it is handed. outputs stats in a dict. It will also print out the stats in a readable format if the parameter "printOut" is true
"""
def getAllPlayerStats(playerId,printOut):
	playerStat = db.games.find({"participantIdentities.player.summonerId":playerId},{"participants.stats":1,"_id":0})
	pListNum = getPlayerListNum(playerId)
	for i in playerStat:
		if printOut == True:
			j = i['participants'][pListNum]['stats']
			for a, b in j.items():
				print a,":",b
			divider(50)
		return i['participants'][pListNum]['stats']

"""
This function will return the average player damage for each position, it must be handed the desired postion(TOP/MID/DUO_SUPPORT/DUO_CARRY). ##THIS IS NOT FINHSED##
"""
def getPlayerAvgDmg(pos,outputDmgList):
	listToAvg = []
	allPlayerDmg = db.games.find({"participants.timeline.role":pos},{"participants.stats.totalDamageDealtToChampions":1,"_id":0})
	for i in allPlayerDmg:
		j = i['participants'][0]['stats']
		for a,b in j.items():
			if outputDmgList == True:
				print a,":",b
			listToAvg.append(b)
	#print len(listToAvg)
	avg = 0
	for x in range(0,(len(listToAvg))):
		avg = avg + listToAvg[x]
	avg = avg/(len(listToAvg))
	return avg

"""
This function will return the averge gold for each position. 
"""
def getPlayerAvgGold(outputGoldList):
	listToAvg = []
	allPlayerDmg = db.games.find({"matchMode":"CLASSIC"},{"participants.stats.goldEarned":1,"_id":0})
	for i in allPlayerDmg:
		y = 0
		for y in range(0,10):
			j = i['participants'][y]['stats']
			for a,b in j.items():
				if outputGoldList == True:
					print a,":",b
				listToAvg.append(b)
			y += 1
	print len(listToAvg)
	avg = 0
	for x in range(0,(len(listToAvg))):
		avg = avg + listToAvg[x]
	avg = avg/(len(listToAvg))
	return avg

"""
gets a list of champions played by everyone, all positions. There may be an issue with the printout of Id(might be hitting output limit in python)
"""
def getChampions(printChamps):
	listToReturn = []
	champs = db.games.find({"matchMode":"CLASSIC"},{"participants.championId":1,"_id":0})
	a = 0
	for i in champs:
		while a<10:
			if printChamps == True:
				print i['participants'][a]['championId']
			listToReturn.append(i['participants'][a]['championId'])
			#print a
			a += 1
		if a>9:
			a = 0
	#print len(listToReturn)
	return listToReturn
	
"""
This function returns a list of all the wins 
"""
def getWinList():
	wins = db.games.find({"matchMode":"CLASSIC"},{"participants.stats.winner"})
	winsList = []
	a = 0
	for i in wins:
		while a<10:
			winsList.append(i['participants'][a]['stats']['winner'])
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
This will return a list of all the playerId in all the games
"""
def getPlayerId():
	listOfPlayers = []
	players = db.games.find({"matchMode":"CLASSIC"},{"participantIdentities.player.summonerId":1,"_id":0})
	a = 0
	for i in players:
		while a<10:
			listOfPlayers.append(i['participantIdentities'][a]['player']['summonerId'])
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
	listToReturn = []
	item0 = db.games.find({"matchMode":"CLASSIC"},{"participants.stats":1,"_id":0})	
	a = 0
	for i in item0:
		while a<10:
			l = i['participants'][a]['stats']
			if printItems == True:
				print "item 0: ",l['item0']
				print "item 1: ",l['item1']
				print "item 2: ",l['item2']
				print "item 3: ",l['item3']
				print "item 4: ",l['item4']
				print "item 5: ",l['item5']	
			if l['item0'] != 0:
				listToReturn.append(l['item0'])
			if l['item1'] != 0:
				listToReturn.append(l['item1'])
			if l['item2'] != 0:
				listToReturn.append(l['item2'])
			if l['item3'] != 0:
				listToReturn.append(l['item3'])
			if l['item4'] != 0:
				listToReturn.append(l['item4'])
			if l['item5'] != 0:
				listToReturn.append(l['item5'])
			a += 1
		if a>9:
			a = 0
	return listToReturn	
	
"""
This function will return the most popular items
"""
def mostCommonItem(numToList):
	items = getItems(False)
	
	mostCommon = findMostCommon(items,numToList)
	return mostCommon
	
"""
Finds what items have the highers win rate, ignores trinkets becuase everone gets them
"""
def highestWinRateItem():
	winningItems = []
	loosingItems = []
	items = db.games.find({"matchMode":"CLASSIC"},{"participants.stats":1,"_id":0})
	for i in items:
		a = 0
		while a<10:
			if i['participants'][a]['stats']['winner'] == True:
				if i['participants'][a]['stats']['item0'] != 0:
					winningItems.append(i['participants'][a]['stats']['item0'])
				if i['participants'][a]['stats']['item1'] != 0:
					winningItems.append(i['participants'][a]['stats']['item1'])
				if i['participants'][a]['stats']['item2'] != 0:
					winningItems.append(i['participants'][a]['stats']['item2'])
				if i['participants'][a]['stats']['item3'] != 0:
					winningItems.append(i['participants'][a]['stats']['item3'])
				if i['participants'][a]['stats']['item4'] != 0:
					winningItems.append(i['participants'][a]['stats']['item4'])
				if i['participants'][a]['stats']['item5'] != 0:
					winningItems.append(i['participants'][a]['stats']['item5'])
			else:
				if i['participants'][a]['stats']['item0'] != 0:
					loosingItems.append(i['participants'][a]['stats']['item0'])
				if i['participants'][a]['stats']['item1'] != 0:
					loosingItems.append(i['participants'][a]['stats']['item1'])
				if i['participants'][a]['stats']['item2'] != 0:
					loosingItems.append(i['participants'][a]['stats']['item2'])
				if i['participants'][a]['stats']['item3'] != 0:
					loosingItems.append(i['participants'][a]['stats']['item3'])
				if i['participants'][a]['stats']['item4'] != 0:
					loosingItems.append(i['participants'][a]['stats']['item4'])
				if i['participants'][a]['stats']['item5'] != 0:
					loosingItems.append(i['participants'][a]['stats']['item5'])
			a += 1
	bestItems = findMostCommon(winningItems,6)
	worstItems = findMostCommon(loosingItems,6)
	print bestItems
	print worstItems
	
	
"""
This function will compare the is the winning team was the first to do something, eg did the winning team get first blood, it must be handed the DB locations, objective name and bool for printing out data
can be handed:
"teams.firstBlood","firstBlood",False
"teams.firstBaron","firstBaron",False
"teams.firstDragon","firstDragon",False
"teams.firsTower","firstTower",False
"teams.firstInhibitor","firstInhibitor",False
"""
def firstObjectiveTemplate(obLoc,ob,outputTF):
	listWinners = []
	listObs =[]
	firstBlood = db.games.find({"matchMode":"CLASSIC"},{obLoc:1,"teams.winner":1,"_id":0})
	for i in firstBlood:
		if outputTF == True:
			print "Win Team1: ",i['teams'][0]['winner']
			print ob," Team1: ",i['teams'][0][ob]
			print "Win Team 2: ",i['teams'][1]['winner']
			print ob," Team2 :",i['teams'][1][ob]
		listWinners.append(i['teams'][0]['winner'])
		listObs.append(i['teams'][0][ob])
		listWinners.append(i['teams'][1]['winner'])
		listObs.append(i['teams'][1][ob])
	#print len(listWinners)
	#print len(listFirstBloods)
	totalWinObTrue = 0
	totalWinObFalse = 0
	for i in range(0,len(listWinners)):
		#print listWinners[i]
		#sprint listFirstBloods[i]
		if listWinners[i] == True and listObs[i] == True:
			totalWinObTrue = totalWinObTrue + 1
		elif listWinners[i] == True and listObs[i] == False or listWinners[i] == True and listObs[i] == False:
			totalWinObFalse = totalWinObFalse + 1
	#print totalWinObTrue		
	#print totalWinObFalse
	if totalWinObTrue>totalWinObFalse:
		return True
	else:
		return False	

"""
This function will find what bans coralate with winning
"""
def winningBans():
	winBanList = []
	winBan = db.games.find({"matchMode":"CLASSIC"},{"teams.winner":1,"teams.bans":1,"_id":0})
	for i in winBan:
		j = i['teams'][0]['winner']
		k = i['teams'][1]['winner']
		a = 0
		while a<2:
			if j == True:
				l = i['teams'][0]['bans'][a]['championId']
			else:
				l = i['teams'][1]['bans'][a]['championId']
			winBanList.append(l)
			a +=1
	return findMostCommon(winBanList,3)
	
"""
This function will show if winning players place more wards then loosing players, it retruns a list:
1nd value is the average wards placed by a winner
2rd value is the average wards placed by a looser 
3st value is True/False (True if winners place more wards, false is looser place more wards)
## MIGHT NEED TO ADD SOMETHING TO EMPTY LIST "listToReturn" ##
"""
def wardBoughtTrend():
	winningTeamWards = 0
	loosingTeamWards = 0
	listToReturn = []
	wardsPlaced = db.games.find({"matchMode":"CLASSIC"},{"participants.stats.visionWardsBoughtInGame":1,"participants.stats.sightWardsBoughtInGame":1,"participants.stats.winner":1,"teams.winner":1,"_id":0})
	for i in wardsPlaced:
		a = 0
		while a<10:
			if i['participants'][a]['stats']['winner'] == True:
				winningTeamWards = winningTeamWards + i['participants'][a]['stats']['sightWardsBoughtInGame'] + i['participants'][a]['stats']['visionWardsBoughtInGame']
			else:
				loosingTeamWards = loosingTeamWards + i['participants'][a]['stats']['sightWardsBoughtInGame'] + i['participants'][a]['stats']['visionWardsBoughtInGame']
			a += 1
	winningTeamAvg = winningTeamWards/1000.0
	loosingTeamAvg = loosingTeamWards/1000.0
	#print winningTeamWards
	#print loosingTeamWards
	#print winningTeamAvg
	#print loosingTeamAvg
	listToReturn.append(winningTeamAvg)
	listToReturn.append(loosingTeamAvg)
	if winningTeamAvg > loosingTeamAvg:
		listToReturn.append(True)
		return listToReturn
	elif loosingTeamAvg > winningTeamAvg:
		listToReturn.append(False)
		return listToReturn
	else:
		return "There is no difference" #this is very unlikely to happen 


"""
this functions if the team with the most towers normally win. It returns a list:
1st value is the avg winning team towers
2nd value is the avg loosing team towers
3rd value is a bool, True if winners get more towers, False if loosers get mroe towers
"""
def mostTowersWin():
	winningTeamTowers = 0
	loosingTeamTowers = 0
	listToReturn = []
	towers = db.games.find({"matchMode":"CLASSIC"},{"teams.winner":1,"teams.towerKills":1,"_id":0})
	for i in towers:
		if i['teams'][0]['winner'] == True:
			winningTeamTowers = winningTeamTowers + i['teams'][0]['towerKills']
			loosingTeamTowers = loosingTeamTowers + i['teams'][1]['towerKills']
		else:
			winningTeamTowers = winningTeamTowers + i['teams'][1]['towerKills']
			loosingTeamTowers = loosingTeamTowers + i['teams'][0]['towerKills']
	if winningTeamTowers>loosingTeamTowers:
		listToReturn.append(winningTeamTowers/1000.0,loosingTeamTowers/1000.0,True)
	else:
		listToReturn.append(winningTeamTowers/1000.0,loosingTeamTowers/1000.0,False)

"""
adds up CS difference and finds out if winning teams had more CS, this is the Delta difference not difference in actual CS
"""
def csDiffWin():
	listToReturn = []
	csDiff = getCsDiff()
	if csDiff[0] > csDiff[1]:
		listToReturn.append((csDiff[0]/10000.0)-csDiff[1]/10000.0)
		listToReturn.append(True)
		return listToReturn
	else:
		listToReturn.append((csDiff[1]/10000.0)-csDiff[0]/10000.0)
		listToReturn.append(False)
		return listToReturn	

"""
adds up the dmg done by each team member to get total team dmg and finds out if the winning teams did more dmg. It retruns a list with 3 items:
1st average winner damage
2nd average looser damage
3rd True if winners do more damage, False if looser do more damage
"""
def dmgDiffWin():
	listToReturn = []
	winnerDmg = 0
	looserDmg = 0
	damage = db.games.find({"matchMode":"CLASSIC"},{"participants.stats.winner":1,"participants.stats.totalDamageDealtToChampions":1,"_id":0})
	for i in damage:
		a = 0
		while a<10:
			if i['participants'][a]['stats']['winner'] == True:
				winnerDmg = winnerDmg + i['participants'][a]['stats']['totalDamageDealtToChampions']
				#print i['participants'][a]['stats']['totalDamageDealtToChampions']
			else:
				looserDmg = looserDmg + i['participants'][a]['stats']['totalDamageDealtToChampions']
			a += 1
	listToReturn.append(winnerDmg/10000.0)
	listToReturn.append(looserDmg/10000.0)
	if winnerDmg > looserDmg:
		listToReturn.append(True)
		return listToReturn
	else:
		listToReturn.append(False)
		return listToReturn


"""
adds up gold differences of each player to find team gold then finds if winning teams had more gold
"""	
def goldDiffWin():
	listToReturn = []
	winnerGold = 0
	looserGold = 0
	gold = db.games.find({"matchMode":"CLASSIC"},{"participants.stats.winner":1,"participants.stats.goldEarned":1,"_id":0})
	for i in gold:
		a = 0
		while a<10:
			if i['participants'][a]['stats']['winner'] == True:
				winnerGold = winnerGold + i['participants'][a]['stats']['goldEarned']
			else:
				looserGold = looserGold + i['participants'][a]['stats']['goldEarned']
			a += 1
	listToReturn.append(winnerGold/10000)
	listToReturn.append(looserGold/10000)
	if winnerGold > looserGold:
		listToReturn.append(True)
		return listToReturn
	else:
		listToReturn.append(False)
		return listToReturn
	



print goldDiffWin()

class display():
	def displayData():
		print ""

client.close()


"""
abcdefghijklmnopqrst
"""