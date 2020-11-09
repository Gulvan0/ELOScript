import math
import json
from tabulate import tabulate

table_headers = ("#", "Player", "Rating", "Games", "Wins", "Losses", "Draws", "Score vs next")
data = {}

def new_matchup():
  return {"w": 0, "l": 0, "d": 0}

def new_player():
  return {"rating": 1500, "wins": 0, "losses": 0, "draws": 0, "matchups": {}}

def calc_total(player):
  return player["wins"] + player["losses"] + player["draws"]

def reward(r1, r2, sa, totalGames):
  return math.floor(16 * max(25 - 2*totalGames, 1) * (sa - 1 / (1 + 10**((r2-r1)/400))))

def write_rating(rating, games):
  s = str(rating)
  if games < 12:
    s += " (?)"
  return s

def output():
  rows = []
  for (k, v) in data.items():
    i = 0
    while i < len(rows):
      if v["rating"] >= rows[i][1]:
        break
      i += 1
    rows.insert(i, [k, v["rating"], calc_total(v), v["wins"], v["losses"], v["draws"]])
  for ind, r in enumerate(rows):
    r.insert(0, ind+1)
    r[2] = write_rating(r[2], r[3])
    if ind < len(rows) - 1:
      m1, _ = get_matchups(r[1], rows[ind+1][0])
      r.append(calc_score(m1["w"], m1["l"], m1["d"]))
    else:
      r.append("-")
  return tabulate(rows, headers = table_headers)

def calc_score(wins, loses, draws):
  return str(wins+draws/2)+"-"+str(loses+draws/2)

def print_matchups(player):
  stats = data.get(player)
  if stats == None:
    print("Player " + player + " not found, aborting")
    return 
  rows = []
  for (k, v) in stats["matchups"].items():
    rows.append([k, calc_score(v["w"], v["l"], v["d"]) ,v["w"], v["l"], v["d"]])
  print(tabulate(rows, ("Opponent", "Score", "Wins", "Losses", "Draws")))

def get_matchups(p1, p2):
  first = data[p1]
  second = data[p2]
  if first == None or second == None:
    return (None, None)
  if first["matchups"].get(p2) == None:
    first["matchups"][p2] = new_matchup()
  if second["matchups"].get(p1) == None:
    second["matchups"][p1] = new_matchup()
  data[p1] = first
  data[p2] = second
  return (first["matchups"][p2], second["matchups"][p1])

def set_matchup(p1, p2, w, l, d):
  m1, m2 = get_matchups(p1, p2)
  if (m1, m2) == (None, None):
    print("One of the players isn't found, aborting")
    return
  m1["w"] = m2["l"] = w
  m1["l"] = m2["w"] = l
  m1["d"] = m2["d"] = d
  data[p1]["matchups"][p2] = m1
  data[p2]["matchups"][p1] = m2
  with open("data.json", "w") as f:
    json.dump(data, f)
  with open("rating.txt", "w") as f:
    f.write(output())
  print("Matchups updated!")

def update_matchup(p1, p2, outcome):
  m1, m2 = get_matchups(p1, p2)
  if (m1, m2) == (None, None):
    print("One of the players isn't found, aborting")
    return
  if outcome == "w":
    m1["w"] += 1
    m2["l"] += 1
  elif outcome == "l":
    m1["l"] += 1
    m2["w"] += 1
  elif outcome == "d":
    m1["d"] += 1
    m2["d"] += 1
  data[p1]["matchups"][p2] = m1
  data[p2]["matchups"][p1] = m2

with open("data.json", "r") as f:
  data = json.load(f)

while True:
  inp = input().split()

  if inp[0] == "show":
    print(output())
    continue

  if inp[0] == "matchups":
    if len(inp) != 2:
      print("Usage: matchups player")
    else:
      print_matchups(inp[1].lower())
    continue

  if inp[0] == "setmatchups":
    if len(inp) != 6:
      print("Usage: setmatchups player1 player2 wins losses draws")
    else:
      set_matchup(inp[1].lower(), inp[2].lower(), int(inp[3]), int(inp[4]), int(inp[5]))
    continue
  
  if len(inp) != 3:
    print("Usage: player1 player2 w/l/d")
    continue

  firstName = inp[0].lower()
  secondName = inp[1].lower()
  first = data.get(firstName)
  second = data.get(secondName)

  if first == None:
    print(firstName + " not found, creating new profile")
    first = new_player()
  if second == None:
    print(secondName + " not found, creating new profile")
    second = new_player()

  if inp[2] == "d":
    firstSa = 0.5
    first["draws"] += 1
    second["draws"] += 1
  elif inp[2] == "l":
    firstSa = 0
    first["losses"] += 1
    second["wins"] += 1
  elif inp[2] == "w":
    firstSa = 1
    first["wins"] += 1
    second["losses"] += 1
  else:
    print("Invalid outcome: " + inp[2])
  secondSa = 1 - firstSa

  first["rating"] += reward(first["rating"], second["rating"], firstSa, calc_total(first))
  second["rating"] += reward(second["rating"], first["rating"], secondSa, calc_total(second))
  data[firstName] = first
  data[secondName] = second
  update_matchup(firstName, secondName, inp[2])

  with open("data.json", "w") as f:
    json.dump(data, f)
  with open("rating.txt", "w") as f:
    f.write(output())

  print("Rating changed. The new values are: ")
  print(tabulate([[firstName, first["rating"]], [secondName, second["rating"]]]))