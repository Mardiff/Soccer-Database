SELECT subs.game, (subs.z + starts.y) as homegrowns
FROM
(SELECT game, SUM(IF(Player.homegrown, 1, 0)) as z
FROM Event, Player
WHERE player2 = Player.id AND Event.type = 'sub'
GROUP BY game) as subs,
(SELECT Game.id, IF(Player.homegrown, 1 + sample.y, 0 + sample.y) as y
FROM Game, Player,
(SELECT Game.id, IF(Player.homegrown, 1 + sample.y, 0 + sample.y) as y
FROM Game, Player,
(SELECT Game.id, IF(Player.homegrown, 1 + sample.y, 0 + sample.y) as y
FROM Game, Player,
(SELECT Game.id, IF(Player.homegrown, 1 + sample.y, 0 + sample.y) as y
FROM Game, Player,
(SELECT Game.id, IF(Player.homegrown, 1 + sample.y, 0 + sample.y) as y
FROM Game, Player,
(SELECT Game.id, IF(Player.homegrown, 1 + sample.y, 0 + sample.y) as y
FROM Game, Player,
(SELECT Game.id, IF(Player.homegrown, 1 + sample.y, 0 + sample.y) as y
FROM Game, Player,
(SELECT Game.id, IF(Player.homegrown, 1 + sample.y, 0 + sample.y) as y
FROM Game, Player,
(SELECT Game.id, IF(Player.homegrown, 1 + sample.y, 0 + sample.y) as y
FROM Game, Player,
(SELECT Game.id, IF(Player.homegrown, 1 + sample.y, 0 + sample.y) as y
FROM Game, Player,
(SELECT Game.id, IF(Player.homegrown, 1 + sample.y, 0 + sample.y) as y
FROM Game, Player,
(SELECT Game.id, IF(Player.homegrown, 1 + sample.y, 0 + sample.y) as y
FROM Game, Player,
(SELECT Game.id, IF(Player.homegrown, 1 + sample.y, 0 + sample.y) as y
FROM Game, Player,
(SELECT Game.id, IF(Player.homegrown, 1 + sample.y, 0 + sample.y) as y
FROM Game, Player,
(SELECT Game.id, IF(Player.homegrown, 1 + sample.y, 0 + sample.y) as y
FROM Game, Player,
(SELECT Game.id, IF(Player.homegrown, 1 + sample.y, 0 + sample.y) as y
FROM Game, Player,
(SELECT Game.id, IF(Player.homegrown, 1 + sample.y, 0 + sample.y) as y
FROM Game, Player,
(SELECT Game.id, IF(Player.homegrown, 1 + sample.y, 0 + sample.y) as y
FROM Game, Player,
(SELECT Game.id, IF(Player.homegrown, 1 + sample.y, 0 + sample.y) as y
FROM Game, Player,
(SELECT Game.id, IF(Player.homegrown, 1 + sample.y, 0 + sample.y) as y
FROM Game, Player,
(SELECT Game.id, IF(Player.homegrown, 1 + sample.y, 0 + sample.y) as y
FROM Game, Player,
(SELECT Game.id, IF(Player.homegrown, 1, 0) as y
FROM Game, Player
WHERE home1 = Player.id) as sample
WHERE home2 = Player.id AND Game.id = sample.id) as sample
WHERE home3 = Player.id AND Game.id = sample.id) as sample
WHERE home4 = Player.id AND Game.id = sample.id) as sample
WHERE home5 = Player.id AND Game.id = sample.id) as sample
WHERE home6 = Player.id AND Game.id = sample.id) as sample
WHERE home7 = Player.id AND Game.id = sample.id) as sample
WHERE home8 = Player.id AND Game.id = sample.id) as sample
WHERE home9 = Player.id AND Game.id = sample.id) as sample
WHERE home10 = Player.id AND Game.id = sample.id) as sample
WHERE home11 = Player.id AND Game.id = sample.id) as sample
WHERE away1 = Player.id AND Game.id = sample.id) as sample
WHERE away2 = Player.id AND Game.id = sample.id) as sample
WHERE away3 = Player.id AND Game.id = sample.id) as sample
WHERE away4 = Player.id AND Game.id = sample.id) as sample
WHERE away5 = Player.id AND Game.id = sample.id) as sample
WHERE away6 = Player.id AND Game.id = sample.id) as sample
WHERE away7 = Player.id AND Game.id = sample.id) as sample
WHERE away8 = Player.id AND Game.id = sample.id) as sample
WHERE away9 = Player.id AND Game.id = sample.id) as sample
WHERE away10 = Player.id AND Game.id = sample.id) as sample
WHERE away11 = Player.id AND Game.id = sample.id) as starts
WHERE subs.game = starts.id
ORDER BY homegrowns DESC