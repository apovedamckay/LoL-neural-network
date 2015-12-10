import json
import requests
from pprint import pprint
import codecs
import time

# api_key = "44a61ade-3abb-4d3d-8c50-3aa2b6325a8d"


def getGamestateById(ID):
    api_key = "44a61ade-3abb-4d3d-8c50-3aa2b6325a8d"
    url = "https://na.api.pvp.net/api/lol/na/v2.2/match/" + str(ID) + "?api_key=" + str(api_key) + "&includeTimeline=true"
    response = requests.get(url)
    print(url)
    if response.status_code == 200:
        getGamestate(response.json())
    else:
        print('ID ' + str(ID) + ': rate limited, retrying...')
        print(response.headers)
        getGamestateById(ID)
    print()
    time.sleep(1.7)


def getGamestate(obj):
    state = []
    team1 = {'gold': 0, 'xp': 0, 'dragons': 0, 'towers': 0, 'wards': 0, 'barons': 0, 'inhibs': 0}
    team2 = {'gold': 0, 'xp': 0, 'dragons': 0, 'towers': 0, 'wards': 0, 'barons': 0, 'inhibs': 0}
        
    for frame in obj["timeline"]["frames"]:
        
        if frame['timestamp'] < 1500000:
            for (key, values) in frame.items():
                if key == "events":
                    for event in values:
                        if event['eventType'] == 'WARD_PLACED':
                            if event['creatorId'] < 6:
                                team1['wards'] += 1
                            else:
                                team2['wards'] += 1
                        elif event['eventType'] == 'ELITE_MONSTER_KILL':
                            if event['monsterType'] == 'DRAGON':
                                if event['killerId'] < 6: team1['dragons'] += 1
                                else: team2['dragons'] += 1
                            elif event['monsterType'] == 'BARON_NASHOR':
                                if event['killerId'] < 6: team1['barons'] += 1
                                else: team2['barons'] += 1
                            # elif event['monsterType'] == 'RED_LIZARD':
                            #     print('red buff')
                            #     if event['killerId'] < 6: team1['red_buffs'] += 1
                            #     else: team2['red_buffs'] += 1
                            # elif event['monsterType'] == 'BLUE_GOLEM':
                            #     print('blue buff')
                            #     if event['killerId'] < 6: team1['blue_buffs'] += 1
                            #     else: team2['blue_buffs'] += 1
                            
                        elif event['eventType'] == 'BUILDING_KILL':
                            if event['buildingType'] == 'INHIBITOR_BUILDING':
                                if event['killerId'] < 6: team1['inhibs'] += 1
                                else: team2['inhibs'] += 1
                            elif event['buildingType'] == 'TOWER_BUILDING':
                                if event['killerId'] < 6: team1['towers'] += 1
                                else: team2['towers'] += 1

            team1['gold'] = 0
            team2['gold'] = 0
            team1['xp'] = 0
            team2['xp'] = 0
            for ID in frame['participantFrames']:
                participant = frame['participantFrames'][ID]
                if int(ID) > 5:
                    team2['gold'] += participant['totalGold']
                    team2['xp'] += participant['xp']
                else:
                    team1['gold'] += participant['totalGold']
                    team1['xp'] += participant['xp'] 

        else: # after timestamp 1500000 has passed
            break

    # for event in frame['events']:
    # print('TEAM 1:')
    # for i in team1.items():
    #     print('    '+str(i))
    # print()
    # print('TEAM 2:')
    # for i in team2.items():
    #     print('    '+str(i))
        
    def comparison(x):
        if team1[x] == 0 and team2[x] == 0:
            state.append(0)
        elif team1[x] == 0:
            state.append(team2[x]*-1)
        elif team2[x] == 0:
            state.append(team1[x])
        else:
            if team1[x] > team2[x]: state.append(float(team1[x])/team2[x])
            else: state.append(float(team2[x])/team1[x]*-1)
            
    comparison('gold')
    comparison('xp')
    comparison('dragons')
    comparison('towers')
    comparison('wards')
    comparison('barons')
    comparison('inhibs')
    # comparison('red_buffs')
    # comparison('blue_buffs')


    if obj['participants'][0]['stats']['winner']:
        winner = 1
    else:
        winner = -1

    state.append(winner)
    result = ""
    for i in state:
        result += (str(i) + ', ')
    

    with open('game2.csv', 'a') as fd:
        fd.write(result + '\n')
        fd.close()

with open('matchDatabaseBackup') as f:
    # i = 100
    for matchId in f:
        # if i <= 0:
        #     break
        getGamestateById(matchId[0:10])
        # i = i-1
    f.close()



#DRAGON KILLS Event.eventType = "ELITE_MONSTER_KILL", Event.monsterType = "DRAGON"
#TOWER KILLS Event.eventType = "BUILDING_KILL", Event.buildingType = "TOWER_BUILDING"
#NUMBER OF WARDS Event.eventType = "WARD_PLACED", Event.wardType = ""
#BARON KILLS Event.eventType = "ELITE_MONSTER_KILL", Event.monsterType = "BARON_NASHOR"
#INHIBITOR KILLS Event.eventType = "BUILDING_KILL", Event.buildingType = "INHIBITOR_BUILDING"
#NUMBER OF RED BUFFS Event.eventType = "ELITE_MONSTER_KILL", Event.monsterType = "RED_LIZARD"
#NUMBER OF BLUE BUFFS Event.eventType = "ELITE_MONSTER_KILL", Event.monsterType = "BLUE_GOLEM"
#CHAMPION WINRATE