import requests
import json
import time 
import datetime

keyAPI = ""
requestsCounter = 0
output = open("cleanScriptSelf_output.csv","w")
output.write("matchID, team, eventType, timestamp, x, y, killer, victim, assistant\n")
'''
summonerName = input("Enter your summoner name: ")
summmonerProfile = requests.get("https://na.api.pvp.net/api/lol/na/v1.4/summoner/by-name/" + str(summonerName) + "?api_key=" + keyAPI).json()
time.sleep(1)
requestsCounter += 1

summonerName = summonerName.replace(" ", "")
print(summonerName)
print(summmonerProfile[str(summonerName)]["id"])
enemyJunglerSummonerId = summmonerProfile[str(summonerName)]["id"]
'''
enemyJunglerSummonerId = input("Enter your summoner id: ")
#grabs summoner name and converts it into his ID so I can grab his matchlist/history
#CHANGED TO GRAB SUMMONER ID DUE TO THE POSSBILITY OF FREQUENT NAME CHANGE

enemyJunglerMatchList = requests.get("https://na.api.pvp.net/api/lol/na/v2.2/matchlist/by-summoner/"+ str(enemyJunglerSummonerId) + "?rankedQueues=RANKED_SOLO_5x5&seasons=SEASON2015&api_key&api_key=" + keyAPI).json()
print("Pausing 1 second for enemyJunglerMatchList...")
time.sleep(1)
requestsCounter += 1 
#grabs the matchlist

enemyJunglerChampion = "unknown"
enemyJunglerChampionId = input("Enter the champion that you're interested in: ")
championList = requests.get("https://global.api.pvp.net/api/lol/static-data/na/v1.2/champion?api_key=" + keyAPI).json()
print("Pausing 1 second for championList...")
time.sleep(1)
requestsCounter += 1 
#prompts the targeted champion 

for champion in championList["data"]:
	if str(championList["data"][champion]["id"]) == enemyJunglerChampionId:
		enemyJunglerChampionId = championList["data"][champion]["id"]
		print("Found champion: " + champion)
	
#searches for that champion's name	

'''
eachMatchChampionId = -1
eachMatchIdList = []
eachMatchChampionIdList = []

for eachMatch in matchList["matches"]:	
#	eachMatchId = eachMatch["matchId"]
	eachMatchIdList.append(eachMatch["matchId"])
#	eachMatchChampionId = eachMatch["champion"] 
	eachMatchChampionIdList.append(eachMatch["champion"])
#	if (eachMatchChampionId == -1):
#		print("Some error happened and there is no champion found")
###### lol, the script worked on accident because matchID is replaced everytime and the champion is also replaced.  It will just display the last replacement 	
eachMatchChampionId = eachMatchChampionIdList[4]
print("eachMatchChampionId is: " + str(eachMatchChampionIdList[4]))
#intention: store the matches in a list and look at the selected one
'''
'''
for i in range(0,matchList["totalGames"]): 
	eachMatchId = matchList["matches"][4]["matchId"]
	eachMatchChampionId = matchList["matches"][4]["champion"]
	if (eachMatchChampionId == -1):
		print("Some error happened and there is no champion found")
print("eachMatchChampionId is: " + str(eachMatchChampionId))
print("Selected eachMatchId is: " + str(eachMatchId))

matchData = requests.get("https://na.api.pvp.net/api/lol/na/v2.2/match/" + str(eachMatchId) + "?includeTimeline=true&api_key=" + keyAPI).json()
print("Pausing 1 second for matchData from match: " + str(eachMatchId))
time.sleep(1)
requestsCounter += 1
'''
'''
matchChampionId = -1
championTeamId = -1
for matchChampionId in matchData["participants"]:
	if eachMatchChampionId == matchChampionId["championId"]:
		championTeamId = matchChampionId["teamId"]
		print(championTeamId)
		print(eachMatchChampionId)
#using the championId, find out the team of the summoner, 
		
enemyTeamId = 100 if (championTeamId == 200) else 200
#and reverse it
'''
'''
enemyJunglerChampionId = -1
enemyJunglerParticipantId = -1
enemyJunglerSummonerId = -1

for eachParticipant in matchData["participants"]:
	if eachParticipant["teamId"] == enemyTeamId:
		if eachParticipant["timeline"]["lane"] == "JUNGLE":
			enemyJunglerChampionId = eachParticipant["championId"] 
			print("Enemy jungler champion ID: " + str(enemyJunglerChampionId))
			enemyJunglerParticipantId = eachParticipant["participantId"] 
			print("Enemy jungler enemyJunglerParticipantId: " + str(enemyJunglerParticipantId))
#after reversing it, find out the enemy champion and enemy participantId
			
enemyJunglerSummonerId = matchData["participantIdentities"][enemyJunglerParticipantId - 1]["player"]["summonerId"] 
#so i can find his summonerId

print("enemyJunglerSummonerId: " + str(enemyJunglerSummonerId))
enemyJunglerMatchList = requests.get("https://na.api.pvp.net/api/lol/na/v2.2/matchlist/by-summoner/"+ str(enemyJunglerSummonerId) + "?rankedQueues=RANKED_SOLO_5x5&easons=SEASON2015&api_key&api_key=" + keyAPI).json()
#using his summonerId, search through his matchlist/history

print("Pausing 1 second for enemyJunglerMatchList...")
time.sleep(1)
requestsCounter += 1
'''


enemyCorrespondingMatchID = []
for eachEnemyJunglerMatch in enemyJunglerMatchList["matches"]:
	if eachEnemyJunglerMatch["matchId"] not in enemyCorrespondingMatchID and eachEnemyJunglerMatch["champion"] == enemyJunglerChampionId and eachEnemyJunglerMatch["lane"] == "JUNGLE": 
		enemyCorrespondingMatchID.append(eachEnemyJunglerMatch["matchId"])
#for matches that meets the requirements of unique, matching targeted champion id, and the lane is indeed jungle

enemyCorrespondingMatchIdOutputList = []
eventTypeList = []
playerSide = []
timestampList = [] 
killerIdList = []
victimIdList = [] 
assistantIdList = []
positionX = []
positionY = []
#hit the statistics
try:
	for i in range(0,len(enemyCorrespondingMatchID)):
		if requestsCounter == 99:
			break
		try:
			enemyMatchData = requests.get("https://na.api.pvp.net/api/lol/na/v2.2/match/" + str(enemyCorrespondingMatchID[i]) + "?includeTimeline=true&api_key=" + keyAPI).json()
			print("Current count: " + str(requestsCounter) + " , Pausing 1 second for enemyMatchData... ")
			time.sleep(1)
			requestsCounter += 1

			for eachEnemyMatchDataParticipant in enemyMatchData["participantIdentities"]:
				if enemyJunglerSummonerId == str(eachEnemyMatchDataParticipant["player"]["summonerId"]):
					print(enemyJunglerSummonerId)
					enemyMatchDataParticipantId = eachEnemyMatchDataParticipant["participantId"]
					print("enemyMatchDataParticipantId: " + str(enemyMatchDataParticipantId))
				
			enemyMatchDataFrames = enemyMatchData["timeline"]["frames"]
			frameNumber = 0
			for eachFrame in enemyMatchDataFrames:
				if "position" in eachFrame["participantFrames"][str(enemyMatchDataParticipantId)]:
					enemyParticipantFramePosition = eachFrame["participantFrames"][str(enemyMatchDataParticipantId)]["position"]
					enemyCorrespondingMatchIdOutputList.append(enemyCorrespondingMatchID[i])
					eventTypeList.append("frame" + str(frameNumber))
					timestampList.append(60000 * frameNumber)
					killerIdList.append("eachFrame data")
					victimIdList.append("eachFrame data")
					assistantIdList.append("eachFrame data")
					positionX.append(enemyParticipantFramePosition["x"])
					positionY.append(enemyParticipantFramePosition["y"])	
					if enemyMatchDataParticipantId in range(1, 6):
						playerSide.append("Blue")
					else: 
						playerSide.append("Red")
					frameNumber += 1
				if "events" in eachFrame:
					eventsList = eachFrame["events"]
					for eachEvent in eventsList:
						if "assistingParticipantIds" in eachEvent: 
							if enemyMatchDataParticipantId in eachEvent["assistingParticipantIds"]:
								enemyCorrespondingMatchIdOutputList.append(enemyCorrespondingMatchID[i])
								eventTypeList.append(eachEvent["eventType"])
								timestampList.append(eachEvent["timestamp"])
								killerIdList.append(eachEvent["killerId"])
								if "victimId" in eachEvent:
									victimIdList.append(eachEvent["victimId"])
								else:
									victimIdList.append("No victimId found")
								assistantIdList.append(eachEvent["assistingParticipantIds"])
								positionX.append(eachEvent["position"]["x"])
								positionY.append(eachEvent["position"]["y"])
								if enemyMatchDataParticipantId in range(1, 6):
									playerSide.append("Blue")
								else: 
									playerSide.append("Red")
						if "position" in eachEvent: 
							if "victimId" in eachEvent or "killerId" in eachEvent:
								if enemyMatchDataParticipantId == eachEvent["killerId"] or ("victimId" in eachEvent and enemyMatchDataParticipantId == eachEvent["victimId"]): ##### for comparison, you have to do specifically eachEvent["killerId"]
									enemyCorrespondingMatchIdOutputList.append(enemyCorrespondingMatchID[i])
									eventTypeList.append(eachEvent["eventType"])
									timestampList.append(eachEvent["timestamp"])
									killerIdList.append(eachEvent["killerId"])
									if "victimId" in eachEvent:
										victimIdList.append(eachEvent["victimId"]) 
									else:
										victimIdList.append("No victimId found")
									assistantIdList.append("he cannot be assisting as he is killer or victim")
									positionX.append(eachEvent["position"]["x"])
									positionY.append(eachEvent["position"]["y"])
									if enemyMatchDataParticipantId in range(1, 6):
										playerSide.append("Blue")
									else: 
										playerSide.append("Red")
						elif ("ITEM_PURCHASED" in eachEvent.values()) and (enemyMatchDataParticipantId == eachEvent["participantId"]): 
							enemyCorrespondingMatchIdOutputList.append(enemyCorrespondingMatchID[i])
							eventTypeList.append(eachEvent["eventType"])
							timestampList.append(eachEvent["timestamp"])
							killerIdList.append("Item purchased")
							victimIdList.append("Item purchased")
							assistantIdList.append("Item purchased")
							if enemyMatchDataParticipantId in range(1, 6):
								positionX.append(str(581))
								positionY.append(str(561))
								playerSide.append("Blue")
							else:
								positionX.append(str(15000-581))
								positionY.append(str(15000-561))
								playerSide.append("Red")
		except Exception as e: 
			print(type(e).__name__ + " " + str(e.args))
			print("probably a jsondecodeerror")
except KeyboardInterrupt:
	print("Caught interrupt")
print("Will this print?")

for i in range (0,len(eventTypeList)):
	output.write(str(enemyCorrespondingMatchIdOutputList[i]) + ","
	+ playerSide[i] + ","
	+ eventTypeList[i] + "," 
	+ str(timestampList[i]) + ","
	+ str(positionX[i]) + ","
	+ str(positionY[i]) + ","
	+ str(killerIdList[i]) + "," 
	+ str(victimIdList[i]) + "," 
	+ str(assistantIdList[i]))
	output.write("\n")	