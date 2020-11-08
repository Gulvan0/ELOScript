# ELOScript
 A simple script for hosting small leagues

Default rating is 1500. Maximum rating reward per win is 16 points. 
Player data is stored in data.json. rating.txt contains the pretty-printed actual player rankings

Commands:
1. player1 player2 outcome - score the match results

player1, player2 - player logins
outcome - w (player1 won) / l (player2 won) / d (draw)

Creates a new record if player1 or player2 isn't found

2. show - print the player rankings