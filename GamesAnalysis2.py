from pymongo import MongoClient
client = MongoClient()
db = client.lolMatchesDB

"""
This class was mostly used for test the structure of the data, it does not analyse data, only outputs raw data from DB
"""
class singleDataOutputs():
	"""
	This functions takes a matchId as a paramerter then returns which team won.
	"""
	def getGameResult(self,matchId):
		self.gameResult = db.games.find({"matchId":matchId},{"teams.winner":1})
		for self.i in self.gameResult:
			if self.i['teams'][0]['winner'] == True:
				return "Team 1"
			else:
				return "Team 2"
	
	"""
	This fucntion is handed a matchId and playerId then returns there Id with the game result (win/loss).
	"""
	def getPlayerWin(self,matchId,playerId):
		self.winsToRetrun = []
		self.playerToReturn = []
		self.playerWinDict = db.games.find({"matchId":matchId},{"participants.stats.winner":1,"_id":0})
		self.playerIdDict = db.games.find({"matchId":matchId},{"participantIdentities.player.summonerId":1,"_id":0})
		self.a=0
		self.b=0
		for self.i in self.playerWinDict:
			self.winsToRetrun.append(i['participants'][a]['stats']['winner'])
			self.a += 1
		for self.i in self.playerIdDict:
			self.playerToReturn.append(i['participantIdentities'][b]['player']['summonerId'])
		for self.i in range(len(self.playerToReturn)):
			return self.playerToReturn[i],self.winsToRetrun[i]

	"""
	this function gets the matchId and game winner from the database, it then outputs all the results of each game.
	"""
	def returnAllWinners(self):
		self.gameResult = db.games.find({"teams.winner":True},{"matchId":1,"teams.winner":1,})
	
		for self.i in self.gameResult:
			if self.i['teams'][0]['winner'] == True:
				print "Winner: Team 1"
			else:
				print "Winner: Team 2"
	
	"""
	This function takes a players Id then calls the getPlayerListNum to get its position the array so it can then return the players total damage to champions.
	"""
	def getPlayerDmg(self,playerId):
		self.playerDmg = db.games.find({"participantIdentities.player.summonerId":playerId},{"participants.stats.totalDamageDealtToChampions":1,"_id":0})
		self.playListNum = getPlayerListNum(playerId)
		for self.i in self.playerDmg:
			return self.i['participants'][self.playListNum]['stats']['totalDamageDealtToChampions']	

	"""
	This function will return a players estimated position (TOP/MID/DUO_SUPPORT/DUO_CARRY)
	"""
	def getPlayerPos(self,playerId):
		self.playerPos = db.games.find({"participantIdentities.player.summonerId":playerId},{"participants.timeline.role":1,"_id":0})
		self.pListNum = getPlayerListNum(playerId)
		for self.i in self.playerPos:
			return self.i['participants'][self.pListNum]['timeline']['role']
		
		
	"""
	This function will return all the stats of the playerId it is handed. outputs stats in a dict. It will also print out the stats in a readable format if the parameter "printOut" is true
	"""
	def getAllPlayerStats(self,playerId,printOut):
		self.playerStat = db.games.find({"participantIdentities.player.summonerId":playerId},{"participants.stats":1,"_id":0})
		self.pListNum = getPlayerListNum(playerId)
		for self.i in self.playerStat:
			if printOut == True:
				self.j = self.i['participants'][self.pListNum]['stats']
				for self.a, self.b in self.j.items():
					print self.a,":",self.b
				divider(50)
			return self.i['participants'][self.pListNum]['stats']
	
class massDataAnalsis():

	"""
	This functions will return total of the winners CSdelta and the total of the loosers CSDelta, returns them in a list:
	1st winners total CS delta
	2nd looser total CS delfa
	"""
	def getCsDiff(self):
		self.listToReturn = []
		self.winningCS = 0
		self.loosingCS = 0
		self.playersCsDiff = db.games.find({"matchMode":"CLASSIC"},{"participants.timeline.csDiffPerMinDeltas":1,"participants.stats.winner":1,"_id":0})
		
		#for i in playersCsDiff:
			#print i
		self.b = 0
		for self.i in self.playersCsDiff:
			self.a = 0
			
			while self.a<10:
				if self.i['participants'][self.a]['stats']['winner'] == True:
					try:
						self.winningCS = self.winningCS + self.i['participants'][self.a]['timeline']['csDiffPerMinDeltas']['zeroToTen']
					except KeyError:
						pass
					try:
						self.winningCS = self.winningCS + self.i['participants'][self.a]['timeline']['csDiffPerMinDeltas']['tenToTwenty']
					except KeyError:
						pass
					try:
						self.winningCS = self.winningCS + self.i['participants'][self.a]['timeline']['csDiffPerMinDeltas']['twentyToThrity']
					except KeyError:
						pass
					try:
						self.winningCS = self.winningCS + self.i['participants'][self.a]['timeline']['csDiffPerMinDeltas']['thirtyToEnd']
					except KeyError:
						pass	
				else:
					try:
						self.loosingCS = self.loosingCS + self.i['participants'][self.a]['timeline']['csDiffPerMinDeltas']['zeroToTen']
					except KeyError:
						pass
					try:
						self.loosingCS = self.loosingCS + self.i['participants'][self.a]['timeline']['csDiffPerMinDeltas']['tenToTwenty']
					except KeyError:
						pass
					try:
						self.loosingCS = self.loosingCS + self.i['participants'][self.a]['timeline']['csDiffPerMinDeltas']['twentyToThrity']
					except KeyError:
						pass
					try:
						self.loosingCS = self.loosingCS + self.i['participants'][self.a]['timeline']['csDiffPerMinDeltas']['thirtyToEnd']
					except KeyError:
						pass
				self.a += 1
				self.b += 1
		#print b
		self.listToReturn.append(self.winningCS)
		self.listToReturn.append(self.loosingCS)
		return self.listToReturn
	"""
	this function retrun what position in the list a player is, this is needed beause in the database players and there names are stored in the array participantIdentities but all the stats (champoins, CS, spells, wins/loss) is stored in the participants array so the location in the array is needed to find players stats.
	"""
	def getPlayerListNum(self,playerId):
		self.playerListNum = db.games.find({"participantIdentities.player.summonerId":playerId},{"participantIdentities.player.summonerId":1,"_id":0})
		for self.i in self.playerListNum:
			self.a=0
			for self.a in range(0,9):
				if self.i['participantIdentities'][a]['player']['summonerId'] == playerId:
					return self.a
				self.a += 1
	
	
	"""
	This function will return the average player damage for each position, it must be handed the desired postion(TOP/MID/DUO_SUPPORT/DUO_CARRY). ##THIS IS NOT FINHSED##
	"""
	def getPlayerAvgDmg(self,pos,outputDmgList):
		self.listToAvg = []
		self.allPlayerDmg = db.games.find({"participants.timeline.role":pos},{"participants.stats.totalDamageDealtToChampions":1,"_id":0})
		for self.i in self.allPlayerDmg:
			self.j = self.i['participants'][0]['stats']
			for self.a,self.b in self.j.items():
				if self.outputDmgList == True:
					print self.a,":",self.b
				self.listToAvg.append(self.b)
		#print len(listToAvg)
		self.avg = 0
		for self.x in range(0,(len(self.listToAvg))):
			self.avg = self.avg + self.listToAvg[x]
		self.avg = self.avg/(len(self.listToAvg))
		return self.avg
	
	"""
	This function will return the averge gold for each position. 
	"""
	def getPlayerAvgGold(self,outputGoldList):
		self.listToAvg = []
		self.allPlayerDmg = db.games.find({"matchMode":"CLASSIC"},{"participants.stats.goldEarned":1,"_id":0})
		for self.i in self.allPlayerDmg:
			self.y = 0
			for self.y in range(0,10):
				self.j = self.i['participants'][y]['stats']
				for self.a,self.b in self.j.items():
					if self.outputGoldList == True:
						print self.a,":",self.b
					self.listToAvg.append(self.b)
				self.y += 1
		print len(self.listToAvg)
		self.avg = 0
		for self.x in range(0,(len(self.listToAvg))):
			self.avg = self.avg + self.listToAvg[x]
		self.avg = self.avg/(len(self.listToAvg))
		return self.avg
	
	"""
	gets a list of champions played by everyone, all positions. There may be an issue with the printout of Id(might be hitting output limit in python)
	"""
	def getChampions(self,printChamps):
		self.listToReturn = []
		self.champs = db.games.find({"matchMode":"CLASSIC"},{"participants.championId":1,"_id":0})
		self.a = 0
		for self.i in self.champs:
			while self.a<10:
				if printChamps == True:
					print self.i['participants'][self.a]['championId']
				self.listToReturn.append(self.i['participants'][self.a]['championId'])
				#print a
				self.a += 1
			if self.a>9:
				self.a = 0
		#print len(listToReturn)
		return self.listToReturn
		
	"""
	This function returns a list of all the wins 
	"""
	def getWinList(self):
		self.wins = db.games.find({"matchMode":"CLASSIC"},{"participants.stats.winner"})
		self.winsList = []
		self.a = 0
		for self.i in self.wins:
			while self.a<10:
				self.winsList.append(self.i['participants'][self.a]['stats']['winner'])
				self.a += 1
			if self.a>9:
				self.a = 0
		return self.winsList
		print ""
	
		
	"""
	This function will return most common position in each role. IMPORTANT: item is returned is a list with only 1 item
	"""
	def mostCommonChamp(self,numToOutput):
		self.champs = massDataAnalsis().getChampions(False)
		self.toReturn = massDataAnalsis().findMostCommon(self.champs,numToOutput)
		return self.toReturn
	
	"""
	This will return a list of all the playerId in all the games
	"""
	def getPlayerId(self):
		self.listOfPlayers = []
		self.players = db.games.find({"matchMode":"CLASSIC"},{"participantIdentities.player.summonerId":1,"_id":0})
		self.a = 0
		for self.i in self.players:
			while self.a<10:
				self.listOfPlayers.append(self.i['participantIdentities'][self.a]['player']['summonerId'])
				self.a += 1
			if self.a>9:
				self.a = 0
		return(self.listOfPlayers)
	
	"""
	This function will find the most common items in a list handed to it, the "numToOutput" is how many of the most common to return, eg "2" will return the 2 most common items in the list.
	"""
	def findMostCommon(self,listToUse,numToOutput):
		self.a = {}
		for self.i in listToUse:
			if self.i in self.a:
				self.a[self.i] += 1
			else:
				self.a[self.i] = 1
		self.mostCommon = sorted(self.a, key = self.a.get, reverse = True)
		return self.mostCommon[:numToOutput]	
		
	"""
	This funciton will return the highest win rate champion, if "returnLooser" is True then it will retrun the most common looser instead of the winner. (will return a list)
	"""
	def highestWinRateChampion(self,numToList,returnLoosers):
		self.onlyWinners = []
		self.onlyLoosers = []
		self.champsList = massDataAnalsis().getChampions(False)
		self.winList = massDataAnalsis().getWinList()
		#print len(self.winList)
		#print len(self.champsList)
		#print self.winList[5]
		for i in range (0,10000):
			if self.winList[i] == True:
				self.onlyWinners.append(self.champsList[i])
			else:
				self.onlyLoosers.append(self.champsList[i])
		self.mostCommonWinner = massDataAnalsis().findMostCommon(self.onlyWinners,numToList)
		if returnLoosers == True:
			self.mostCommonLooser = massDataAnalsis().findMostCommon(self.onlyLoosers,numToList)
			return self.mostCommonLooser
		return self.mostCommonWinner
		
	"""
	This function will return a list with all the items bought in the all the games
	"""
	def getItems(self,printItems):
		self.listToReturn = []
		self.item0 = db.games.find({"matchMode":"CLASSIC"},{"participants.stats":1,"_id":0})	
		self.a = 0
		for self.i in self.item0:
			while self.a<10:
				self.l = self.i['participants'][self.a]['stats']
				if printItems == True:
					print "item 0: ",l['item0']
					print "item 1: ",l['item1']
					print "item 2: ",l['item2']
					print "item 3: ",l['item3']
					print "item 4: ",l['item4']
					print "item 5: ",l['item5']	
				if self.l['item0'] != 0:
					self.listToReturn.append(self.l['item0'])
				if self.l['item1'] != 0:
					self.listToReturn.append(self.l['item1'])
				if self.l['item2'] != 0:
					self.listToReturn.append(self.l['item2'])
				if self.l['item3'] != 0:
					self.listToReturn.append(self.l['item3'])
				if self.l['item4'] != 0:
					self.listToReturn.append(self.l['item4'])
				if self.l['item5'] != 0:
					self.listToReturn.append(self.l['item5'])
				self.a += 1
			if self.a>9:
				self.a = 0
		return self.listToReturn	
		
	"""
	This function will return the most popular items
	"""
	def mostCommonItem(self,numToList):
		self.items = massDataAnalsis().getItems(False)
		
		self.mostCommon = massDataAnalsis().findMostCommon(self.items,numToList)
		return self.mostCommon
		
	"""
	Finds what items have the highers win rate, ignores trinkets becuase everone gets them
	must be haned bool winnerOrLoosers, True to retrun best items False to return worst items
	"""
	def highestWinRateItem(self,winnersOrLoosers):
		self.winningItems = []
		self.loosingItems = []
		self.items = db.games.find({"matchMode":"CLASSIC"},{"participants.stats":1,"_id":0})
		for self.i in self.items:
			self.a = 0
			while self.a<10:
				if self.i['participants'][self.a]['stats']['winner'] == True:
					if self.i['participants'][self.a]['stats']['item0'] != 0:
						self.winningItems.append(self.i['participants'][self.a]['stats']['item0'])
					if self.i['participants'][self.a]['stats']['item1'] != 0:
						self.winningItems.append(self.i['participants'][self.a]['stats']['item1'])
					if self.i['participants'][self.a]['stats']['item2'] != 0:
						self.winningItems.append(self.i['participants'][self.a]['stats']['item2'])
					if self.i['participants'][self.a]['stats']['item3'] != 0:
						self.winningItems.append(self.i['participants'][self.a]['stats']['item3'])
					if self.i['participants'][self.a]['stats']['item4'] != 0:
						self.winningItems.append(self.i['participants'][self.a]['stats']['item4'])
					if self.i['participants'][self.a]['stats']['item5'] != 0:
						self.winningItems.append(self.i['participants'][self.a]['stats']['item5'])
				else:
					if self.i['participants'][self.a]['stats']['item0'] != 0:
						self.loosingItems.append(self.i['participants'][self.a]['stats']['item0'])
					if self.i['participants'][self.a]['stats']['item1'] != 0:
						self.loosingItems.append(self.i['participants'][self.a]['stats']['item1'])
					if self.i['participants'][self.a]['stats']['item2'] != 0:
						self.loosingItems.append(self.i['participants'][self.a]['stats']['item2'])
					if self.i['participants'][self.a]['stats']['item3'] != 0:
						self.loosingItems.append(self.i['participants'][self.a]['stats']['item3'])
					if self.i['participants'][self.a]['stats']['item4'] != 0:
						self.loosingItems.append(self.i['participants'][self.a]['stats']['item4'])
					if self.i['participants'][self.a]['stats']['item5'] != 0:
						self.loosingItems.append(self.i['participants'][self.a]['stats']['item5'])
				self.a += 1
		self.bestItems = massDataAnalsis().findMostCommon(self.winningItems,6)
		self.worstItems = massDataAnalsis().findMostCommon(self.loosingItems,6)
		if winnersOrLoosers == True:
			return self.bestItems
		elif winnersOrLoosers == False:
			return self.worstItems
		else:
			return "highestWinRateItem must be hanned a boolean"
		
		
	"""
	This function will compare the is the winning team was the first to do something, eg did the winning team get first blood, it must be handed the DB locations, objective name and bool for printing out data
	can be handed:
	"teams.firstBlood","firstBlood",False
	"teams.firstBaron","firstBaron",False
	"teams.firstDragon","firstDragon",False
	"teams.firstTower","firstTower",False
	"teams.firstInhibitor","firstInhibitor",False
	"""
	def firstObjectiveTemplate(self,obLoc,ob,outputTF):
		self.listWinners = []
		self.listObs =[]
		self.firstBlood = db.games.find({"matchMode":"CLASSIC"},{obLoc:1,"teams.winner":1,"_id":0})
		for self.i in self.firstBlood:
			if outputTF == True:
				print "Win Team1: ",self.i['teams'][0]['winner']
				print ob," Team1: ",self.i['teams'][0][ob]
				print "Win Team 2: ",self.i['teams'][1]['winner']
				print ob," Team2 :",self.i['teams'][1][ob]
			self.listWinners.append(self.i['teams'][0]['winner'])
			self.listObs.append(self.i['teams'][0][ob])
			self.listWinners.append(self.i['teams'][1]['winner'])
			self.listObs.append(self.i['teams'][1][ob])
		#print len(listWinners)
		#print len(listFirstBloods)
		self.totalWinObTrue = 0
		self.totalWinObFalse = 0
		for self.i in range(0,len(self.listWinners)):
			#print listWinners[i]
			#sprint listFirstBloods[i]
			if self.listWinners[self.i] == True and self.listObs[self.i] == True:
				self.totalWinObTrue = self.totalWinObTrue + 1
			elif self.listWinners[self.i] == True and self.listObs[self.i] == False or self.listWinners[self.i] == True and self.listObs[self.i] == False:
				self.totalWinObFalse = self.totalWinObFalse + 1
		#print totalWinObTrue		
		#print totalWinObFalse
		return self.totalWinObTrue/10.0
	"""
	This function will find what bans coralate with winning
	"""
	def winningBans(self):
		self.winBanList = []
		self.winBan = db.games.find({"matchMode":"CLASSIC"},{"teams.winner":1,"teams.bans":1,"_id":0})
		for self.i in self.winBan:
			self.j = self.i['teams'][0]['winner']
			self.k = self.i['teams'][1]['winner']
			self.a = 0
			while self.a<2:
				if self.j == True:
					self.l = self.i['teams'][0]['bans'][self.a]['championId']
				else:
					self.l = self.i['teams'][1]['bans'][self.a]['championId']
				self.winBanList.append(self.l)
				self.a +=1
		return massDataAnalsis().findMostCommon(self.winBanList,3)
		
	"""
	This function will show if winning players place more wards then loosing players, it retruns a list:
	1nd value is the average wards placed by a winner
	2rd value is the average wards placed by a looser 
	3st value is True/False (True if winners place more wards, false is looser place more wards)
	## MIGHT NEED TO ADD SOMETHING TO EMPTY LIST "listToReturn" ##
	"""
	def wardBoughtTrend(self):
		self.winningTeamWards = 0
		self.loosingTeamWards = 0
		self.listToReturn = []
		self.wardsPlaced = db.games.find({"matchMode":"CLASSIC"},{"participants.stats.visionWardsBoughtInGame":1,"participants.stats.sightWardsBoughtInGame":1,"participants.stats.winner":1,"teams.winner":1,"_id":0})
		for self.i in self.wardsPlaced:
			self.a = 0
			while self.a<10:
				if self.i['participants'][self.a]['stats']['winner'] == True:
					self.winningTeamWards = self.winningTeamWards + self.i['participants'][self.a]['stats']['sightWardsBoughtInGame'] + self.i['participants'][self.a]['stats']['visionWardsBoughtInGame']
				else:
					self.loosingTeamWards = self.loosingTeamWards + self.i['participants'][self.a]['stats']['sightWardsBoughtInGame'] + self.i['participants'][self.a]['stats']['visionWardsBoughtInGame']
				self.a += 1
		self.winningTeamAvg = self.winningTeamWards/1000.0
		self.loosingTeamAvg = self.loosingTeamWards/1000.0
		#print winningTeamWards
		#print loosingTeamWards
		#print winningTeamAvg
		#print loosingTeamAvg
		self.listToReturn.append(self.winningTeamAvg)
		self.listToReturn.append(self.loosingTeamAvg)
		if self.winningTeamAvg > self.loosingTeamAvg:
			self.listToReturn.append(True)
			return self.listToReturn
		elif self.loosingTeamAvg > self.winningTeamAvg:
			self.listToReturn.append(False)
			return self.listToReturn
		else:
			return "There is no difference" #this is very unlikely to happen 
	
	
	"""
	this functions if the team with the most towers normally win. It returns a list:
	1st value is the avg winning team towers
	2nd value is the avg loosing team towers
	3rd value is a bool, True if winners get more towers, False if loosers get mroe towers
	"""
	def mostTowersWin(self):
		self.winningTeamTowers = 0
		self.loosingTeamTowers = 0
		self.listToReturn = []
		self.towers = db.games.find({"matchMode":"CLASSIC"},{"teams.winner":1,"teams.towerKills":1,"_id":0})
		for self.i in self.towers:
			if self.i['teams'][0]['winner'] == True:
				self.winningTeamTowers = self.winningTeamTowers + self.i['teams'][0]['towerKills']
				self.loosingTeamTowers = self.loosingTeamTowers + self.i['teams'][1]['towerKills']
			else:
				self.winningTeamTowers = self.winningTeamTowers + self.i['teams'][1]['towerKills']
				self.loosingTeamTowers = self.loosingTeamTowers + self.i['teams'][0]['towerKills']
		self.listToReturn.append(self.winningTeamTowers/1000.0)
		self.listToReturn.append(self.loosingTeamTowers/1000.0)
		if self.winningTeamTowers>self.loosingTeamTowers:
			self.listToReturn.append(True)
		else:
			self.listToReturn.append(False)
		return self.listToReturn
	"""
	adds up CS difference and finds out if winning teams had more CS, this is the Delta difference not difference in actual CS
	"""
	def csDiffWin(self):
		self.listToReturn = []
		self.csDiff = massDataAnalsis().getCsDiff()
		if self.csDiff[0] > self.csDiff[1]:
			self.listToReturn.append((self.csDiff[0]/10000.0)-self.csDiff[1]/10000.0)
			self.listToReturn.append(True)
			return self.listToReturn
		else:
			self.listToReturn.append((self.csDiff[1]/10000.0)-self.csDiff[0]/10000.0)
			self.listToReturn.append(False)
			return self.listToReturn	
	
	"""
	adds up the dmg done by each team member to get total team dmg and finds out if the winning teams did more dmg. It retruns a list with 3 items:
	1st average winner damage
	2nd average looser damage
	3rd True if winners do more damage, False if looser do more damage
	"""
	def dmgDiffWin(self):
		self.listToReturn = []
		self.winnerDmg = 0
		self.looserDmg = 0
		self.damage = db.games.find({"matchMode":"CLASSIC"},{"participants.stats.winner":1,"participants.stats.totalDamageDealtToChampions":1,"_id":0})
		for self.i in self.damage:
			self.a = 0
			while self.a<10:
				if self.i['participants'][self.a]['stats']['winner'] == True:
					self.winnerDmg = self.winnerDmg + self.i['participants'][self.a]['stats']['totalDamageDealtToChampions']
					#print i['participants'][a]['stats']['totalDamageDealtToChampions']
				else:
					self.looserDmg = self.looserDmg + self.i['participants'][self.a]['stats']['totalDamageDealtToChampions']
				self.a += 1
		self.listToReturn.append(self.winnerDmg/10000.0)
		self.listToReturn.append(self.looserDmg/10000.0)
		if self.winnerDmg > self.looserDmg:
			self.listToReturn.append(True)
			return self.listToReturn
		else:
			self.listToReturn.append(False)
			return self.listToReturn
	
	
	"""
	adds up gold differences of each player to find team gold then finds if winning teams had more gold
	"""	
	def goldDiffWin(self):
		self.listToReturn = []
		self.winnerGold = 0
		self.looserGold = 0
		self.gold = db.games.find({"matchMode":"CLASSIC"},{"participants.stats.winner":1,"participants.stats.goldEarned":1,"_id":0})
		for self.i in self.gold:
			self.a = 0
			while self.a<10:
				if self.i['participants'][self.a]['stats']['winner'] == True:
					self.winnerGold = self.winnerGold + self.i['participants'][self.a]['stats']['goldEarned']
				else:
					self.looserGold = self.looserGold + self.i['participants'][self.a]['stats']['goldEarned']
				self.a += 1
		self.listToReturn.append(self.winnerGold/10000)
		self.listToReturn.append(self.looserGold/10000)
		if self.winnerGold > self.looserGold:
			self.listToReturn.append(True)
			return self.listToReturn
		else:
			self.listToReturn.append(False)
			return self.listToReturn
			

class display():
	"""
	this functions prints out a divider made "=" for the length it is handed.
	"""
	def divider(self,length):
		self.string = "="
		for self.i in range(0,length):
			self.string = self.string + "="
		print self.string 
	"""
	This will display all the data in a readable fashion
	"""
	def displayData(self):
		display().divider(50)
		
		#CHAMPION STATS
		print "CHAMPION ANALYTICS"
		print "Most common champions"
		self.mostUsedChamps = massDataAnalsis().mostCommonChamp(5)
		print self.mostUsedChamps
		print "\n \n"
		
		print "Highest winrate champions:"
		#self.bestChamps = massDataAnalsis().highestWinRateChampion(5,True)
		#print self.bestChamps
		
		display().divider(50)
		
		#ITEM STATS
		print "ITEM ANALYTICS"
		
		self.mostUsedItems = massDataAnalsis().mostCommonItem(6)
		print "Most used items"
		print self.mostUsedItems
		print "\n \n"
		
		print "Highest win rate items"
		self.mostWinItems = massDataAnalsis().highestWinRateItem(True)
		print self.mostWinItems
		 
		display().divider(50)
		
		#OBJECTIVE STATS
		print "OBJECTIVE ANALYTICS"
		
		print "On average winning teams get:"
		self.mostTowers = massDataAnalsis().mostTowersWin()
		print self.mostTowers[0], "Towers per game"
		print "loosing teams average:" 
		print self.mostTowers[1], "Towers per game"
		print "\n \n"
		
		print "Teams that get first blood win"
		self.firstBlood = massDataAnalsis().firstObjectiveTemplate("teams.firstBlood","firstBlood",False)
		print self.firstBlood,"% of the time " 
		print "\n \n"
		
		print "Teams that get first dragon win"
		self.firstDrag = massDataAnalsis().firstObjectiveTemplate("teams.firstDragon","firstDragon",False)
		print self.firstDrag, "% of the time"
		print "\n \n"
		
		print "Teams that get first baron win"
		self.firstBaron = massDataAnalsis().firstObjectiveTemplate("teams.firstBaron","firstBaron",False)
		print self.firstBaron, "% of the time"
		print "\n \n"
		
		print "Teams that get the first tower win"
		self.firstTower = massDataAnalsis().firstObjectiveTemplate("teams.firstTower","firstTower",False)
		print self.firstTower, "% of the time"
		print "\n \n"
		
		print "Teams that get the first inhibitor win"
		self.firstInhib = massDataAnalsis().firstObjectiveTemplate("teams.firstInhibitor","firstInhibitor",False)
		print self.firstInhib, "% of the time"
				
		display().divider(50)
		
		#PLAYER STATS
		print "PLAYER ANALYTICS"
		
		print "A winning player gets an averge of"
		self.csWin = massDataAnalsis().csDiffWin()
		print self.csWin[0], "more creep score per minute"
		print "\n \n"
		
		print "A winning player on average does"
		self.dmgWin = massDataAnalsis().dmgDiffWin()
		print self.dmgWin[0]-self.dmgWin[1], "more damage then a looser"
		print "\n \n"
				
		print "A winning player on average has"
		self.goldWin = massDataAnalsis().goldDiffWin()
		print self.goldWin[0], "more gold then a loosing player"
		
		display().divider(50)
		
		#TEAM STATS
		print "TEAM ANALYTICS"
		
		print "Highest winrate ban:"
		self.bestBans = massDataAnalsis().winningBans()
		print self.bestBans
		print "\n \n"
		
		print "Winning teams place"
		self.winWardPlaced = massDataAnalsis().wardBoughtTrend()
		print self.winWardPlaced[0] - self.winWardPlaced[1], "more wards, or", ((self.winWardPlaced[0]/self.winWardPlaced[1])*100)-100, "% more"
		
		display().divider(50)
		
go = display().displayData()
client.close()
