import requests
import json
import matplotlib.pyplot as plt
from operator import add
import random

API = 'RGAPI-6543e265-bc0a-4259-90e9-b09fb676503b'

champions = {
    266: "Aatrox",
    412: "Thresh",
    23: "Tryndamere",
    79: "Gragas",
    69: "Cassiopeia",
    136: "Aurelion Sol",
    13: "Ryze",
    78: "Poppy",
    14: "Sion",
    1: "Annie",
    202: "Jhin",
    43: "Karma",
    111: "Nautilus",
    240: "Kled",
    99: "Lux",
    103: "Ahri",
    2: "Olaf",
    112: "Viktor",
    34: "Anivia",
    27: "Singed",
    86: "Garen",
    127: "Lissandra",
    57: "Maokai",
    25: "Morgana",
    28: "Evelynn",
    105: "Fizz",
    74: "Heimerdinger",
    238: "Zed",
    68: "Rumble",
    82: "Mordekaiser",
    37: "Sona",
    96: "Kog'Maw",
    55: "Katarina",
    117:  "Lulu",
    22: "Ashe",
    30: "Karthus",
    12: "Alistar",
    122: "Darius",
    67: "Vayne",
    110: "Varus",
    77: "Udyr",
    89: "Leona",
    126: "Jayce",
    134: "Syndra",
    80: "Pantheon",
    92: "Riven",
    121: "Kha'Zix",
    42: "Corki",
    268: "Azir",
    51: "Caitlyn",
    76: "Nidalee",
    85: "Kennen",
    3: "Galio",
    45: "Veigar",
    432: "Bard",
    150: "Gnar",
    90: "Malzahar",
    104: "Graves",
    254: "Vi",
    10: "Kayle",
    39: "Irelia",
    64: "Lee Sin",
    420: "Illaoi",
    60: "Elise",
    106: "Volibear",
    20: "Nunu",
    4: "Twisted Fate",
    24: "Jax",
    102: "Shyvana",
    429: "Kalista",
    36: "Dr. Mundo",
    427: "Ivern",
    131: "Diana",
    223: "Tahm Kench",
    63: "Brand",
    113: "Sejuani",
    8: "Vladimir",
    154: "Zac",
    421: "Rek'Sai",
    133: "Quinn",
    84: "Akali",
    163: "Taliyah",
    18: "Tristana",
    120: "Hecarim",
    15: "Sivir",
    236: "Lucian",
    107: "Rengar",
    19: "Warwick",
    72: "Skarner",
    54: "Malphite",
    157: "Yasuo",
    101: "Xerath",
    17: "Teemo",
    75: "Nasus",
    58: "Renekton",
    119: "Draven",
    35: "Shaco",
    50: "Swain",
    91: "Talon",
    40: "Janna",
    115: "Ziggs",
    245: "Ekko",
    61: "Orianna",
    114: "Fiora",
    9: "Fiddlesticks",
    31: "Cho'Gath",
    33: "Rammus",
    7: "LeBlanc",
    16: "Soraka",
    26: "Zilean",
    56: "Nocturne",
    222: "Jinx",
    83: "Yorick",
    6: "Urgot",
    203: "Kindred",
    21: "Miss Fortune",
    62: "Wukong",
    53: "Blitzcrank",
    98: "Shen",
    201: "Braum",
    5: "Xin Zhao",
    29: "Twitch",
    11: "Master Yi",
    44: "Taric",
    32: "Amumu",
    41: "Gangplank",
    48: "Trundle",
    38: "Kassadin",
    161: "Vel'Koz",
    143: "Zyra",
    267: "Nami",
    59: "Jarvan IV",
    81: "Ezreal",
    164: 'Camille',
    555: 'Pyke',
    145: 'Kaisa',
    518: 'Neeko',
    517: 'Sylas',
    141: 'Kayn',
    516: 'Ornn',
    142: 'Zoe',
    498: 'Xayah',
    497: 'Rakan'
    }

def enoughLength(matchId):
    url = 'https://euw1.api.riotgames.com/lol/match/v4/matches/' + matchId + '?api_key=' + API
    response = requests.get(url).json()
    if response['gameDuration'] >= 1200:
        return 1
    else:
        return 0

def retrieveMatchList(championId):
    matchList = []
    print('----------------')
    with open('euw1pros.txt', 'r') as f:
        for line in f:
            url = 'https://euw1.api.riotgames.com/lol/match/v4/matchlists/by-account/' + line.rstrip("\n\r") + '?champion=' + championId + '&queue=420&season=11&api_key=' + API
            response = requests.get(url).json()

            try:
                i = 0
                while(1):
                    if (enoughLength(str(response['matches'][i]['gameId']))):
                        matchList.append(str(response['matches'][i]['gameId']))
                        break
                    else:
                        i += 1

            except IndexError:
                print('No valid matches in this season')
                ##print(requests.get(url).headers)
            except KeyError:
                print('No valid matches on this account')

            print(len(matchList))
            if len(matchList) >= 1:
                return matchList

def championIdLookUp(championName):
    with open('champion.json', 'r') as f:
        data = json.load(f)
        return data['data'][championName]['key']

def championNameLookUp(championId):
    return champions.get(championId, 'Invalid championId')

def champCurveGenerator(championId, matchId):
    url = 'https://euw1.api.riotgames.com/lol/match/v4/matches/' + matchId + '?api_key=' + API
    response = requests.get(url).json()

    team = 0
    index = 0
    for i in range(0, 10):
        try:
            if response['participants'][i]['championId'] == championId:
                if i < 5:
                    team = 0
                    index = i
                else:
                    team = 1
                    index = i-5
        except:
            print(response)

    damageDealt = []
    totalDamageDealt = 0

    if not team:
        for j in range(0, 5):
            try:
                ##print(j)
                damageDealt.append(response['participants'][j]['stats']['totalDamageDealtToChampions'])
                totalDamageDealt += damageDealt[j]
            except:
                print(response)
    else:
        for j in range(5, 10):
            try:
                ##print(j)
                damageDealt.append(response['participants'][j]['stats']['totalDamageDealtToChampions'])
                totalDamageDealt += damageDealt[j-5]
            except:
                print(response)

    damageTakenDeltas = []

    if team:
        for j in range(0, 5):
            ##print(j)
            try:
                damageTakenDeltas.append((response['participants'][j]['timeline']['damageTakenPerMinDeltas']['0-10'], response['participants'][j]['timeline']['damageTakenPerMinDeltas']['10-20'], response['participants'][j]['timeline']['damageTakenPerMinDeltas']['20-30']))
            except:
                try:
                    damageTakenDeltas.append((response['participants'][j]['timeline']['damageTakenPerMinDeltas']['0-10'], response['participants'][j]['timeline']['damageTakenPerMinDeltas']['10-20'], response['participants'][j]['timeline']['damageTakenPerMinDeltas']['10-20']))
                except:
                    try:
                        damageTakenDeltas.append((response['participants'][j]['timeline']['damageTakenPerMinDeltas']['0-10'], response['participants'][j]['timeline']['damageTakenPerMinDeltas']['0-10'], response['participants'][j]['timeline']['damageTakenPerMinDeltas']['0-10']))
                    except:
                        damageTakenDeltas.append((200, 500, 800))

    else:
        for j in range(5, 10):
            ##print(j)
            try:
                damageTakenDeltas.append((response['participants'][j]['timeline']['damageTakenPerMinDeltas']['0-10'],
                                          response['participants'][j]['timeline']['damageTakenPerMinDeltas']['10-20'],
                                          response['participants'][j]['timeline']['damageTakenPerMinDeltas']['20-30']))
            except:
                try:
                    damageTakenDeltas.append((
                                             response['participants'][j]['timeline']['damageTakenPerMinDeltas']['0-10'],
                                             response['participants'][j]['timeline']['damageTakenPerMinDeltas']['10-20'],
                                             response['participants'][j]['timeline']['damageTakenPerMinDeltas']['10-20']))
                except:
                    try:
                        damageTakenDeltas.append((response['participants'][j]['timeline']['damageTakenPerMinDeltas']['0-10'],
                                                  response['participants'][j]['timeline']['damageTakenPerMinDeltas']['0-10'],
                                                  response['participants'][j]['timeline']['damageTakenPerMinDeltas']['0-10']))
                    except:
                        damageTakenDeltas.append((200, 500, 800))

    aggregatedDamageTakenDeltas = []
    for k in range(0, 3):
        aggregatedDamageTakenDeltas.append(damageTakenDeltas[0][k] + damageTakenDeltas[1][k] + damageTakenDeltas[2][k] +
                                           damageTakenDeltas[3][k] + damageTakenDeltas[4][k])

    return damageDealt[index]/totalDamageDealt * aggregatedDamageTakenDeltas[0], damageDealt[index]/totalDamageDealt * \
           aggregatedDamageTakenDeltas[1], damageDealt[index]/totalDamageDealt * aggregatedDamageTakenDeltas[2]

def participantChampId(matchId):
    url = 'https://euw1.api.riotgames.com/lol/match/v4/matches/' + matchId + '?api_key=' + API
    response = requests.get(url).json()
    team1 = []
    team2 = []
    for i in range(0,5):
        team1.append(str(response['participants'][i]['championId']))
        team2.append(str(response['participants'][i+5]['championId']))
    return team1, team2

def averageChampCurveGenerator(championId, matchList):
    toAverage = []
    number = len(matchList)
    for match in matchList:
        toAverage.append(champCurveGenerator(championId, match))
    average = [0, 0, 0]
    for element in toAverage:
        average = list(map(add, average, element))
    average = list(map(lambda x: x/number, average))
    showCurve(average, championNameLookUp(int(championId)))
    return average

def showCurve(averageDeltas, name):
    x = [0]
    y = [0]
    for i in range(0, 30):
        x.append(i+1)
        y.append(y[i] + averageDeltas[int(i/10)])
    plt.plot(x, y)
    plt.xlabel('x - Minutes')
    plt.ylabel('y - Damage')
    plt.title(name)
    plt.show()

def showMatchCurves(averageDeltas1, averageDeltas2, name1, name2):
    x = [0]
    y1 = [0]
    y2 = [0]
    for i in range(0, 30):
        x.append(i+1)
        y1.append(y1[i] + averageDeltas1[int(i/10)])
        y2.append(y2[i] + averageDeltas2[int(i / 10)])

    plt.plot(x, y1, 'r')
    plt.title(name1)

    plt.plot(x, y2, 'b')
    plt.title(name2)

    plt.xlabel('x - Minutes')
    plt.ylabel('y - Damage')

    plt.show()

def averageTeamCurveGenerator(team):
    curves = []
    for championId in team:
        matchList = loadMatchList(championId)
        curves.append(averageChampCurveGenerator(championId, matchList))
    teamCurve = [0, 0, 0]
    for curve in curves:
        teamCurve = list(map(add, teamCurve, curve))
    print(teamCurve)
    return teamCurve

def matchCurveGenerator(matchId):
    teams = participantChampId(matchId)
    averageDeltas1 = averageTeamCurveGenerator(teams[0])
    averageDeltas2 = averageTeamCurveGenerator(teams[1])

    showMatchCurves(averageDeltas1, averageDeltas2, 'team1', 'team2')

def matchAggregator(championId):
    with open('euw1pros.txt', 'r') as f:
        number = 0
        for line in f:
            print('New line')
            with open(championNameLookUp(championId) + 'GameId.txt', 'a') as g:
                url = 'https://euw1.api.riotgames.com/lol/match/v4/matchlists/by-account/' + line.rstrip(
                "\n\r") + '?champion=' + str(championId) + '&queue=420&season=11&api_key=' + API
                response = requests.get(url).json()
                ##print(response)
                i=0
                n=2
                while n:
                    print(i)
                    try:
                        if enoughLength(str(response['matches'][i]['gameId'])):
                            print(response['matches'][i]['gameId'])
                            g.write(str(response['matches'][i]['gameId'])+'\n')
                            n -= 1
                            number += 1

                    except IndexError:
                        print('No valid matches in this season')
                        ##print(requests.get(url).headers)
                        break
                    except KeyError:
                        print('No valid matches on this account')
                        break

                    i+=1
            if number >= 50:
                return

def loadMatchList(championId):
    matchList = []
    with open(championNameLookUp(championId) + 'GameId.txt', 'r') as f:
        for line in f:
            matchList.append(line.rstrip("\n\r"))
    return matchList

def initChampionsGameId():
    for champion in champions:
        matchAggregator(champion)

initChampionsGameId()


