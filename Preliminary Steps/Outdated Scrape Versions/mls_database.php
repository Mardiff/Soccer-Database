<?php

//Connect to myPHPAdmin
$conn = new mysqli("classroom.cs.unc.edu", "ardiff", "@JoshSargent9", "ardiffdb");	

//Clear databases
$conn->query('TRUNCATE TABLE League;');
$conn->query('TRUNCATE TABLE Team;');
$conn->query('TRUNCATE TABLE Player;');
$conn->query('TRUNCATE TABLE Game;');
$conn->query('TRUNCATE TABLE Event;');

//Load entries into databases
$fhandle = fopen('mls_database.csv', 'r');

$count = 1;

$event_count = 0;

// $sql = "INSERT INTO Player (id, name, birthdate, birthplace, birth_country, height, nat1, nat2, position, team, player_number, value) VALUES (23,'PAUL','3/3/3','BR','USA',23,'United States','N/A','GK',23,23,232323)";

// $conn->query($sql);

//Create all NFL Teams
while($line=fgets($fhandle)) {
	$words = explode(',', $line);

	printf("Entering entry %s out of %s, %d%% \n", $count, 5860, 100*$count/5860);

	// Getting rid of \n at the end of the line
	$words[count($words)-1] = substr($words[count($words)-1],0,strlen($words[count($words)-1])-1);

	$count += 1;

	// LEAGUE
	if($words[0] == '0') {
		$sql = "INSERT INTO League (id, name, country) VALUES ('$words[1]', '$words[2]', '$words[3]')";

		$conn->query($sql);
	}

	// TEAM
	if($words[0] == '1') {
		$sql = "INSERT INTO Team (id, name, league, points) VALUES ($words[1], '$words[2]', '$words[3]', $words[4])";

	
		$conn->query($sql);
	}

	// PLAYER
	if($words[0] == '2') {
		$sql = "INSERT INTO Player (id, name, birthdate, birthplace, birth_country, height, nat1, nat2, position, team, player_number, value) VALUES ($words[1], '$words[2]', '$words[3]', '$words[4]', '$words[5]', $words[6], '$words[7]', '$words[8]', '$words[9]', $words[10], $words[11], $words[12])";

		$conn->query($sql);
	}

	// GAME
	if($words[0] == '3') {
		$sql = "INSERT INTO Game (id, gamedate, home, away, location, attendance, referee, home_manager, away_manager, home_formation, away_formation, home1, home2, home3, home4, home5, home6, home7, home8, home9, home10, home11, away1, away2, away3, away4, away5, away6, away7, away8, away9, away10, away11) VALUES ($words[1], '$words[2]', $words[3], $words[4], '$words[5]', '$words[6]', '$words[7]', '$words[8]', '$words[9]', '$words[10]', '$words[11]', $words[12], $words[13], $words[14], $words[15], $words[16], $words[17], $words[18], $words[19], $words[20], $words[21], $words[22], $words[23], $words[24], $words[25], $words[26], $words[27], $words[28], $words[29], $words[30], $words[31], $words[32], $words[33])";

		$conn->query($sql);
	}

	// EVENT
	if($words[0] == '4') {
		$sql = "INSERT INTO Event (id, game, minute, type, player1, player2, team) VALUES ($event_count, $words[1], $words[2], '$words[3]', $words[4], $words[5], $words[6])";

		$result = $conn->query($sql);

		if(!$result) {
			printf("FAILED: %s\n", $sql);
		}

		$event_count++;
	}
}