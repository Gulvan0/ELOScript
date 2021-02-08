from datetime import datetime
import json
from tabulate import tabulate
import playerinfoutils
from extractor import get_matchups

table_headers = ("#", "Player", "Rating", "Games", "Wins", "Losses", "Draws", "Score vs Runner-up")

def _export_filename():
    timestamp = str(datetime.today())
    timestamp = timestamp.split(".")[0]
    timestamp = timestamp.replace(" ", "_")
    timestamp = timestamp.replace(":", "-")
    return "rating_" + timestamp + ".txt"

def _get_str_rating(rating, total_games):
  s = str(rating)
  if total_games < 12:
    s += " (?)"
  return s
  
def _get_str_personal_score(wins, losses, draws):
  return str(wins+draws/2)+"-"+str(losses+draws/2)

def _assemble_general_info(data):
  result = []
  for (name, playerdata) in data.items():
    playerinfo = {}
    playerinfo["name"] = name
    playerinfo["rating"] = playerdata["rating"]
    playerinfo["total_games_count"] = playerinfoutils.total_games(playerdata)
    playerinfo["win_count"] = playerdata["wins"]
    playerinfo["loss_count"] = playerdata["losses"]
    playerinfo["draw_count"] = playerdata["draws"]
    result.append(playerinfo)
  return result

def _enumerate_info(info):
  for index, playerinfo in enumerate(info):
    playerinfo["position"] = index + 1

def _convert_info_to_ratings(data, info):
  rating_rows = []
  for pinfo in info:
    stringified_rating = _get_str_rating(pinfo["rating"], pinfo["total_games_count"])
    if pinfo["position"] < len(info):
        runnerup_index = pinfo["position"] # as index = position - 1
        runnerup_login = info[runnerup_index]["name"]
        matchups_vs_runnerup = get_matchups(data, pinfo["name"], runnerup_login)[0]
        score_vs_runnerup =  _get_str_personal_score(matchups_vs_runnerup["w"], matchups_vs_runnerup["l"], matchups_vs_runnerup["d"])
    else:
        score_vs_runnerup = "Not applicable"
    row = [pinfo["position"], pinfo["name"], stringified_rating, pinfo["total_games_count"], pinfo["win_count"], pinfo["loss_count"], pinfo["draw_count"], score_vs_runnerup]
    rating_rows.append(row)
  return rating_rows

def _stringify(data):
  assembled_info = _assemble_general_info(data)
  assembled_info.sort(key = lambda playerinfo: playerinfo["rating"], reverse = True)
  _enumerate_info(assembled_info)

  rows = _convert_info_to_ratings(data, assembled_info)
  return tabulate(rows, headers = table_headers)

def print_table(data):
    print(_stringify(data))

def export_table(data):
    with open(_export_filename(), "w") as f:
        f.write(_stringify(data))

def print_matchups_of_player(data, player_login):
  playerinfo = data.get(player_login)
  if playerinfo == None:
    print("Player " + player_login + " not found, cancelling")
    return 

  headers = ("Opponent", "Score", "Wins", "Losses", "Draws")
  rows = []
  for (opponent_login, matchups_vs_opponent) in playerinfo["matchups"].items():
    score_vs_opponent = _get_str_personal_score(matchups_vs_opponent["w"], matchups_vs_opponent["l"], matchups_vs_opponent["d"])
    row = [opponent_login, score_vs_opponent, matchups_vs_opponent["w"], matchups_vs_opponent["l"], matchups_vs_opponent["d"]]
    rows.append(row)
  print(tabulate(rows, headers))