import math
import json
import mutator
import writer
import help
import copy
import os.path

significant_commands = ["setmatchups", "aftermatch", "remove", "merge", "deactivate", "reactivate"]
data = {}
prefs = {}

previous_data = None

def undo():
  global data
  global previous_data
  if previous_data == None:
    print("It is possible to undo only one command at a time. Either this rule was violated, or you haven't executed any command yet. Cancelled")
  else:
    data = copy.deepcopy(previous_data)
    previous_data = None
    mutator.dump(data)

    with open("dump.txt", "r") as f:
      lines = f.readlines()
    lines = lines[:-1]
    with open("dump.txt", "w") as f:
      lines = f.writelines(lines)

    print("Undo successful")

def use_command(inp):
  if inp[0] == "displayrating":
    writer.print_table(data, prefs)
  elif inp[0] == "exportrating":
    writer.export_table(data, prefs)
  elif inp[0] == "matchups":
    writer.print_matchups_of_player(data, inp[1].lower())
  elif inp[0] == "setmatchups":
    return mutator.set_matchup(data, inp[1].lower(), inp[2].lower(), int(inp[3]), int(inp[4]), int(inp[5]))
  elif inp[0] == "aftermatch":
    return mutator.save_match_results(data, inp[1].lower(), inp[2].lower(), inp[3].lower(), prefs)
  elif inp[0] == "remove":
    return mutator.remove_player(data, inp[1].lower())
  elif inp[0] == "merge":
    return mutator.merge_players(data, inp[1].lower(), inp[2].lower())
  elif inp[0] == "deactivate":
    return mutator.deactivate_player(data, inp[1].lower())
  elif inp[0] == "reactivate":
    return mutator.reactivate_player(data, inp[1].lower())
  elif inp[0] == "undo":
    undo()
  return True

if not os.path.isfile("prefs.json"):
  prefs = {"calib_games": 12}
  with open("prefs.json", "w") as f:
    json.dump(prefs, f)
else:
  with open("prefs.json", "r") as f:
    prefs = json.load(f)

with open("data.json", "r") as f:
  data = json.load(f)

while True:
  full_input = input()
  inp = full_input.split()
  cmd = inp[0]

  if cmd == "help":
    if len(inp) == 2:
      help.print_cmd_help(inp[1])
    else:
      help.print_help()
  elif not cmd in help.get_cmd_list():
    print("Command not found: " + cmd)
  elif help.get_arg_count(cmd) + 1 != len(inp):
    print(help.get_usage(cmd))
  else:
    if cmd in significant_commands:
      prev_data = copy.deepcopy(data)
    success = use_command(inp)
    if cmd in significant_commands and success:
      with open("dump.txt", "a") as f:
        f.write(full_input + "\n")
      previous_data = prev_data