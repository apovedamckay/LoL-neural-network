import json
import requests
from pprint import pprint
import codecs

# api_key = "44a61ade-3abb-4d3d-8c50-3aa2b6325a8d"
# matchId = 1778933437 #1778839570 #1778942120

# url = "https://na.api.pvp.net/api/lol/na/v2.2/match/" + str(matchId) + "?api_key=" + str(api_key) + "&includeTimeline=true"
# response = requests.get(url)
# print(response.status_code)
# if response.status_code != 200:
#     print(response.text)
# else:
#     obj = response.json()
#     with open('match.json', 'wb') as fd:
#         json.dumps(obj, fd, ensure_ascii=False)
#         fd.close()




def getGamestate(obj):
    state = {'team1': '', 'team2': '', 'winner': ''}
    team1 = {'gold': 0, 'xp': 0, 'dragons': 0, 'towers': 0, 'wards': 0, 'barons': 0, 'inhibs': 0, 'red_buffs': 0, 'blue_buffs': 0}
    team2 = {'gold': 0, 'xp': 0, 'dragons': 0, 'towers': 0, 'wards': 0, 'barons': 0, 'inhibs': 0, 'red_buffs': 0, 'blue_buffs': 0}
    if obj['participants'][0]['stats']['winner']:
        state['winner'] = 'team1'
    else:
        state['winner'] = 'team2'
        
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
                            elif event['monsterType'] == 'RED_LIZARD':
                                if event['killerId'] < 6: team1['red_buffs'] += 1
                                else: team2['red_buffs'] += 1
                            elif event['monsterType'] == 'BLUE_GOLEM':
                                if event['killerId'] < 6: team1['blue_buffs'] += 1
                                else: team2['blue_buffs'] += 1
                            # else: pass
                        elif event['eventType'] == 'BUILDING_KILL':
                            if event['buildingType'] == 'INHIBITOR_BUILDING':
                                if event['killerId'] < 6: team1['inhibs'] += 1
                                else: team2['inhibs'] += 1
                            elif event['buildingType'] == 'TOWER_BUILDING':
                                if event['killerId'] < 6: team1['towers'] += 1
                                else: team2['towers'] += 1
                                
        else: # after timestamp 1500000 has passed
            for ID in frame['participantFrames']:
                participant = frame['participantFrames'][ID]
                if int(ID) > 5:
                    team2['gold'] += participant['totalGold']
                    team2['xp'] += participant['xp']
                else:
                    team1['gold'] += participant['totalGold']
                    team1['xp'] += participant['xp']
            break

    # for event in frame['events']:
    # print('TEAM 1:')
    # for i in team1.items():
    #     print('    '+str(i))
    # print()
    # print('TEAM 2:')
    # for i in team2.items():
    #     print('    '+str(i))
        
    state['team1'] = team1
    state['team2'] = team2
    with open('results.json', 'a') as fd:
        json.dump(state, fd)
        fd.close()

with open('matches3.json') as f:
    data = json.load(f)
    for match in data['matches']:
        getGamestate(match)
    f.close()



#DRAGON KILLS Event.eventType = "ELITE_MONSTER_KILL", Event.monsterType = "DRAGON"
#TOWER KILLS Event.eventType = "BUILDING_KILL", Event.buildingType = "TOWER_BUILDING"
#NUMBER OF WARDS Event.eventType = "WARD_PLACED", Event.wardType = ""
#BARON KILLS Event.eventType = "ELITE_MONSTER_KILL", Event.monsterType = "BARON_NASHOR"
#INHIBITOR KILLS Event.eventType = "BUILDING_KILL", Event.buildingType = "INHIBITOR_BUILDING"
#NUMBER OF RED BUFFS Event.eventType = "ELITE_MONSTER_KILL", Event.monsterType = "RED_LIZARD"
#NUMBER OF BLUE BUFFS Event.eventType = "ELITE_MONSTER_KILL", Event.monsterType = "BLUE_GOLEM"
#CHAMPION WINRATE