def offsetToTime(s):
	newS = s[22:-3].split("px -")
	return int(float(newS[0])/36 + 1 + (float(newS[1])/36*10))

def sanitizeData(word):
	return word.replace(',','').replace('.','').replace("'", "")

def getDateFromText(date):
	newDate = ''
	if(date[:3] == 'Jan'):
		newDate += '01/'
	elif(date[:3] == 'Feb'):
		newDate += '02/'
	elif(date[:3] == 'Mar'):
		newDate += '03/'
	elif(date[:3] == 'Apr'):
		newDate += '04/'
	elif(date[:3] == 'May'):
		newDate += '05/'
	elif(date[:3] == 'Jun'):
		newDate += '06/'
	elif(date[:3] == 'Jul'):
		newDate += '07/'
	elif(date[:3] == 'Aug'):
		newDate += '08/'
	elif(date[:3] == 'Sep'):
		newDate += '09/'
	elif(date[:3] == 'Oct'):
		newDate += '10/'
	elif(date[:3] == 'Nov'):
		newDate += '11/'
	elif(date[:3] == 'Dec'):
		newDate += '12/'

	if(len(date) == 10):
		newDate += date[4:5]
	elif(len(date) == 11):
		newDate += date[4:6]

	newDate += ("/" + date[-4:])

	date_substrings = newDate.split('/');

	if(len(date_substrings[1]) == 1):
		date_substrings[1] = '0' + date_substrings[1]

	formattedDate = date_substrings[2] + '-' + date_substrings[0] + '-' + date_substrings[1]

	return formattedDate

def getEnumPosition(position):
	if(position == 'Goalkeeper'):
		return 'GK'
	if(position == 'Defence'):
		return 'D'
	if(position == 'Defence-Left-Back'):
		return 'LB'
	if(position == 'Defence-Centre-Back'):
		return 'CB'
	if(position == 'Defence-Right-Back'):
		return 'RB'
	if(position == 'Midfield'):
		return 'M'
	if(position == 'Midfield-DefensiveMidfield'):
		return 'DM'
	if(position == 'Midfield-CentralMidfield'):
		return 'CM'
	if(position == 'Midfield-LeftMidfield'):
		return 'LM'
	if(position == 'Midfield-RightMidfield'):
		return 'RM'
	if(position == 'Midfield-AttackingMidfield'):
		return 'AM'
	if(position == 'Striker-LeftWing'):
		return 'LW'
	if(position == 'Striker-RightWing'):
		return 'RW'
	if(position == 'Striker-Centre-Forward'):
		return 'CF'
	if(position == 'Striker-SecondaryStriker'):
		return 'SS'
	if(position == 'Striker'):
		return 'ST'

def getValue(number, multiplier):
	number = number.split('\n')[1].split('k')[0].split('m')[0][1:]

	if multiplier == 'k':
		return float(number) * 1000
	if multiplier == 'm':
		return float(number) * 1000000


import requests, bs4, time

time_start = time.time()

print('Time Start: ' + str(time_start))

#################### ONLY THING YOU HAVE TO CHANGE TO CHANGE THE LEAGUE #########################################
url = 'https://www.transfermarkt.com/1-bundesliga/startseite/wettbewerb/ES1/plus/?saison_id=2016'
headers = {"User-Agent":"Mozilla/5.0"}
response = requests.get(url, headers=headers)
soup = bs4.BeautifulSoup(response.text, 'lxml')


##################### ADDING LEAGUE AND TEAMS #########################


league_id = url.split('/')[-3]
league_name = soup.find('h1').getText()
league_country = soup.find('select', {'data-placeholder' : 'Country'}).option.getText();

season_id = url.split('saison_id=')[1]

filename = league_id+'-'+season_id+'.csv'

f = open(filename, "w")

f.write('0,'+league_id+','+league_name+','+league_country+'\n')


######################### ADDING TEAMS #################################
teams = []

league_tables = soup.findAll('div', {'class' : 'tab-print'})

for league_table in league_tables:
	teams += league_table.tbody.findAll('tr')

team_count = 0;


for team in teams:

	team_count += 1

	team_id = team.findAll('td')[1].a['id']
	team_name = team.findAll('td')[1].img['alt']
	team_league = league_id

	team_squad_url = 'https://www.transfermarkt.co.uk' + team.findAll('td')[1].a['href']
	team_points = team.findAll('td')[5].getText()
	team_url_name = team_squad_url.split('/')[3]
	team_pd_url = 'https://www.transfermarkt.co.uk/'+team_url_name+'/leistungsdaten/verein/'+team_id+'/plus/0?reldata='+league_id+'%26'+season_id
	
	#print('Loading ' + team_name + ' (' +str(team_count)+ '/' +str(len(teams))+ '): ' + team_pd_url)

	f.write('1,' + team_id + ',' + team_name + ',' + team_league + ',' + team_points + '\n')

	team_response = requests.get(team_pd_url, headers=headers)
	team_soup = bs4.BeautifulSoup(team_response.text, 'lxml')	


#################### ADDING PLAYERS ####################################

	table = team_soup.find('table', {'class' : 'items'})	

	odd_rows = table.findAll('tr', {'class' : 'odd'})
	even_rows = table.findAll('tr', {'class' : 'even'})	

	players = odd_rows + even_rows

	count = 0;

	for player in players:	

		count += 1	

		player_data = player.findAll('td', {'class' : 'zentriert'});	

		player_id = player.find('a', {'class' : 'spielprofil_tooltip'})["id"]
		player_url = "https://www.transfermarkt.co.uk" + player.find('a', {'class' : 'spielprofil_tooltip'})["href"]
		player_name = player.find('a', {'class' : 'spielprofil_tooltip'}).getText()
		number = player_data[0].getText()
		appearances = player_data[4].getText()
		goals = player_data[5].getText()
		minutes = player.find('td', {'class' : 'rechts'}).getText() 	

		print('Entering (' + team_name + ', ' + player_name + '): Player ' + str(count) + '/' + str(len(players)) + ' on team ' + str(team_count) + '/' + str(len(teams)) + ': ' + str((((team_count-1) / len(teams)) +  (count / len(players) / len(teams))) * 50)[:4] + '%')

		player_response = requests.get(player_url, headers=headers)
		player_soup = bs4.BeautifulSoup(player_response.text, 'lxml')	

		spielerdaten = player_soup.find('div', {'class' : 'spielerdaten'})
		sd = spielerdaten.findAll('tr');	

		birthdate = 'N/A'
		birthplace  = 'N/A'
		birth_country  = 'N/A'
		height = '-1'
		nat1 = 'N/A'
		nat2 = 'N/A'
		position = 'N/A'
		foot = 'N/A'
		team = 'N/A'
		player_value = '-1'

		value_data = player_soup.find('div', {'class' : 'dataMarktwert'})


		if value_data is not None: 
			player_value = str(int(getValue(value_data.getText(), value_data.findAll('span')[1].getText())))

		for row in sd:	

			text = row.th.getText()	

			if text == 'Date of birth:':
				birthdate = row.td.a.getText()	

			elif text == 'Place of birth:':
				birthplace = row.td.span.getText()
				if row.td.span.img is not None:
					birth_country = row.td.span.img['alt']
				birthplace = sanitizeData(birthplace)[:-2]

			elif text == 'Height:':
				height = row.td.getText()
				height = sanitizeData(height)[:-2]

			elif text == 'Nationality:':
				nats = row.td.findAll('img')
				nat1 = nats[0]['alt']
				if len(nats) > 1:
					nat2 = nats[1]['alt']	

			elif text == 'Position:':
				position = row.td.getText()
				position = ''.join(position.split())	

			elif text == 'Foot:':
				foot = row.td.getText	

			elif 'Current club:' in text:
				team = row.td.a['id']	


		player_name = sanitizeData(player_name)
		player_id = sanitizeData(player_id)
		birthdate = sanitizeData(birthdate)
		birth_country = sanitizeData(birth_country)
		nat1 = sanitizeData(nat1)
		nat2 = sanitizeData(nat2)
		position = sanitizeData(position)
		team = sanitizeData(team)
		player_url = sanitizeData(player_url)
		number = sanitizeData(number)
		appearances = sanitizeData(appearances)
		goals = sanitizeData(goals)
		minutes = sanitizeData(minutes)[:-1]
		birthdate = getDateFromText(birthdate)
		position = getEnumPosition(position)	

		if(number == '-'):
			number = '-1'	

		if(appearances == 'Was not used during this season' or appearances == 'Not in squad during this season'):
			appearances = '0'	

		if(goals == '-'):
			goals = '0'	

		if(minutes == ''):
			minutes = '0'	
	

		f.write('2,' + player_id + ',' + player_name + ',' + birthdate + ',' + birthplace + ',' + birth_country + ',' + height + ',' + nat1 + ',' + nat2 + ',' + position + ',' + team + ',' + number + ',' + player_value + '\n')	


##################### ADDING GAMES AND EVENTS #########################
fixtures_url = 'https://www.transfermarkt.co.uk' + soup.find('table', {'class' : 'livescore'}).find('div', {'class' : 'footer-links'}).a['href']

fixtures_response = requests.get(fixtures_url, headers=headers)
fixtures_soup = bs4.BeautifulSoup(fixtures_response.text, 'lxml')

all_tables = fixtures_soup.findAll('table')

# FIRST THREE TABLES ARE USELESS
ftables = all_tables[3:]


#################### FILL IN NUMBER OF TEAMS LATER ##########################
number_of_games = int(len(ftables) * 22 / 2);

game_count = 0;

for ftable in ftables:

	frows = ftable.tbody.findAll('tr', {'class' : None})

	for frow in frows:
		
		game_count += 1

		game_url = 'https://www.transfermarkt.co.uk' + frow.select('td.zentriert.hauptlink')[0].a['href']

		game_response = requests.get(game_url, headers=headers)
	
		game_soup = bs4.BeautifulSoup(game_response.text, 'lxml')


		game_id = game_url.split('https://www.transfermarkt.co.uk/spielbericht/index/spielbericht/')[1]

		game_date = getDateFromText(game_soup.find('div', {'class' : 'sb-spieldaten'}).p.findAll('a')[1].getText().replace(',','')[4:]);

		team_infos = game_soup.findAll('a', {'class' : 'sb-vereinslink'});		
		

		home = team_infos[4]['id'];
		away = team_infos[5]['id'];		

		print('Game '+str(game_id)+' Progress: ' + str(game_count) + '/' + str(number_of_games) + ': ' + str(50 + (50 * game_count/number_of_games))[:4] + '%');

		lazy_p = game_soup.find('p', {'class' : 'sb-zusatzinfos'})		

		location = lazy_p.a.getText();
		attendance = lazy_p.strong.getText()[12:].replace('.','');
		referee = lazy_p.findAll('a')[1].getText()		

		player_containers = game_soup.findAll('div', {'class' : 'aufstellung-spieler-container'})		

		home_lineup = []
		away_lineup = []		

		hmanager = "N/A"
		amanager = "N/A"

		location = sanitizeData(location)
		referee = sanitizeData(referee)

		if game_id == '2718728':
			hmanager = 'Zinédine Zidane'
			amanager = 'Enrique Martín'
			home_lineup.append('27486')
			home_lineup.append('145707')
			home_lineup.append('25557')
			home_lineup.append('14132')
			home_lineup.append('58884')
			home_lineup.append('31909')
			home_lineup.append('27992')
			home_lineup.append('51471')
			home_lineup.append('39381')
			home_lineup.append('8198')
			home_lineup.append('128223')
			away_lineup.append('71206')
			away_lineup.append('99924')
			away_lineup.append('35600')
			away_lineup.append('126252')
			away_lineup.append('298589')
			away_lineup.append('197122')
			away_lineup.append('63040')
			away_lineup.append('174859')
			away_lineup.append('54774')
			away_lineup.append('197126')
			away_lineup.append('61637')
		elif game_id == '2718783':
			hmanager = 'Mauricio Pellegrino'
			amanager = 'Juande Ramos'
			home_lineup.append('172015')
			home_lineup.append('129386')
			home_lineup.append('339808')
			home_lineup.append('67080')
			home_lineup.append('263627')
			home_lineup.append('263856')
			home_lineup.append('76273')
			home_lineup.append('282411')
			home_lineup.append('133794')
			home_lineup.append('243541')
			home_lineup.append('139915')
			away_lineup.append('7914')
			away_lineup.append('45305')
			away_lineup.append('246291')
			away_lineup.append('308371')
			away_lineup.append('285322')
			away_lineup.append('357885')
			away_lineup.append('58874')
			away_lineup.append('28171')
			away_lineup.append('49500')
			away_lineup.append('126625')
			away_lineup.append('199369')
		elif game_id == '2718792':
			hmanager = 'Eusebio'
			amanager = 'Mauricio Pellegrino'
			home_lineup.append('229604')
			home_lineup.append('58074')
			home_lineup.append('142419')
			home_lineup.append('158863')
			home_lineup.append('61812')
			home_lineup.append('59375')
			home_lineup.append('59344')
			home_lineup.append('15693')
			home_lineup.append('35773')
			home_lineup.append('351478')
			home_lineup.append('122155')
			away_lineup.append('172015')
			away_lineup.append('129386')
			away_lineup.append('139434')
			away_lineup.append('67080')
			away_lineup.append('263627')
			away_lineup.append('263856')
			away_lineup.append('282411')
			away_lineup.append('93142')
			away_lineup.append('133794')
			away_lineup.append('243541')
			away_lineup.append('139915')
		elif game_id == '2719070':
			hmanager = 'N/A'
			amanager = 'Diego Simeone'
			home_lineup.append('44062')
			home_lineup.append('351746')
			home_lineup.append('113133')
			home_lineup.append('188838')
			home_lineup.append('135208')
			home_lineup.append('95641')
			home_lineup.append('7663')
			home_lineup.append('127142')
			home_lineup.append('200558')
			home_lineup.append('319745')
			home_lineup.append('25316')
			away_lineup.append('121483')
			away_lineup.append('250845')
			away_lineup.append('107010')
			away_lineup.append('281963')
			away_lineup.append('21725')
			away_lineup.append('148928')
			away_lineup.append('22969')
			away_lineup.append('140776')
			away_lineup.append('74229')
			away_lineup.append('125781')
			away_lineup.append('27389')
		elif game_id == '2719080':
			hmanager = 'Rubi'
			amanager = 'N/A'
			home_lineup.append('27493')
			home_lineup.append('58426')
			home_lineup.append('286779')
			home_lineup.append('45256')
			home_lineup.append('57785')
			home_lineup.append('138935')
			home_lineup.append('89473')
			home_lineup.append('300168')
			home_lineup.append('71394')
			home_lineup.append('246277')
			home_lineup.append('277093')
			away_lineup.append('71801')
			away_lineup.append('351746')
			away_lineup.append('113133')
			away_lineup.append('148004')
			away_lineup.append('135208')
			away_lineup.append('95641')
			away_lineup.append('200558')
			away_lineup.append('7663')
			away_lineup.append('319745')
			away_lineup.append('72779')
			away_lineup.append('25316')
		else:
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

		f.write('3,'+game_id+','+game_date+','+home+','+away+','+location+','+attendance+','+referee+','+hmanager+','+amanager+','+hformation[18:]+','+aformation[18:]+','+home_lineup[0]+','+home_lineup[1]+','+home_lineup[2]+','+home_lineup[3]+','+home_lineup[4]+','+home_lineup[5]+','+home_lineup[6]+','+home_lineup[7]+','+home_lineup[8]+','+home_lineup[9]+','+home_lineup[10]+','+away_lineup[0]+','+away_lineup[1]+','+away_lineup[2]+','+away_lineup[3]+','+away_lineup[4]+','+away_lineup[5]+','+away_lineup[6]+','+away_lineup[7]+','+away_lineup[8]+','+away_lineup[9]+','+away_lineup[10]+'\n')		

		actions = game_soup.findAll('div', {'class' : 'sb-aktion'})		

		for action in actions:		

			action_time = '-1'
			action_type = '-1'
			player1 = '-1'
			player2 = '-1'
			action_team = '-1'		

			action_time = offsetToTime(action.find('div', {'class' : 'sb-aktion-uhr'}).span['style']);		

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

			elif len(spielstand['class']) > 1:
				if spielstand['class'][1] == 'hide-for-small':
					action_type = 'sub'
					player2 = aktion.findAll('a')[0]['id']
					if len(aktion.findAll('a')) > 1:
						player1 = aktion.findAll('a')[2]['id']
					action_team = wappen.a['id']		
			
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

			else:
				print("NOT DEFINED AHHHHHHH")		

			f.write('4,'+game_id+','+str(action_time)+','+action_type+','+player1+','+player2+','+action_team+'\n')



f.close()

time_end = time.time()

print('Elapsed time: ' + str((time_end-time_start)/60.0) + ' minutes....')


