def offsetToTime(s):
	newS = s[22:-3].split("px -")
	return int(float(newS[0])/36 + 1 + (float(newS[1])/36*10))

def sanitizeData(word):
	return word.replace(',','').replace('.','').replace("'", "").replace('\t','').replace('\n','')


import requests, bs4, time

time_start = time.time()

headers = {"User-Agent":"Mozilla/5.0"}

print('Time Start: ' + str(time_start))

ussda_url = 'http://www.ussoccerda.com/sam/standings/league/'

response = requests.get(ussda_url, headers = headers)

soup = bs4.BeautifulSoup(response.text, 'lxml')

standings_table = soup.find('div', {'class' : 'standings-league-events'})

year = sanitizeData(standings_table.find('h1').text.replace('Current Season ',''))

f = open('USSDA Player Stats ' + year + '.csv', "w")
f.write('Name,Team,Division,Birth Year,Goals,Starts,Appearances,Total Games,Start Percentage\n')

leagues = standings_table.findAll('div', {'class' : 'leagues'})[:3]

league_count = -1;

for league in leagues:
	league_count += 1

	league_url = league.find('a')['href']
	league_division = sanitizeData(league.find('a').text.replace('Boys ','').replace('-',''))

	league_response = requests.get(league_url, headers = headers)

	lsoup = bs4.BeautifulSoup(league_response.text, 'lxml')

	standings = lsoup.find('div', {'id' : 'standings'})

	team_as = standings.findAll('a')

	team_count = 0;

	for team_a in team_as:
		team_url = team_a['href']
		team_name = sanitizeData(team_a.text)


		team_count += 1
		print("Entering (" + team_name + "): " + str(team_count) + "/" + str(len(team_as)) + " : " + str((team_count/len(team_as)/3 + league_count/len(leagues))*100)[:4] + "%")

		team_response = requests.get(team_url, headers = headers)

		tsoup = bs4.BeautifulSoup(team_response.text, 'lxml')

		# Info per player: YOB, Name, Team, Division, GP, GS, S%, G
		rosterTable = tsoup.find('table', {'class' : 'rosterTable'})
		players = rosterTable.findAll('tr', {'class' : 'even'}) + rosterTable.findAll('tr', {'class' : 'odd'})

		for player in players:

			name = sanitizeData(player.find('a').text)
			#team_name
			#league_division
			yob = sanitizeData(player.findAll('td', {'class' : 'center'})[0].text)
			appearances = sanitizeData(player.findAll('td', {'class' : 'center'})[2].text)
			starts = sanitizeData(player.findAll('td', {'class' : 'center'})[3].text)
			st_per = str(float(sanitizeData(player.findAll('td', {'class' : 'center'})[4].text)) / 1000)
			total_games = '1000' if float(st_per) == 0 else str(round(float(starts)/float(st_per)))
			st_per = str(float(starts)/float(total_games))
			goals = sanitizeData(player.findAll('td', {'class' : 'center'})[5].text)

			f.write(name+','+team_name+','+league_division+','+yob+','+goals+','+starts+','+appearances+','+total_games+','+st_per+'\n')
f.close()

time_end = time.time()

print('Elapsed time: ' + str((time_end-time_start)/60.0) + ' minutes....')