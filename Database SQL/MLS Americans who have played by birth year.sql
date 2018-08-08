SELECT YEAR(asdfg.birthdate) as birthyear, COUNT(*) as players
FROM


(SELECT asdf.id, asdf.birthdate
FROM

(SELECT Player.id, Player.name, (all_start_minutes.minutes+all_subin_minutes.minutes-all_subout_minutes.minutes) as minutes, Player.birthdate
FROM Player,

(SELECT Player.id, IFNULL(joined_starts.minutes,0) as minutes
FROM Player,
(SELECT Player.id, starts.minutes
FROM Player
LEFT JOIN 
(SELECT Player.id, COUNT(Player.id)*90 as minutes
FROM Player, Game
WHERE (Player.id = home1 OR Player.id = home2 OR Player.id = home3 OR Player.id = home4 OR Player.id = home5 OR Player.id = home6 OR Player.id = home7 OR Player.id = home8 OR Player.id = home9 OR Player.id = home10 OR Player.id = home11 OR Player.id = away1 OR Player.id = away2 OR Player.id = away3 OR Player.id = away4 OR Player.id = away5 OR Player.id = away6 OR Player.id = away7 OR Player.id = away8 OR Player.id = away9 OR Player.id = away10 OR Player.id = away11)
GROUP BY Player.id) as starts
 ON Player.id = starts.id
UNION
SELECT Player.id, starts.minutes
FROM Player
RIGHT JOIN 
(SELECT Player.id, COUNT(Player.id)*90 as minutes
FROM Player, Game
WHERE (Player.id = home1 OR Player.id = home2 OR Player.id = home3 OR Player.id = home4 OR Player.id = home5 OR Player.id = home6 OR Player.id = home7 OR Player.id = home8 OR Player.id = home9 OR Player.id = home10 OR Player.id = home11 OR Player.id = away1 OR Player.id = away2 OR Player.id = away3 OR Player.id = away4 OR Player.id = away5 OR Player.id = away6 OR Player.id = away7 OR Player.id = away8 OR Player.id = away9 OR Player.id = away10 OR Player.id = away11)
GROUP BY Player.id) as starts 
ON Player.id = starts.id) as joined_starts
WHERE Player.id = joined_starts.id) as all_start_minutes,

(SELECT Player.id, IFNULL(joined_subins.minutes,0) as minutes
FROM Player,
(SELECT Player.id, subins.minutes
FROM Player
LEFT JOIN 
(SELECT Player.id, SUM(90-Event.minute) as minutes
FROM Player, Event
WHERE Player.id = Event.player2
AND Event.type = 'sub'
GROUP BY Player.id) as subins
 ON Player.id = subins.id
UNION
SELECT Player.id, subins.minutes
FROM Player
RIGHT JOIN 
(SELECT Player.id, SUM(90-Event.minute) as minutes
FROM Player, Event
WHERE Player.id = Event.player2
AND Event.type = 'sub'
GROUP BY Player.id) as subins 
ON Player.id = subins.id) as joined_subins
WHERE Player.id = joined_subins.id) as all_subin_minutes,

(SELECT Player.id, IFNULL(joined_subouts.minutes,0) as minutes
FROM Player,
(SELECT Player.id, subouts.minutes
FROM Player
LEFT JOIN 
(SELECT Player.id, SUM(90-Event.minute) as minutes
FROM Player, Event
WHERE (Player.id = Event.player1
AND (Event.type = 'sub' OR
     Event.type = 'red' OR
     Event.type = 'yellowred'))
GROUP BY Player.id) as subouts
 ON Player.id = subouts.id
UNION
SELECT Player.id, subouts.minutes
FROM Player
RIGHT JOIN 
(SELECT Player.id, SUM(90-Event.minute) as minutes
FROM Player, Event
WHERE (Player.id = Event.player1
AND (Event.type = 'sub' OR
     Event.type = 'red' OR
     Event.type = 'yellowred'))
GROUP BY Player.id) as subouts
ON Player.id = subouts.id) as joined_subouts
WHERE Player.id = joined_subouts.id) as all_subout_minutes

WHERE Player.id = all_start_minutes.id AND Player.id = all_subin_minutes.id AND Player.id = all_subout_minutes.id AND (Player.nat1 = "United States" OR Player.nat2 = "United States")) as asdf
WHERE asdf.minutes > 0)

as asdfg


GROUP BY YEAR(asdfg.birthdate)
ORDER BY birthyear