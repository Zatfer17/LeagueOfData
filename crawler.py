import requests
import itertools
import datetime
import json
import os

##TODO regenerate it every 24h
API = 'RGAPI-ee60e5e0-d0ac-4a07-82f3-fd2d15f21c3a'

def retrieveAccountID(region, summonerName):
    url = 'https://' + region + '.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + summonerName + '?api_key=' + API
    response = requests.get(url).json()
    try:
        return response['accountId']
    except:
        print(response)

def retrieveMatchParticipantsID(region, matchId):
    url = 'https://' + region + '.api.riotgames.com/lol/match/v4/matches/' + matchId + '?api_key=' + API
    response = requests.get(url).json()
    participants = []
    for i in range(0, 10):
        try:
            participants.append(response['participantIdentities'][i]['player']['accountId'])
        except:
            print(response)
    return participants

def retrieveMatchesIdGivenAccountId(region, accountId):
    url = 'https://' + region + '.api.riotgames.com/lol/match/v4/matchlists/by-account/' + accountId + '?api_key=' + API
    response = requests.get(url).json()
    matches = []
    for i in range(0, 11):
        try:
            matches.append(response['matches'][i]['gameId'])
        except:
            print(response)
    return matches

def retrieveOtherProsID(region, summonerName):
    matches = retrieveMatchesIdGivenAccountId(region, retrieveAccountID(region, summonerName))
    pros = []
    for match in matches:
        pros += retrieveMatchParticipantsID(region, str(match))
    return pros

def prosCrawler(region, crawlerSeed):
    pros = []
    for seed in crawlerSeed:
        pros.append(retrieveOtherProsID(region, seed))
    return set(itertools.chain.from_iterable(pros))

def initProsAccounts(region, crawlerSeed):
    with open(region + "pros.txt", "r") as f:
        timestamp1 = f.readline()
        t1 = datetime.datetime.strptime(timestamp1, "%Y-%m-%d %H:%M:%S.%f\n")
        t2 = datetime.datetime.now()
        if ((t2-t1).days>1):
            with open(region + "pros.txt", "w+") as f:
                f.write(str(datetime.datetime.utcnow()) + '\n')
                for accountId in prosCrawler(region, crawlerSeed):
                    f.write("%s\n" % accountId)

##TODO make this a txt with only matchId
def getMatchIdGivenAccountIdAndChampId(region, accountId, champId):
    url = 'https://' + region + '.api.riotgames.com/lol/match/v4/matchlists/by-account/' + accountId + '?champion=' + champId + '&queue=420&season=11&api_key=' + API
    response = requests.get(url).json()
    with open(region + champId + '.json', 'r+') as f:
        try:
            for match in response['matches']:
                json.dump(match, f)
                f.write(',\n')
        except:
            print(accountId)
            print(response)

def getMatchIdGivenChampId(region, champId):
    f = open(region + champId + '.json', 'w+')
    with open(region + "pros.txt", "r") as f:
        for line in f:
            getMatchIdGivenAccountIdAndChampId(region, line.rstrip("\n\r"), champId)
    with open(region + champId + '.json', 'r+') as f:
        data = f.read()
        f.seek(0, 0)
        f.write('[' + data)
    with open(region + champId + '.json', "ab") as f:
        f.seek(-3, 2)
        f.truncate()
        f.write(']\n'.encode())


##getMatchIdGivenAccountIdAndChampId('euw1', 'iq4wwia_QS-zFt4xmjcYY_Xa23yKCH3VVPlHOVOse0qVMg', '266')
getMatchIdGivenChampId('euw1', '266')









