SELECT AnalWLeagues.league, SUM(AnalWLeagues.Domestic) as Domestic, SUM(AnalWLeagues.Total) as Total, (100 * SUM(AnalWLeagues.Domestic) / SUM(AnalWLeagues.Total)) as Percentage
FROM
(SELECT League.name as league, Team.name, Analysis.Domestic, Analysis.Total
FROM
League, Team,
(SELECT Team.name, IFNULL(dirty.Domestic,0) as Domestic, IFNULL(dirty.Total,0) as Total, IFNULL(dirty.Percentage,0) as Percentage
FROM Team,
(SELECT all_minutes.id, all_domestic_minutes.minutes as Domestic, all_minutes.minutes as Total, IFNULL(((all_domestic_minutes.minutes/all_minutes.minutes) * 100),0) as Percentage
FROM
(SELECT total.id, IFNULL((total.minutes-reds.minutes),total.minutes) as minutes
FROM
(SELECT Team.id, (COUNT(*)*990) as minutes
FROM Team, Game
WHERE (Game.home = Team.id OR Game.away = Team.id)
GROUP BY Team.id) as total
LEFT JOIN
(SELECT Team.id, SUM(90-Event.minute) as minutes
FROM Team, Event
WHERE Event.team = Team.id
AND (Event.type = 'red' OR Event.type = 'yellowred')
GROUP BY Team.id) as reds
ON total.id = reds.id) as all_minutes
LEFT JOIN
(SELECT startin_minutes.id, IFNULL(startin_minutes.minutes - subout_minutes.minutes, startin_minutes.minutes) as minutes
FROM
(SELECT start_minutes.id, IFNULL(start_minutes.minutes + subin_minutes.minutes, start_minutes.minutes) as minutes
FROM
(SELECT Team.id, IFNULL(start_minutes.minutes, 0) as minutes
FROM Team
LEFT JOIN
(SELECT a10.id, IFNULL(a10.usstarts+a11.usstarts,a10.usstarts)*90 as minutes
FROM
(SELECT a9.id, IFNULL(a9.usstarts+a10.usstarts,a9.usstarts) as usstarts
FROM
(SELECT a8.id, IFNULL(a8.usstarts+a9.usstarts,a8.usstarts) as usstarts
FROM
(SELECT a7.id, IFNULL(a7.usstarts+a8.usstarts,a7.usstarts) as usstarts
FROM
(SELECT a6.id, IFNULL(a6.usstarts+a7.usstarts,a6.usstarts) as usstarts
FROM
(SELECT a5.id, IFNULL(a5.usstarts+a6.usstarts,a5.usstarts) as usstarts
FROM
(SELECT a4.id, IFNULL(a4.usstarts+a5.usstarts,a4.usstarts) as usstarts
FROM
(SELECT a3.id, IFNULL(a3.usstarts+a4.usstarts,a3.usstarts) as usstarts
FROM
(SELECT a2.id, IFNULL(a2.usstarts+a3.usstarts,a2.usstarts) as usstarts
FROM
(SELECT a1.id, IFNULL(a1.usstarts+a2.usstarts,a1.usstarts) as usstarts
FROM
(SELECT h12345678901.id, IFNULL(h12345678901.usstarts+a1.usstarts,h12345678901.usstarts) as usstarts
FROM
(SELECT h1234567890.id, IFNULL(h1234567890.usstarts+h11.usstarts,h1234567890.usstarts) as usstarts
FROM
(SELECT h123456789.id, IFNULL(h123456789.usstarts+h10.usstarts,h123456789.usstarts) as usstarts
FROM
(SELECT h12345678.id, IFNULL(h12345678.usstarts+h9.usstarts,h12345678.usstarts) as usstarts
FROM
(SELECT h1234567.id, IFNULL(h1234567.usstarts+h8.usstarts,h1234567.usstarts) as usstarts
FROM
(SELECT h123456.id, IFNULL(h123456.usstarts+h7.usstarts,h123456.usstarts) as usstarts
FROM
(SELECT h12345.id, IFNULL(h12345.usstarts+h6.usstarts,h12345.usstarts) as usstarts
FROM
(SELECT h1234.id, IFNULL(h1234.usstarts+h5.usstarts,h1234.usstarts) as usstarts
FROM
(SELECT h123.id, IFNULL(h123.usstarts+h4.usstarts,h123.usstarts) as usstarts
FROM
(SELECT h12.id, IFNULL(h12.usstarts+h3.usstarts,h12.usstarts) as usstarts
FROM
(SELECT h1.id, IFNULL(h1.usstarts+h2.usstarts,h1.usstarts) as usstarts
FROM
(SELECT Team.id, IFNULL(h1.usstarts,0) as usstarts
FROM
Team
LEFT JOIN
(SELECT Team.id, COUNT(*) as usstarts
FROM League, Team, Player, Game
WHERE Game.home = Team.id
AND Game.home1 = Player.id
AND ((Player.nat1 = League.country OR Player.nat2 = League.country) AND Player.birthdate >= '1997-01-01') AND Team.league = League.id
GROUP BY Team.id) as h1
ON Team.id = h1.id) as h1
LEFT JOIN
(SELECT Team.id, COUNT(*) as usstarts
FROM League, Team, Player, Game
WHERE Game.home = Team.id
AND Game.home2 = Player.id
AND ((Player.nat1 = League.country OR Player.nat2 = League.country) AND Player.birthdate >= '1997-01-01') AND Team.league = League.id
GROUP BY Team.id) as h2
ON h1.id = h2.id) as h12
LEFT JOIN
(SELECT Team.id, COUNT(*) as usstarts
FROM League, Team, Player, Game
WHERE Game.home = Team.id
AND Game.home3 = Player.id
AND ((Player.nat1 = League.country OR Player.nat2 = League.country) AND Player.birthdate >= '1997-01-01') AND Team.league = League.id
GROUP BY Team.id) as h3
ON h12.id = h3.id) as h123
LEFT JOIN
(SELECT Team.id, COUNT(*) as usstarts
FROM League, Team, Player, Game
WHERE Game.home = Team.id
AND Game.home4 = Player.id
AND ((Player.nat1 = League.country OR Player.nat2 = League.country) AND Player.birthdate >= '1997-01-01') AND Team.league = League.id
GROUP BY Team.id) as h4
ON h123.id = h4.id) as h1234
LEFT JOIN
(SELECT Team.id, COUNT(*) as usstarts
FROM League, Team, Player, Game
WHERE Game.home = Team.id
AND Game.home5 = Player.id
AND ((Player.nat1 = League.country OR Player.nat2 = League.country) AND Player.birthdate >= '1997-01-01') AND Team.league = League.id
GROUP BY Team.id) as h5
ON h1234.id = h5.id) as h12345
LEFT JOIN
(SELECT Team.id, COUNT(*) as usstarts
FROM League, Team, Player, Game
WHERE Game.home = Team.id
AND Game.home6 = Player.id
AND ((Player.nat1 = League.country OR Player.nat2 = League.country) AND Player.birthdate >= '1997-01-01') AND Team.league = League.id
GROUP BY Team.id) as h6
ON h12345.id = h6.id) as h123456
LEFT JOIN
(SELECT Team.id, COUNT(*) as usstarts
FROM League, Team, Player, Game
WHERE Game.home = Team.id
AND Game.home7 = Player.id
AND ((Player.nat1 = League.country OR Player.nat2 = League.country) AND Player.birthdate >= '1997-01-01') AND Team.league = League.id
GROUP BY Team.id) as h7
ON h123456.id = h7.id) as h1234567
LEFT JOIN
(SELECT Team.id, COUNT(*) as usstarts
FROM League, Team, Player, Game
WHERE Game.home = Team.id
AND Game.home8 = Player.id
AND ((Player.nat1 = League.country OR Player.nat2 = League.country) AND Player.birthdate >= '1997-01-01') AND Team.league = League.id
GROUP BY Team.id) as h8
ON h1234567.id = h8.id) as h12345678
LEFT JOIN
(SELECT Team.id, COUNT(*) as usstarts
FROM League, Team, Player, Game
WHERE Game.home = Team.id
AND Game.home9 = Player.id
AND ((Player.nat1 = League.country OR Player.nat2 = League.country) AND Player.birthdate >= '1997-01-01') AND Team.league = League.id
GROUP BY Team.id) as h9
ON h12345678.id = h9.id) as h123456789
LEFT JOIN
(SELECT Team.id, COUNT(*) as usstarts
FROM League, Team, Player, Game
WHERE Game.home = Team.id
AND Game.home10 = Player.id
AND ((Player.nat1 = League.country OR Player.nat2 = League.country) AND Player.birthdate >= '1997-01-01') AND Team.league = League.id
GROUP BY Team.id) as h10
ON h123456789.id = h10.id) as h1234567890
LEFT JOIN
(SELECT Team.id, COUNT(*) as usstarts
FROM League, Team, Player, Game
WHERE Game.home = Team.id
AND Game.home11 = Player.id
AND ((Player.nat1 = League.country OR Player.nat2 = League.country) AND Player.birthdate >= '1997-01-01') AND Team.league = League.id
GROUP BY Team.id) as h11
ON h1234567890.id = h11.id) as h12345678901
LEFT JOIN
(SELECT Team.id, COUNT(*) as usstarts
FROM League, Team, Player, Game
WHERE Game.away = Team.id
AND Game.away1 = Player.id
AND ((Player.nat1 = League.country OR Player.nat2 = League.country) AND Player.birthdate >= '1997-01-01') AND Team.league = League.id
GROUP BY Team.id) as a1
ON h12345678901.id = a1.id) as a1
LEFT JOIN
(SELECT Team.id, COUNT(*) as usstarts
FROM League, Team, Player, Game
WHERE Game.away = Team.id
AND Game.away2 = Player.id
AND ((Player.nat1 = League.country OR Player.nat2 = League.country) AND Player.birthdate >= '1997-01-01') AND Team.league = League.id
GROUP BY Team.id) as a2
ON a1.id = a2.id) as a2
LEFT JOIN
(SELECT Team.id, COUNT(*) as usstarts
FROM League, Team, Player, Game
WHERE Game.away = Team.id
AND Game.away3 = Player.id
AND ((Player.nat1 = League.country OR Player.nat2 = League.country) AND Player.birthdate >= '1997-01-01') AND Team.league = League.id
GROUP BY Team.id) as a3
ON a2.id = a3.id) as a3
LEFT JOIN
(SELECT Team.id, COUNT(*) as usstarts
FROM League, Team, Player, Game
WHERE Game.away = Team.id
AND Game.away4 = Player.id
AND ((Player.nat1 = League.country OR Player.nat2 = League.country) AND Player.birthdate >= '1997-01-01') AND Team.league = League.id
GROUP BY Team.id) as a4
ON a3.id = a4.id) as a4
LEFT JOIN
(SELECT Team.id, COUNT(*) as usstarts
FROM League, Team, Player, Game
WHERE Game.away = Team.id
AND Game.away5 = Player.id
AND ((Player.nat1 = League.country OR Player.nat2 = League.country) AND Player.birthdate >= '1997-01-01') AND Team.league = League.id
GROUP BY Team.id) as a5
ON a4.id = a5.id) as a5
LEFT JOIN
(SELECT Team.id, COUNT(*) as usstarts
FROM League, Team, Player, Game
WHERE Game.away = Team.id
AND Game.away6 = Player.id
AND ((Player.nat1 = League.country OR Player.nat2 = League.country) AND Player.birthdate >= '1997-01-01') AND Team.league = League.id
GROUP BY Team.id) as a6
ON a5.id = a6.id) as a6
LEFT JOIN
(SELECT Team.id, COUNT(*) as usstarts
FROM League, Team, Player, Game
WHERE Game.away = Team.id
AND Game.away7 = Player.id
AND ((Player.nat1 = League.country OR Player.nat2 = League.country) AND Player.birthdate >= '1997-01-01') AND Team.league = League.id
GROUP BY Team.id) as a7
ON a6.id = a7.id) as a7
LEFT JOIN
(SELECT Team.id, COUNT(*) as usstarts
FROM League, Team, Player, Game
WHERE Game.away = Team.id
AND Game.away8 = Player.id
AND ((Player.nat1 = League.country OR Player.nat2 = League.country) AND Player.birthdate >= '1997-01-01') AND Team.league = League.id
GROUP BY Team.id) as a8
ON a7.id = a8.id) as a8
LEFT JOIN
(SELECT Team.id, COUNT(*) as usstarts
FROM League, Team, Player, Game
WHERE Game.away = Team.id
AND Game.away9 = Player.id
AND ((Player.nat1 = League.country OR Player.nat2 = League.country) AND Player.birthdate >= '1997-01-01') AND Team.league = League.id
GROUP BY Team.id) as a9
ON a8.id = a9.id) as a9
LEFT JOIN
(SELECT Team.id, COUNT(*) as usstarts
FROM League, Team, Player, Game
WHERE Game.away = Team.id
AND Game.away10 = Player.id
AND ((Player.nat1 = League.country OR Player.nat2 = League.country) AND Player.birthdate >= '1997-01-01') AND Team.league = League.id
GROUP BY Team.id) as a10
ON a9.id = a10.id) as a10
LEFT JOIN
(SELECT Team.id, COUNT(*) as usstarts
FROM League, Team, Player, Game
WHERE Game.away = Team.id
AND Game.away11 = Player.id
AND ((Player.nat1 = League.country OR Player.nat2 = League.country) AND Player.birthdate >= '1997-01-01') AND Team.league = League.id
GROUP BY Team.id) as a11
ON a10.id = a11.id) as start_minutes
ON Team.id = start_minutes.id) as start_minutes
LEFT JOIN
(SELECT Team.id, SUM(90-Event.minute) as minutes
FROM League, Team, Player as Player1, Player as Player2, Event
WHERE Event.team = Team.id
AND Team.league = League.id
AND Event.type = 'sub'
AND Event.player1 = Player1.id
AND Event.player2 = Player2.id
AND ((Player2.nat1 = League.country OR Player2.nat2 = League.country) AND Player2.birthdate >= '1997-01-01')
AND (NOT ((Player1.nat1 = League.country OR Player1.nat2 = League.country) AND Player1.birthdate >= '1997-01-01'))
GROUP BY Team.id) as subin_minutes
ON start_minutes.id = subin_minutes.id) as startin_minutes
LEFT JOIN
(SELECT Team.id, SUM(90-Event.minute) as minutes
FROM League, Team, Player as Player1, Player as Player2, Event
WHERE Event.team = Team.id
AND Team.league = League.id
AND (((Event.type = 'red' OR Event.type = 'yellowred') AND Event.player1 = Player1.id AND Player1.id = Player2.id AND ((Player1.nat1 = League.country OR Player1.nat2 = League.country) AND Player1.birthdate >= '1997-01-01')) 
OR (Event.type = 'sub'
AND Event.player1 = Player1.id
AND Event.player2 = Player2.id
AND (NOT ((Player2.nat1 = League.country OR Player2.nat2 = League.country) AND Player2.birthdate >= '1997-01-01'))
AND ((Player1.nat1 = League.country OR Player1.nat2 = League.country) AND Player1.birthdate >= '1997-01-01')))
GROUP BY Team.id) as subout_minutes
ON startin_minutes.id = subout_minutes.id) as all_domestic_minutes
ON all_minutes.id = all_domestic_minutes.id) as dirty
WHERE Team.id = dirty.id) as Analysis
WHERE Analysis.name = Team.name AND Team.league = League.id) as AnalWLeagues
GROUP BY AnalWLeagues.league
ORDER BY Percentage DESC