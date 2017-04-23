import requests, pickle

champ_pool = { }

r = 'http://ddragon.leagueoflegends.com/cdn/6.24.1/data/en_US/champion.json'

req = requests.get(r)
text = req.text
#print('RETURN TEXT\n' + text + '\n')
total_champs = 1

champs = req.json().get('data')
#print(champs)


for champ in champs:
	champ_info = req.json().get('data').get(champ)
	#print(champ_info)
	key = champ_info.get('key')
	#print(champ +':'+ key)
	#print('Champion id:'+ str(id))
	champ_pool.update({int(key) : champ})

	total_champs+=1
	
print('Total Number of Champions: ' + str(total_champs))
#print(champ_pool)

outFile = open('champions.py' , 'w' )
outFile.write('champ_pool = ' + str(champ_pool))
outFile.close()

input('Program is finished.\nPress enter to exit')