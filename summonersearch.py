#Austin Gheen. April 2017

import requests
from champions import champ_pool


#key for API
key = 'aff44123-649d-4e9b-a431-2a7bbe8141e5'
#print("Key: "+key)
#print(' ')#for spacing

#asks for summoner name from user. take out whitespaces if there are any
inp1 = input('\nEnter summoner name:')
inp1.strip()
print('\nSummoner: ' + inp1 + '\n')
inp1 = inp1.replace(' ', '')

#creates variable, r_summoner, for urllink for api
r_summoner = 'https://na.api.riotgames.com/api/lol/NA/v1.4/summoner/by-name/'+inp1+'?api_key='+key
#print('URL for request: ' + r_summoner + '\n')

#requests summoners account info
print('REQUESTING SUMMONER ID..\n')
req_summoner = requests.get(r_summoner)
#print('RETURN TEXT\n' + req_summoner.text + '\n')

#grabs summoner id from req.text
id = str(req_summoner.json().get(inp1).get('id'))
#print('Summoner Id: ' + id + '\n')

#RANKED RANKING REQUEST
#requests summoners solo/duo leauge
r_league = 'https://na.api.riotgames.com/api/lol/NA/v2.5/league/by-summoner/'+id+'?api_key='+key
req_league = requests.get(r_league)
#print(req_league.text)

############
#RANKED INFO
############

#json object containing 2 dictionaries, which are SOLO/DUO and FLEX league
summoner_league = req_league.json().get(id)

#grabs list of members in league (entries)
solo_league = summoner_league[0]
solo_entries = solo_league.get('entries')

for league in summoner_league:
	if league.get('queue') == 'RANKED_SOLO_5x5':
		#grabs list of members in league (entries)
		solo_league = league
		solo_entries = solo_league.get('entries')
		#searches through list for desired summoner
		#when found, grabs summoners divison, wins, losses
		for solo_member in solo_entries:
			player_id = solo_member.get('playerOrTeamId')
			if player_id == id:
				solo_division = solo_member.get('division')
				solo_tier = solo_league.get('tier')
				solo_points = str(solo_member.get('leaguePoints'))
				solo_wins = solo_member.get('wins')
				solo_losses = solo_member.get('losses')
				solo_total = solo_wins + solo_losses
				solo_win_percentage = round(solo_wins/solo_total, 4) * 100

				print('\nSOLO/DUO:' + solo_tier + ' ' + solo_division + ' ' + solo_points
					+ ' LP\nW/L: ' + str(solo_wins) + '/' + str(solo_losses) 
					+ '\nWIN%: ' + str(solo_win_percentage) + '%\n' )

	if league.get('queue') == 'RANKED_FLEX_SR':
		#grabs list of members in league (entries)
		flex_league = league
		flex_entries = flex_league.get('entries')
		#searches through list for desired summoner
		#when found, grabs summoners divison, wins, loses
		for flex_member in flex_entries:
			player_id = flex_member.get('playerOrTeamId')
			if player_id == id:
				flex_division = flex_member.get('division')
				flex_tier = flex_league.get('tier')
				flex_points = str(flex_member.get('leaguePoints'))
				flex_wins = flex_member.get('wins')
				flex_losses = flex_member.get('losses')
				flex_total = flex_wins + flex_losses
				flex_win_percentage = round(flex_wins/flex_total, 4) * 100

				print('FLEX:' + flex_tier + ' ' + flex_division + ' ' + flex_points
					+ ' LP\nW/L: ' + str(flex_wins) + '/' + str(flex_losses) 
					+ '\nWIN%: ' + str(flex_win_percentage) + '%\n' )
				
#IN-GAME REQUEST
#requests summoner in-game status, 404 if not in game
r_ingame = 'https://na.api.riotgames.com/observer-mode/rest/consumer/getSpectatorGameInfo/NA1/'+id+'?api_key='+key
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
		print('Currently playing Custom\n')
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
		champ_name = str(champ_pool.get(champion_id))
		print('Player ' + str(i) + ': ' + name + 
			'\nChampion: ' + champ_name + '\n')
		
		i+=1

#print('\nEND')
input('Program is finished.\nPress enter to exit')