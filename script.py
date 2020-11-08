import math
import json
from tabulate import tabulate

table_headers = ("#", "Player", "Rating", "Wins", "Losses", "Draws")
data = {}

def new_player():
  return {"rating": 1500, "wins": 0, "losses": 0, "draws": 0}

def reward(r1, r2, sa):
  return math.floor(16 * (sa - 1 / (1 + 10**((r2-r1)/400))))

def output():
  rows = []
  for k in data.keys():
    i = 0
    while i < len(rows):
      if data[k]["rating"] >= rows[i][1]:
        break
      i += 1
    rows.insert(i, [k, data[k]["rating"], data[k]["wins"], data[k]["losses"], data[k]["draws"]])
  for ind, r in enumerate(rows):
    r.insert(0, ind+1)
  return tabulate(rows, headers = table_headers)

with open("data.json", "r") as f:
  data = json.load(f)
while True:
  inp = input().split()
  if inp[0] == "show":
    print(output())
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
    break
  secondSa = 1 - firstSa

  first["rating"] += reward(first["rating"], second["rating"], firstSa)
  second["rating"] += reward(second["rating"], first["rating"], secondSa)
  data[firstName] = first
  data[secondName] = second
  
  with open("data.json", "w") as f:
    json.dump(data, f)
  with open("rating.txt", "w") as f:
    f.write(output())