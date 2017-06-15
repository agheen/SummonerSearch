#Austin Gheen. April 2017. Updated: 6/14/17

import requests
from champions import champ_pool

##########
#FUNCTIONS
##########
def get_id(name):
	#creates variable, r_summoner, for urllink for api
	r_summoner = 'https://na.api.riotgames.com/api/lol/NA/v1.4/summoner/by-name/'+name+'?api_key='+key
	#print('URL for request: ' + r_summoner + '\n')

	#requests summoners account info
	print('REQUESTING SUMMONER ID..\n')
	req_summoner = requests.get(r_summoner)
	#print('RETURN TEXT\n' + req_summoner.text + '\n')

	#grabs summoner id from req.text
	global sum_id
	sum_id = str(req_summoner.json().get(name).get('id'))
	print('Summoner Id: ' + sum_id + '\n')

def get_ranked():
	#RANKED RANKING REQUEST
	#requests summoners solo/duo leauge
	r_rankedposition = 'https://na1.api.riotgames.com/lol/league/v3/positions/by-summoner/'+sum_id+'?api_key='+key

	############
	#RANKED INFO
	############

	#request for ranked positions
	req_position = requests.get(r_rankedposition)

	#dictionary that could be 0 to 3 elements long. each element is a ranking in a league. solo, flex, 3v3
	positions = req_position.json()

	for position in positions:
		queueType = position.get('queueType')
		if queueType == 'RANKED_SOLO_5x5':
			queueType = 'Solo/Duo'
		if queueType == 'RANKED_FLEX_SR':
			queueType = 'Flex'

		tier = position.get('tier')
		rank = position.get('rank')
		leaguePoints = position.get('leaguePoints')
		wins = position.get('wins')
		losses = position.get('losses')
		win_percentage = round(wins/(wins+losses), 4) * 100

		print('\n'+ queueType +': ' + tier + ' ' + rank + ' ' + str(leaguePoints)
						+ ' LP\nW/L: ' + str(wins) + '/' + str(losses) 
						+ '\nWIN%: ' + str(win_percentage) + '%\n' )

def get_ingame():
	#IN-GAME REQUEST
	#requests summoner in-game status, 404 if not in game
	r_ingame = 'https://na1.api.riotgames.com/lol/spectator/v3/active-games/by-summoner/'+sum_id+'?api_key='+key
	print('REQUESTING GAME STATUS..\n')
	req_ingame = requests.get(r_ingame)
	#print('GAME STATUS RETURN TEXT: ' + req_ingame.text + '\n')

	#grabs id number of game. if not in game gameId is 'None'
	gameId = req_ingame.json().get('gameId')
	#print('GAME ID: '+ gameId + '\n')

	if gameId == None:
		print('SUMMONER STATUS: Not In-Game\n')

	else:
		#############
		#IN-GAME INFO
		#############
		print('SUMMONER STATUS: In-Game\n')

		#grabs game queue type. 420 if ranked solo/duo, 440 ranked flex
		game_queue = req_ingame.json().get('gameQueueConfigId')

		if game_queue == None:
			print('Currently playing Custom Game\n')
		if game_queue == 420:
			print('Currently playing Solo/Duo Queue\n')
		if game_queue == 440:
			print('Currently playing Flex Queue\n')
		if game_queue == 65:
			print('Currently playing ARAM\n')
		if game_queue not in [ None, 420, 440, 65 ]:
			print('Currently playing Other Game Type\n')

		#grabs list of players in game
		game_participants = req_ingame.json().get('participants')
		#print('PLAYERS IN GAME: ' + str(game_participants) + '\n')

		#reads through list (game_participants) of 1-10 players/characters in-game
		i = 1
		for players in game_participants:
			name = str(players.get('summonerName'))
			champion_id = players.get('championId')
			champ_name = get_champion(champion_id)
			print('Player ' + str(i) + ': ' + name + 
				'\nChampion: ' + champ_name + '\n')
			
			i+=1

def get_champion(champ_id):
	champ_id = str(champ_id)
	r_champion = 'https://na1.api.riotgames.com/lol/static-data/v3/champions/'+champ_id+'?locale=en_US&dataById=false&api_key='+key
	req_champ = requests.get(r_champion)
	champ = req_champ.json()
	return champ.get('name')

def run_prog():
	#key for API
	
	#print("Key: "+key)
	global key
	key = 'aff44123-649d-4e9b-a431-2a7bbe8141e5'
	#print(' ')#for spacing

	#asks for summoner name from user. take out whitespaces if there are any
	inp1 = input('\nEnter summoner name:')
	print('\nSummoner: ' + inp1 + '\n')
	inp1 = inp1.replace(' ', '').lower()

	get_id( inp1 )

	get_ranked()
					
	get_ingame()

	#print('\nEND')
	input('Program is finished.\nPress enter to exit')

run_prog()