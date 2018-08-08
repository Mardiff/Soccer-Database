import requests, bs4

def sanitizeData(word):
	return word.replace(',','').replace('.','').replace('á','a').replace('é','e').replace('í','i').replace('ó','o').replace('ú','u').replace('ñ','n').replace('Á','A')

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

	return newDate

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

url = 'https://www.transfermarkt.com/eredivisie/startseite/wettbewerb/NL1'
headers = {"User-Agent":"Mozilla/5.0"}
response = requests.get(url, headers=headers)
soup = bs4.BeautifulSoup(response.text, 'lxml')

team_table = soup.find('table', {'class' : 'items'})

teams_odd = team_table.tbody.findAll('tr', {'class' : 'odd'})
teams_even = team_table.tbody.findAll('tr', {'class' : 'even'})

teams = teams_odd + teams_even

# print(len(teams))

filename = "eredivisie.csv"

f = open(filename, "w")

csv_headers = "name, player_id, birthdate, birthplace, birth_country, height, nationality1, nationality2, position, team, player_url, number, appearances, goals, minutes\n"

f.write(csv_headers)

team_count = 0;

for team in teams:

	team_count += 1

	team_data = team.findAll('td')

	team_id = team_data[1].a['id'];
	team_name = team_data[1].a.getText()
	team_url = 'https://www.transfermarkt.co.uk' + team_data[1].a['href']
	team_pd_url = 'https://www.transfermarkt.co.uk/atlanta-united-fc/leistungsdaten/verein/' + str(team_id) + '/plus/0?reldata=NL1%262017'

	response = requests.get(team_pd_url, headers=headers)
	soup = bs4.BeautifulSoup(response.text, 'lxml')	

	table = soup.find('table', {'class' : 'items'})	

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

		print('Entering (' + team_name + ', ' + player_name + '): Player ' + str(count) + '/' + str(len(players)) + ' on team ' + str(team_count) + '/' + str(len(teams)) + ': ' + str((((team_count-1) / len(teams)) +  (count / len(players) / len(teams))) * 100)[:4] + '%')

		# print("Entering ("+ team_name +") player " + str(count) + "/" + str(len(players)) + ": " + str(count/len(players) * 100)[:4] + "%")	

		player_response = requests.get(player_url, headers=headers)
		player_soup = bs4.BeautifulSoup(player_response.text, 'lxml')	

		spielerdaten = player_soup.find('div', {'class' : 'spielerdaten'})
		sd = spielerdaten.findAll('tr');	

		birthdate = 'N/A'
		birthplace  = 'N/A'
		birth_country  = 'N/A'
		height = 'N/A'
		nat1 = 'N/A'
		nat2 = 'N/A'
		position = 'N/A'
		foot = 'N/A'
		team = 'N/A'
		
		for row in sd:	

			text = row.th.getText()	

			# print(text)	

			if text == 'Date of birth:':
				birthdate = row.td.a.getText()	

			elif text == 'Place of birth:':
				birthplace = row.td.span.getText()
				birth_country = row.td.span.img['alt']	

			elif text == 'Height:':
				height = row.td.getText()	

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

		# print()
		# print('name: ' + name)
		# print("player_id: " + player_id)
		# print("birthdate: " + birthdate)
		# print("birthplace: " + birthplace)
		# print("birth_country: " + birth_country)
		# print("height: " + height)
		# print("nat1: " + nat1)
		# print("nat2: " + nat2)
		# print("position: " + position)
		# print("team: " + team)
		# print("player_url: " + player_url)
		# print("number: " + number)
		# print('appearances: ' + appearances)
		# print('goals: ' + goals)
		# print('minutes: ' + minutes)	

		player_name = sanitizeData(player_name)
		player_id = sanitizeData(player_id)
		birthdate = sanitizeData(birthdate)
		birthplace = sanitizeData(birthplace)[:-2]
		birth_country = sanitizeData(birth_country)
		height = sanitizeData(height)[:-2]
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
	

		f.write(player_name + ',' + player_id + ',' + birthdate + ',' + birthplace + ',' + birth_country + ',' + height + ',' + nat1 + ',' + nat2 + ',' + position + ',' + team + ',' + player_url + ',' + number + ',' + appearances + ',' + goals + ',' + minutes + '\n')	

f.close()	
