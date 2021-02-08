import mutator

def has_matchup(playerdata, others_login):
  return playerdata["matchups"].get(others_login) != None

def get_matchups(data, player1_login, player2_login):
  playerdata_1 = data.get(player1_login)
  playerdata_2 = data.get(player2_login)
  if playerdata_1 == None or playerdata_2 == None:
    return (None, None)

  if has_matchup(playerdata_1, player2_login):
    return (playerdata_1["matchups"][player2_login], playerdata_2["matchups"][player1_login])
  else:
    return (mutator.new_matchup(), mutator.new_matchup())