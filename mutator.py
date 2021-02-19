import extractor
import playerinfoutils
import math
import json
from tabulate import tabulate

def _opposite_outcome(outcome):
    if outcome == "w":
        return "l"
    elif outcome == "l":
        return "w"
    else:
        return "d"

def _reward(r1, r2, sa, totalGames):
  return math.floor(16 * max(25 - 2*totalGames, 1) * (sa - 1 / (1 + 10**((r2-r1)/400))))

def new_matchup():
  return {"w": 0, "l": 0, "d": 0}

def _new_player():
  return {"rating": 1500, "wins": 0, "losses": 0, "draws": 0, "matchups": {}}

def dump(data):
  with open("data.json", "w") as f:
    json.dump(data, f)

def set_matchup(data, login1, login2, w, l, d):
  m1, m2 = extractor.get_matchups(data, login1, login2)
  if (m1, m2) == (None, None):
    print("One of the players doesn't exist, cancelling")
    return False

  data[login1]["wins"] += w - m1["w"]
  data[login1]["losses"] += l - m1["l"]
  data[login1]["draws"] += d - m1["d"]
  data[login2]["wins"] += l - m2["w"]
  data[login2]["losses"] += w - m2["l"]
  data[login2]["draws"] += d - m2["d"]


  m1["w"] = m2["l"] = w
  m1["l"] = m2["w"] = l
  m1["d"] = m2["d"] = d

  data[login1]["matchups"][login2], data[login2]["matchups"][login1] = m1, m2

  dump(data)
  print("Matchups updated!")
  return True

def __aftermatch_modify_matchup(data, winner_login, loser_login, draw):
  m1, m2 = extractor.get_matchups(data, winner_login, loser_login)

  if draw:
    m1["d"] += 1
    m2["d"] += 1
  else:
    m1["w"] += 1
    m2["l"] += 1

  data[winner_login]["matchups"][loser_login], data[loser_login]["matchups"][winner_login] = m1, m2

def __aftermatch_modify_stats(data, winner_login, loser_login, draw):
  winner_data, loser_data = data.get(winner_login), data.get(loser_login)

  if draw:
    winner_data["draws"] += 1
    loser_data["draws"] += 1
  else:
    winner_data["wins"] += 1
    loser_data["losses"] += 1

def __aftermatch_modify_rating(data, winner_login, loser_login, draw):
  winner_data, loser_data = data.get(winner_login), data.get(loser_login)  

  winner_coef = 0.5 if draw else 1  
  loser_coef = 1 - winner_coef

  winner_data["rating"] += _reward(winner_data["rating"], loser_data["rating"], winner_coef, playerinfoutils.total_games(winner_data))
  loser_data["rating"] += _reward(loser_data["rating"], winner_data["rating"], loser_coef, playerinfoutils.total_games(loser_data))

  print("Rating changed. The new values are: ")
  print(tabulate([[winner_login, winner_data["rating"]], [loser_login, loser_data["rating"]]]))

def __aftermatch_confirm_player_exists(data, login):
  if data.get(login) == None:
    print(login + " not found, create a new profile? (Y/N)")
    answer = input()
    if answer == "Y":
      data[login] = _new_player()
      print("Player " + login + " created")
      return True
    elif answer == "N":
      print("Operation cancelled")
      return False
    else:
      print("Unrecognized answer, cancelling the operation")
      return False
  return True

def save_match_results(data, login1, login2, outcome):
  if not __aftermatch_confirm_player_exists(data, login1):
    return False
  if not __aftermatch_confirm_player_exists(data, login2):
    return False

  if outcome == "w":
    winner_login, loser_login = login1, login2
  else:
    winner_login, loser_login = login2, login1
  draw = outcome == "d"

  __aftermatch_modify_matchup(data, winner_login, loser_login, draw)
  __aftermatch_modify_stats(data, winner_login, loser_login, draw)
  __aftermatch_modify_rating(data, winner_login, loser_login, draw)

  dump(data)
  return True

def remove_player(data, login):
  if data.get(login) == None:
    print(login + " not found, cancelling")
    return False
  del data[login]
  dump(data)
  print("Removed player: " + login)
  return True

def merge_players(data, login_from, login_to):
  from_data, to_data = data.get(login_from), data.get(login_to)
  if from_data == None:
    print(login_from + " not found, cancelling")
    return False
  if to_data == None:
    print(login_to + " not found, cancelling")
    return False
  
  to_data["wins"] += from_data["wins"] - from_data["matchups"][login_to]["w"] - to_data["matchups"][login_from]["w"]
  to_data["losses"] += from_data["losses"] - from_data["matchups"][login_to]["l"] - to_data["matchups"][login_from]["l"]
  to_data["draws"] += from_data["draws"] - from_data["matchups"][login_to]["d"] - to_data["matchups"][login_from]["d"]
  to_data["rating"] = math.floor((to_data["rating"] + from_data["rating"]) / 2)

  to_data["matchups"].pop(login_from, None)
  for (opponent, matchup) in from_data["matchups"].items():
    if opponent != login_to:
      if to_data["matchups"].get(opponent) == None:
        to_data["matchups"][opponent] = new_matchup()
      if data[opponent]["matchups"].get(login_to) == None:
        data[opponent]["matchups"][login_to] = new_matchup()
      for (outcome, count) in matchup.items():
        to_data["matchups"][opponent][outcome] += count
        data[opponent]["matchups"][login_to][_opposite_outcome(outcome)] += count
      data[opponent]["matchups"].pop(login_from, None)

  del data[login_from]
  dump(data)
  print("Players merged: " + login_from + " -> " + login_to)
  return True

def deactivate_player(data, login):
  playerdata = data.get(login)
  if playerdata == None:
    print(login + " not found, cancelling")
    return False
  playerdata["hide"] = True
  return True

def reactivate_player(data, login):
  playerdata = data.get(login)
  if playerdata == None:
    print(login + " not found, cancelling")
    return False
  playerdata.pop("hide", None)
  return True
