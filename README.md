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

3. matchups player - print the matchups of the player

player - player login

4. setmatchups player1 player2 wins losses draws - manually set the matchup data

player1, player2 - player logins
wins - number of player1's wins against player2
losses - number of player1's losses against player2
draws - number of player1's draws against player2