import crawler as c

##TODO retrieve these from a file
crawlerSeedEU = {'Rekkles', 'TheShackledOne', 'VIT Jiizuké'}
crawlerSeedNA = {'C9 Sneaky', 'TSM Bjergsen', 'Doublelift'}
crawlerSeedKR = {'KZ Deft0', 'Hide on bush'}

##TODO regenerate it every 24h
API = 'RGAPI-ee60e5e0-d0ac-4a07-82f3-fd2d15f21c3a'

c.initProsAccounts('euw1', crawlerSeedEU)
c.initProsAccounts('na1', crawlerSeedNA)
c.initProsAccounts('kr', crawlerSeedKR)