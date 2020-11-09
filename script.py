import math
import json
from tabulate import tabulate

table_headers = ("#", "Player", "Rating", "Games", "Wins", "Losses", "Draws")
data = {}

def new_player():
  return {"rating": 1500, "wins": 0, "losses": 0, "draws": 0}

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
  return tabulate(rows, headers = table_headers)

with open("data.json", "r") as f:
  data = json.load(f)

while True:
  inp = input().split()

  if inp[0] == "show":
    print(output())
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

  with open("data.json", "w") as f:
    json.dump(data, f)
  with open("rating.txt", "w") as f:
    f.write(output())

  print("Rating changed. The new values are: ")
  print(tabulate([[firstName, first["rating"]], [secondName, second["rating"]]]))