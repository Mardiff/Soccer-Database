# Soccer-Database

This repository can be used to create a relational database of soccer games using Python, PHP, and MySQL. It works for any league that has complete data on transfermarkt.com.

## Fetching Data
The python file "ultimate_scrape.py" is used to scrape data from Transfermarkt. When ran, it asks for the user to provide a league url of a specific season (e.g, https://www.transfermarkt.co.uk/major-league-soccer/startseite/wettbewerb/MLS1/plus/?saison_id=2017). Make sure to include the "saison_id=2017" since the code uses the year to create the name of the csv it stores the data in.

## Uploading Data
The php file "upload_to_database.php" is used to upload the csv to a database. Right now it's set to my local database, but that can be easily changed. If you want to make the same database, "create_database.sql" will create the same database.

## Analyzing Data
Right now all data analysis is done using MySQL, which is kept in the "Database SQL" folder. While that is useful for gathering information, this is limited in it's visualization, so in the future I want to use Python database analysis in integration with Pandas and other stuff to make the process more streamlined.

## Future Plans
1. Make PHP ask for username and password so my information isn't on there.
2. Make PHP ask for filename and database name, because it's dumb that it doesn't.
3. Get rid of the PHP part and turn as much of it into Python as possbile. From there, integrate Python database analysis to easily create functions that calculate data and create graphics with simple function calls.
