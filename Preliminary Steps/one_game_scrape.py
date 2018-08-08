import requests, bs4

def offsetToTime(s):
	newS = s[22:-3].split("px -")
	return int(float(newS[0])/36 + 1 + (float(newS[1])/36*10))

url = 'https://www.transfermarkt.com/spielbericht/index/spielbericht/2824674'
headers = {"User-Agent":"Mozilla/5.0"}
response = requests.get(url, headers=headers)
game_soup = bs4.BeautifulSoup(response.text, 'lxml')

filename = "game.csv"

f = open(filename, "w")

game_id = game_soup.find('a', {'class' : 'ergebnis-link'})['id']
game_date = game_soup.find('div', {'class' : 'sb-spieldaten'}).p.findAll('a')[1].getText();

team_infos = game_soup.findAll('a', {'class' : 'sb-vereinslink'});


home = team_infos[4]['id'];
away = team_infos[5]['id'];

lazy_p = game_soup.find('p', {'class' : 'sb-zusatzinfos'})

location = lazy_p.a.getText();
attendance = lazy_p.strong.getText();
referee = lazy_p.findAll('a')[1].getText()

player_containers = game_soup.findAll('div', {'class' : 'aufstellung-spieler-container'})

home_lineup = []
away_lineup = []

for player in player_containers[:11]:
	home_lineup.append(player.span['id'])

for player in player_containers[11:22]:
	away_lineup.append(player.span['id'])


sub_containers = game_soup.findAll('table', {'class' : 'ersatzbank'})


hmanager =  sub_containers[0].findAll('tr')[-1].a.getText()
amanager = sub_containers[1].findAll('tr')[-1].a.getText()


formation_containers = game_soup.findAll('div', {'class' : 'aufstellung-unterueberschrift'})

hformation = formation_containers[0].getText().replace('\r','').replace('\t','').replace('\n','')
aformation = formation_containers[1].getText().replace('\r','').replace('\t','').replace('\n','')

f.write('3'+','+game_id+','+game_date+','+home+','+away+','+location+','+attendance+','+referee+','+hmanager+','+amanager+','+home_lineup[0]+','+home_lineup[1]+','+home_lineup[2]+','+home_lineup[3]+','+home_lineup[4]+','+home_lineup[5]+','+home_lineup[6]+','+home_lineup[7]+','+home_lineup[8]+','+home_lineup[9]+','+home_lineup[10]+','+away_lineup[0]+','+away_lineup[1]+','+away_lineup[2]+','+away_lineup[3]+','+away_lineup[4]+','+away_lineup[5]+','+away_lineup[6]+','+away_lineup[7]+','+away_lineup[8]+','+away_lineup[9]+','+away_lineup[10]+'\n')

actions = game_soup.findAll('div', {'class' : 'sb-aktion'})

for action in actions:

	time = '-1'
	action_type = '-1'
	player1 = '-1'
	player2 = '-1'
	action_team = '-1'

	time = offsetToTime(action.find('div', {'class' : 'sb-aktion-uhr'}).span['style']);

	aktion = action.find('div', {'class' : 'sb-aktion-aktion'});
	spielstand = action.find('div', {'class' : 'sb-aktion-spielstand'});
	wappen = action.find('div', {'class' : 'sb-aktion-wappen'});

	# Check if goal
	if spielstand.b:
		if 'Own' in aktion.getText():
			action_type = 'own goal'
		else:
			action_type = 'goal'

		player1 = aktion.findAll('a')[0]['id']

		if len(aktion.findAll('a')) > 1:
			player2 = aktion.findAll('a')[1]['id']

		action_team = wappen.a['id']

	elif spielstand.a:
		action_type = 'pk save'
		player1 = aktion.findAll('a')[2]['id']
		player2 = aktion.findAll('a')[0]['id']
		action_team = spielstand.a['id']

	elif spielstand.span['class'][1] == 'sb-gelb':
		action_type = 'yellow'
		player1 = aktion.findAll('a')[0]['id']
		action_team = wappen.a['id']

	elif spielstand.span['class'][1] == 'sb-rot':
		action_type = 'red'
		player1 = aktion.findAll('a')[0]['id']
		action_team = wappen.a['id']

	elif spielstand.span['class'][1] == 'sb-gelbrot':
		action_type = 'yellowred'
		player1 = aktion.findAll('a')[0]['id']
		action_team = wappen.a['id']

	elif 'sb-wechsel' in spielstand.span['class'][1]:
		action_type = 'sub'
		player1 = aktion.findAll('a')[2]['id']
		player2 = aktion.findAll('a')[0]['id']
		action_team = wappen.a['id']

	else:
		print("NOT DEFINED AHHHHHHH")

	f.write('4'+','+str(time)+','+action_type+','+player1+','+player2+','+action_team+'\n')
