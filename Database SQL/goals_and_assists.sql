SELECT Player.name, goal_count.goals, assist_count.assists, (goal_count.goals+assist_count.assists) as 'G+A'
FROM Player,
(SELECT Player.id, COUNT(Player.id) AS goals
FROM Player,Event
WHERE type = 'goal' AND
Player.id = Event.player1
GROUP BY Player.id) as goal_count,
(SELECT Player.id, COUNT(Player.id) AS assists
FROM Player,Event
WHERE type = 'goal' AND
Player.id = Event.player2 AND
Event.player1 != Event.player2
GROUP BY Player.id) as assist_count
WHERE Player.id = goal_count.id  AND
Player.id = assist_count.id  