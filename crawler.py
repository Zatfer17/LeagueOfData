import requests
import itertools

##TODO regenerate it every 24h
API = 'RGAPI-ce8dfdc1-f814-4789-847c-91987973119a'

##TODO retrieve these from a file
crawlerSeedEU = {'Rekkles', 'TheShackledOne', 'VIT Jiizuké'}
crawlerSeedNA = {'C9 Sneaky', 'TSM Bjergsen', 'Doublelift'}
crawlerSeedKR = {'KZ Deft0', 'Hide on bush'}

def retrieveAccountID(summonerName):
    url = 'https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + summonerName + '?api_key=' + API
    response = requests.get(url).json()
    try:
        return response['accountId']
    except:
        print('Rate limit exceeded')

def retrieveMatchParticipantsID(matchId):
    url = 'https://euw1.api.riotgames.com/lol/match/v4/matches/' + matchId + '?api_key=' + API
    response = requests.get(url).json()
    participants = []
    for i in range(0, 10):
        try:
            participants.append(response['participantIdentities'][i]['player']['accountId'])
        except:
            print('Rate limit exceeded')
    return participants

def retrieveMatchesIdGivenAccountId(accountId):
    url = 'https://euw1.api.riotgames.com/lol/match/v4/matchlists/by-account/' + accountId + '?api_key=' + API
    response = requests.get(url).json()
    matches = []
    for i in range(0, 11):
        try:
            matches.append(response['matches'][i]['gameId'])
        except:
            print('Rate limit exceeded')
    return matches

def retrieveOtherProsID(summonerName):
    matches = retrieveMatchesIdGivenAccountId(retrieveAccountID(summonerName))
    pros = []
    for match in matches:
        pros.append(retrieveMatchParticipantsID(str(match)))
    return pros

def prosCrawler(crawlerSeed):
    pros = []
    for seed in crawlerSeed:
        pros += retrieveOtherProsID(seed)
    return set(itertools.chain.from_iterable(pros))









