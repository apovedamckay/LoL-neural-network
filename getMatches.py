import requests
import Queue
import time
# import json

matchFile = open('matchDatabase','w');
gamesRequest = "https://na.api.pvp.net/observer-mode/rest/featured?api_key=9c5a2d19-598d-489f-af61-1f24f4115946"
matchList = [];
playerList = [];
playerQueue = Queue.Queue();
targetVal = 1100;

featuredGames = requests.get(gamesRequest).json();
for game in featuredGames['gameList']:
	for participant in game['participants']:
		playerList.append(participant['summonerName']);
		playerQueue.put(participant['summonerName']);

# playerQueue.put("Adrigreat14");
while playerQueue.empty() != True and len(matchList) <= targetVal:
	currName = playerQueue.get();
	if type(currName) is int:
		currId = str(currName);
	else:
		IDResponse = requests.get("https://na.api.pvp.net/api/lol/na/v1.4/summoner/by-name/"+ currName +"?api_key=9c5a2d19-598d-489f-af61-1f24f4115946");
		time.sleep(1.25);
		parsedName = currName.replace(" ","").lower()
		currId = str(IDResponse.json()[parsedName]['id']);
	historyResponse = requests.get("https://na.api.pvp.net/api/lol/na/v1.3/game/by-summoner/"+currId+"/recent?api_key=9c5a2d19-598d-489f-af61-1f24f4115946");
	time.sleep(1.25);
	currHistory = historyResponse.json();
	for games in currHistory['games']:
		if game['gameMode'] == "CLASSIC" and game['gameType'] == "MATCHED_GAME":
			currGame = str(games['gameId']);
			if currGame in matchList:
				continue;
			matchList.append(currGame + '\n');
			for newPlayer in games['fellowPlayers']:
				if newPlayer['summonerId'] in matchList:
					continue;
				playerQueue.put(newPlayer['summonerId']);
				playerList.append(newPlayer['summonerId']);
			print str(currGame);
for match in matchList:
	matchFile.write(match);
matchFile.close;

print "MATCH IDS RECORDED";
print "RECORDED A TOTAL OF " + str(len(matchList)) + " MATCHES";

