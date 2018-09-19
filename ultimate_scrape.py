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

	date_substrings = newDate.split('/')

	if(len(date_substrings[1]) == 1):
		date_substrings[1] = '0' + date_substrings[1]

	formattedDate = date_substrings[2] + '-' + date_substrings[0] + '-' + date_substrings[1]

	return formattedDate

def getEnumPosition(position):
	if(position == 'Goalkeeper' or position == 'torwart'):
		return 'GK'
	if(position == 'Defence' or position == 'Defender'):
		return 'D'
	if(position == 'Defence-Left-Back' or position == 'Defender-Left-Back' or position == 'abwehr-Left-Back'):
		return 'LB'
	if(position == 'Defence-Centre-Back' or position == 'Defender-Centre-Back' or position == 'abwehr-Centre-Back'):
		return 'CB'
	if(position == 'Defence-Right-Back' or position == 'Defender-Right-Back'):
		return 'RB'
	if(position == 'Midfield' or position == 'Midfielder' or position == 'abwehr-Right-Back'):
		return 'M'
	if(position == 'Midfield-DefensiveMidfield' or position == 'Midfielder-DefensiveMidfield' or position == 'mittelfeld-DefensiveMidfield'):
		return 'DM'
	if(position == 'Midfield-CentralMidfield' or position == 'Midfielder-CentralMidfield' or position == 'mittelfeld-CentralMidfield'):
		return 'CM'
	if(position == 'Midfield-LeftMidfield' or position == 'Midfielder-LeftMidfield' or position == 'mittelfeld-LeftMidfield'):
		return 'LM'
	if(position == 'Midfield-RightMidfield' or position == 'Midfielder-RightMidfield' or position == 'mittelfeld-RightMidfield'):
		return 'RM'
	if(position == 'Midfield-AttackingMidfield' or position == 'Midfielder-AttackingMidfield' or position == 'mittelfeld-AttackingMidfield'):
		return 'AM'
	if(position == 'Striker-LeftWing' or position == 'Forward-LeftWinger' or position == 'sturm-LeftWinger'):
		return 'LW'
	if(position == 'Striker-RightWing' or position == 'Forward-RightWinger' or position == 'sturm-RightWinger'):
		return 'RW'
	if(position == 'Striker-Centre-Forward' or position == 'Forward-Centre-Forward' or position == 'sturm-Centre-Forward'):
		return 'CF'
	if(position == 'Striker-SecondaryStriker' or position == 'Forward-SecondStriker' or position == 'sturm-SecondStriker'):
		return 'SS'
	if(position == 'Striker' or position == 'Forward'):
		return 'ST'
	else:
		print(position)
		return position

def getValue(number, multiplier):
	number = number.split('\n')[1].split('k')[0].split('m')[0][1:].split(' ')[0]
	multiplier = multiplier.lstrip()

	if multiplier == 'k':
		return float(number) * 1000
	if multiplier == 'm':
		return float(number) * 1000000
	if multiplier[0] == 'T':
		return float(number) * 1000

	print('Broken Value: Number = ' + str(number), ', Mult = ' + multiplier)
	return 'Broken Value: Number = ' + str(number), ', Mult = ' + multiplier


import requests, bs4, time

input_league_url = input("Enter league url with saison included: ")
league_urls = [input_league_url]
if league_urls[0] == 'MLS':
	league_urls[0] = 'https://www.transfermarkt.co.uk/major-league-soccer/startseite/wettbewerb/MLS1/plus/?saison_id=2017'

time_start = time.time()

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

print('Time Start: ' + str(time_start))

#https://www.transfermarkt.co.uk/ligue-1/startseite/wettbewerb/FR1/plus/?saison_id=2017
#https://www.transfermarkt.com/laliga/startseite/wettbewerb/ES1/plus/?saison_id=2017

league_counter = 1

for league_url in league_urls:


##################### BEGIN THE SCRAPE! ##################################
	response = requests.get(league_url, headers=headers)
	time.sleep(2)
	soup = bs4.BeautifulSoup(response.text, 'lxml')


	##################### ADDING LEAGUE AND TEAMS #########################


	league_abbrev = league_url.split('/')[-3]
	league_name = soup.find('h1').getText()
	league_country = soup.find('option', {'selected' : 'selected'}).getText()

	season_id = league_url.split('saison_id=')[1]

	league_id = league_abbrev+'-'+season_id

	filename = league_id+'.csv'

	print(filename)

	f = open(filename, "w")

	f.write('0,'+league_id+','+league_name+','+league_country+'\n')

	########################## ADDING TEAMS ################################
	teams = []

	league_tables = soup.findAll('div', {'class' : 'tab-print'})

	for league_table in league_tables:
		teams += league_table.tbody.findAll('tr')

	team_count = 0


	for team in teams:

		team_count += 1

		team_id = team.findAll('td')[1].a['id']
		team_name = team.findAll('td')[1].img['alt']
		team_league = league_id

		team_squad_url = 'https://www.transfermarkt.co.uk' + team.findAll('td')[1].a['href']
		team_points = team.findAll('td')[5].getText()
		team_url_name = team_squad_url.split('/')[3]
		team_pd_url = 'https://www.transfermarkt.co.uk/'+team_url_name+'/leistungsdaten/verein/'+team_id+'/plus/0?reldata='+league_abbrev+'%26'+season_id
		
		#print('Loading ' + team_name + ' (' +str(team_count)+ '/' +str(len(teams))+ '): ' + team_pd_url)

		f.write('1,' + team_id + ',' + team_name + ',' + team_league + ',' + team_points + '\n')

		team_response = requests.get(team_pd_url, headers=headers)
		time.sleep(.5)
		team_soup = bs4.BeautifulSoup(team_response.text, 'lxml')	


	#################### ADDING PLAYERS ####################################

		table = team_soup.find('table', {'class' : 'items'})

		odd_rows = table.findAll('tr', {'class' : 'odd'})
		even_rows = table.findAll('tr', {'class' : 'even'})	

		players = odd_rows + even_rows

		count = 0

		for player in players:	

			count += 1	

			player_data = player.findAll('td', {'class' : 'zentriert'})

			player_id = player.find('a', {'class' : 'spielprofil_tooltip'})["id"]
			player_url = "https://www.transfermarkt.co.uk" + player.find('a', {'class' : 'spielprofil_tooltip'})["href"]
			player_name = player.find('a', {'class' : 'spielprofil_tooltip'}).getText()
			number = player_data[0].getText()
			appearances = player_data[4].getText()
			goals = player_data[5].getText()
			minutes = player.find('td', {'class' : 'rechts'}).getText() 	

			print('Entering (' + team_name + ', ' + player_name + '): Player ' + str(count) + '/' + str(len(players)) + ' on team ' + str(team_count) + '/' + str(len(teams)) + ': ' + str(((((team_count-1) / len(teams)) +  (count / len(players) / len(teams)))/len(league_urls)) * 50)[:5] + '%')

			player_response = requests.get(player_url, headers=headers)
			time.sleep(.5)
			player_soup = bs4.BeautifulSoup(player_response.text, 'lxml')	

			spielerdaten = player_soup.find('div', {'class' : 'spielerdaten'})
			sd = spielerdaten.findAll('tr')

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

				if text == 'Date of Birth:':
					birthdate = row.td.a.getText()

				elif text == 'Place of Birth:':
					birthplace = row.td.span.getText()
					if row.td.span.img is not None:
						birth_country = row.td.span.img['alt']
					birthplace = sanitizeData(birthplace)[:-2]

				elif text == 'Height:':
					height = row.td.getText()
					height = sanitizeData(height)[:-2]

				elif text == 'Nationality:':
					nats = row.td.findAll('img')
					if len(nats) > 0:
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
	fixtures_url = 'https://www.transfermarkt.co.uk' + soup.find('table', {'class' : 'livescore'}).findAll('div', {'class' : 'footer-links'})[1].a['href']

	fixtures_response = requests.get(fixtures_url, headers=headers)
	time.sleep(.5)
	fixtures_soup = bs4.BeautifulSoup(fixtures_response.text, 'lxml')

	all_tables = fixtures_soup.findAll('table')

	# FIRST THREE TABLES ARE USELESS
	ftables = all_tables[3:]

	number_of_games = int(len(ftables) * len(teams) / 2)

	game_count = 0

	for ftable in ftables:

		frows = ftable.tbody.findAll('tr', {'class' : None})

		frows = [frow for frow in frows if (frow.select('td.zentriert.hauptlink')[0].a.getText() != '-:-') & (frow.select('td.zentriert.hauptlink')[0].a.getText() != 'postponed') & (frow.select('td.zentriert.hauptlink')[0].a.getText() != 'ppd.')]

		for frow in frows:
			
			game_count += 1

			game_url = 'https://www.transfermarkt.co.uk' + frow.select('td.zentriert.hauptlink')[0].a['href']

			# print("Now loading" + game_url)

			game_response = requests.get(game_url, headers=headers)
			time.sleep(.5)
			game_soup = bs4.BeautifulSoup(game_response.text, 'lxml')


			game_id = game_url.split('https://www.transfermarkt.co.uk/spielbericht/index/spielbericht/')[1]

			print('Game '+str(game_id)+' Progress: ' + str(game_count) + '/' + str(number_of_games) + ' of league ' + str(league_counter) + '/' + str(len(league_urls)) + ': ' + str(((50 + 50 * game_count/number_of_games)/len(league_urls)))[:5] + '%')

			game_date = getDateFromText(game_soup.find('div', {'class' : 'sb-spieldaten'}).p.findAll('a')[1].getText().replace(',','')[4:])

			team_infos = game_soup.findAll('a', {'class' : 'sb-vereinslink'})
			
			home = team_infos[4]['id']
			away = team_infos[5]['id']

			lazy_p = game_soup.find('p', {'class' : 'sb-zusatzinfos'})		

			location = lazy_p.a.getText()
			attendance = lazy_p.strong.getText()[12:].replace('.','')

			referee = 'N/A'

			if len(lazy_p.findAll('a')) > 1:
				referee = lazy_p.findAll('a')[1].getText()

			home_container = game_soup.select('div.large-6.columns')[1]
			away_container = game_soup.select('div.large-6.columns')[2]

			home_player_containers = home_container.findAll('div', {'class' : 'aufstellung-spieler-container'})
			away_player_containers = away_container.findAll('div', {'class' : 'aufstellung-spieler-container'})
			
			# In case the game lineups are broken
			#0 means both work, 1 means home doesn't work, 2 means away doesn't work, 3 means both don't work
			lineup_error_code = 0

			filteredHTables = home_container.find_all('table', class_=lambda x: x != 'ersatzbank')
			filteredATables = away_container.find_all('table', class_=lambda x: x != 'ersatzbank')

			if(len(filteredHTables) > 0):
				lineup_error_code = 1
				home_alternate_containers = filteredHTables[0].findAll('a')
			
			if(len(filteredATables) > 0):
				lineup_error_code = lineup_error_code + 2
				away_alternate_containers = filteredATables[0].findAll('a')
			

			home_lineup = []
			away_lineup = []

			hmanager = "N/A"
			amanager = "N/A"

			location = sanitizeData(location)
			referee = sanitizeData(referee)
			
			if game_id == '2990891':
				print('This game has a manual entry. Check and see if the data manager has fixed it so you can clean your code')

				home_lineup.append('76592')
				home_lineup.append('123475')
				home_lineup.append('186201')
				home_lineup.append('52622')
				home_lineup.append('352887')
				home_lineup.append('53027')
				home_lineup.append('135867')
				home_lineup.append('242303')
				home_lineup.append('249776')
				home_lineup.append('129724')
				home_lineup.append('160700')

				away_lineup.append('227671')
				away_lineup.append('244724')
				away_lineup.append('76157')
				away_lineup.append('107136')
				away_lineup.append('87493')
				away_lineup.append('73644')
				away_lineup.append('164749')
				away_lineup.append('55386')
				away_lineup.append('185623')
				away_lineup.append('113217')
				away_lineup.append('172285')

			elif game_id == '2726507':
				print('This game has a manual entry. Check and see if the data manager has fixed it so you can clean your code')

				home_lineup.append('22318')
				home_lineup.append('195810')
				home_lineup.append('44420')
				home_lineup.append('111196')
				home_lineup.append('199733')
				home_lineup.append('61449')
				home_lineup.append('266302')
				home_lineup.append('84545')
				home_lineup.append('47065')
				home_lineup.append('159372')
				home_lineup.append('105521')

				away_lineup.append('7797')
				away_lineup.append('124555')
				away_lineup.append('21782')
				away_lineup.append('205054')
				away_lineup.append('216872')
				away_lineup.append('121402')
				away_lineup.append('131109')
				away_lineup.append('199248')
				away_lineup.append('139634')
				away_lineup.append('162961')
				away_lineup.append('146752')

			elif game_id == '2726663':
				print('This game has a manual entry. Check and see if the data manager has fixed it so you can clean your code')

				home_lineup.append('22318')
				home_lineup.append('195810')
				home_lineup.append('44420')
				home_lineup.append('111196')
				home_lineup.append('26721')
				home_lineup.append('128220')
				home_lineup.append('61449')
				home_lineup.append('266302')
				home_lineup.append('84545')
				home_lineup.append('159372')
				home_lineup.append('105521')

				away_lineup.append('77825')
				away_lineup.append('197470')
				away_lineup.append('111227')
				away_lineup.append('22139')
				away_lineup.append('34198')
				away_lineup.append('118689')
				away_lineup.append('44059')
				away_lineup.append('148252')
				away_lineup.append('85825')
				away_lineup.append('20005')
				away_lineup.append('199258')

			elif game_id == '2826762':
				print('This game has a manual entry. Check and see if the data manager has fixed it so you can clean your code')

				home_lineup.append('227671')
				home_lineup.append('39454')
				home_lineup.append('244724')
				home_lineup.append('76157')
				home_lineup.append('107136')
				home_lineup.append('500994')
				home_lineup.append('19955')
				home_lineup.append('55386')
				home_lineup.append('90147')
				home_lineup.append('160700')
				home_lineup.append('54022')

				away_lineup.append('51048')
				away_lineup.append('74233')
				away_lineup.append('223267')
				away_lineup.append('51078')
				away_lineup.append('221412')
				away_lineup.append('70834')
				away_lineup.append('65243')
				away_lineup.append('160217')
				away_lineup.append('51079')
				away_lineup.append('139430')
				away_lineup.append('145602')

			elif game_id == '2990895':
				print('This game has a manual entry. Check and see if the data manager has fixed it so you can clean your code')

				home_lineup.append('215473')
				home_lineup.append('59100')
				home_lineup.append('71161')
				home_lineup.append('74421')
				home_lineup.append('71468')
				home_lineup.append('120093')
				home_lineup.append('77172')
				home_lineup.append('52618')
				home_lineup.append('549361')
				home_lineup.append('40822')
				home_lineup.append('71433')

				away_lineup.append('55142')
				away_lineup.append('234166')
				away_lineup.append('171043')
				away_lineup.append('209513')
				away_lineup.append('147632')
				away_lineup.append('353583')
				away_lineup.append('37918')
				away_lineup.append('274963')
				away_lineup.append('308477')
				away_lineup.append('366143')
				away_lineup.append('366620')

			elif game_id == '2826764':
				print('This game has a manual entry. Check and see if the data manager has fixed it so you can clean your code')

				home_lineup.append('401311')
				home_lineup.append('264133')
				home_lineup.append('419457')
				home_lineup.append('264126')
				home_lineup.append('75612')
				home_lineup.append('228255')
				home_lineup.append('53046')
				home_lineup.append('162947')
				home_lineup.append('262554')
				home_lineup.append('119245')
				home_lineup.append('54839')

				away_lineup.append('71433')
				away_lineup.append('40822')
				away_lineup.append('54590')
				away_lineup.append('52618')
				away_lineup.append('302643')
				away_lineup.append('295426')
				away_lineup.append('87493')
				away_lineup.append('186201')
				away_lineup.append('71161')
				away_lineup.append('104233')
				away_lineup.append('215473')

			elif game_id == '2826767':
				print('This game has a manual entry. Check and see if the data manager has fixed it so you can clean your code')

				home_lineup.append('50965')
				home_lineup.append('76391')
				home_lineup.append('83330')
				home_lineup.append('51044')
				home_lineup.append('38800')
				home_lineup.append('103402')
				home_lineup.append('26268')
				home_lineup.append('119030')
				home_lineup.append('54845')
				home_lineup.append('52991')
				home_lineup.append('19946')

				away_lineup.append('76908')
				away_lineup.append('52989')
				away_lineup.append('102438')
				away_lineup.append('89294')
				away_lineup.append('76717')
				away_lineup.append('90605')
				away_lineup.append('322115')
				away_lineup.append('64083')
				away_lineup.append('147610')
				away_lineup.append('249789')
				away_lineup.append('69959')

			elif game_id == '2826769':
				print('This game has a manual entry. Check and see if the data manager has fixed it so you can clean your code')

				home_lineup.append('53592')
				home_lineup.append('64134')
				home_lineup.append('469718')
				home_lineup.append('116968')
				home_lineup.append('356044')
				home_lineup.append('73630')
				home_lineup.append('295424')
				home_lineup.append('197170')
				home_lineup.append('149393')
				home_lineup.append('280795')
				home_lineup.append('228867')

				away_lineup.append('55142')
				away_lineup.append('171043')
				away_lineup.append('131066')
				away_lineup.append('28087')
				away_lineup.append('67712')
				away_lineup.append('50945')
				away_lineup.append('124734')
				away_lineup.append('155054')
				away_lineup.append('103790')
				away_lineup.append('113217')
				away_lineup.append('238011')

			# Everything works fine
			elif(lineup_error_code == 0):
				for player in home_player_containers[:11]:
					home_lineup.append(player.span['id'])

				for player in away_player_containers[:11]:
					away_lineup.append(player.span['id'])

				hmanager =  home_container.findAll('a')[-1].getText()
				amanager = away_container.findAll('a')[-1].getText()


			# Home team doesn't work
			elif(lineup_error_code == 1):
				for player in home_alternate_containers[:11]:
					home_lineup.append(player['id'])

				for player in away_player_containers[:11]:
					away_lineup.append(player.span['id'])

				hmanager = home_alternate_containers[11].getText()
				amanager = away_container.findAll('a')[-1].getText()


			# Away team doesn't work
			elif(lineup_error_code == 2):
				for player in home_player_containers[:11]:
					home_lineup.append(player.span['id'])

				for player in away_alternate_containers[:11]:
					away_lineup.append(player['id'])

				hmanager =  home_container.findAll('a')[-1].getText()
				amanager = away_alternate_containers[11].getText()


			#Everything is broken
			elif(lineup_error_code == 3):
				for player in home_alternate_containers[:11]:
					home_lineup.append(player['id'])

				for player in away_alternate_containers[:11]:
					away_lineup.append(player['id'])

				hmanager = home_alternate_containers[11].getText()
				amanager = away_alternate_containers[11].getText()

			# It's a no data situation
			else:
				print('Game ' + game_id + ' is broken. If you haven\'t manually added the lineup in the code, it will not work.')
				
		
			formation_containers = game_soup.findAll('div', {'class' : 'aufstellung-unterueberschrift'})		

			hformation = 'N/A'
			aformation = 'N/A'

			if(len(formation_containers) == 2):
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

				if(action.find('div', {'class' : 'sb-aktion-uhr'}).span is not None):
					action_time = offsetToTime(action.find('div', {'class' : 'sb-aktion-uhr'}).span['style'])
				else:
					action_time = 'MOTM INSTANCE'

				aktion = action.find('div', {'class' : 'sb-aktion-aktion'})
				spielstand = action.find('div', {'class' : 'sb-aktion-spielstand'})
				wappen = action.find('div', {'class' : 'sb-aktion-wappen'})

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

				if(action_time != 'MOTM INSTANCE'):
					f.write('4,'+game_id+','+str(action_time)+','+action_type+','+player1+','+player2+','+action_team+'\n')
	
	f.close()

	league_counter += 1

time_end = time.time()

print('Elapsed time: ' + str((time_end-time_start)/60.0) + ' minutes....')