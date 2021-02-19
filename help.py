_commands = [
    {"cmd": "help", "usage": "help", "arg_count": 0, "description": "Outputs list of available commands. Use help [command] to get the command description"},
    {"cmd": "displayrating", "usage": "displayrating", "arg_count": 0, "description": "Displays player rankings"},
    {"cmd": "exportrating", "usage": "exportrating", "arg_count": 0, "description": "Exports player rankings to a text file"},
    {"cmd": "matchups", "usage": "matchups [player]", "arg_count": 1, "description": "Displays the matchups of a given player"},
    {"cmd": "setmatchups", "usage": "setmatchups [player1] [player2] [wins] [losses] [draws]", "arg_count": 5, "description": "Manually overwrite the matchup data of the two players"},
    {"cmd": "aftermatch", "usage": "aftermatch [player1] [player2] [w/l/d]", "arg_count": 3, "description": "Saves the match results (rating, stats, matchup)"},
    {"cmd": "remove", "usage": "remove [player]", "arg_count": 1, "description": "Removes the player from the database. Results of other players' matches against removed player are preserved"},
    {"cmd": "merge", "usage": "merge [departure_player] [destination_player]", "arg_count": 2, "description": "Appends one player's stats to another's and removes the former"},
    {"cmd": "undo", "usage": "undo", "arg_count": 0, "description": "Removes the effects of the last command executed. Only one consequent undo is allowed"},
    {"cmd": "deactivate", "usage": "deactivate [player]", "arg_count": 1, "description": "Hides the player from the rating table. Useful when the player (temporary) leaves the league. Rating, stats, and matchups are preserved"},
    {"cmd": "reactivate", "usage": "reactivate [player]", "arg_count": 1, "description": "Returns the player to the rating table"}
]

def _find_cmd_info(cmd):
    for cmd_i in _commands:
        if cmd_i["cmd"] == cmd:
            return cmd_i
    return None

def get_cmd_list():
    return map(lambda info: info["cmd"], _commands)

def get_usage(cmd):
    return "Usage: " + _find_cmd_info(cmd)["usage"]

def get_arg_count(cmd):
    return _find_cmd_info(cmd)["arg_count"]

def print_help():
    for cmd_info in _commands:
        print(cmd_info["usage"] + " - " + cmd_info["description"])

def print_cmd_help(cmd):
    cmd_info = _find_cmd_info(cmd)
    print(cmd_info["cmd"])
    print(cmd_info["description"])
    print("Usage: " + cmd_info["usage"])