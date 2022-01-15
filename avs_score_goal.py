import requests
from datetime import datetime
import time
import os

starting_score = 0

while True:


    # This gets the date and schedule for today
    start_date = datetime.now()
    today = start_date.strftime("%Y-%m-%d")

    avs_score = requests.get("https://statsapi.web.nhl.com/api/v1/schedule?teamId=21&startDate=" + today + "&endDate=" + today)
    score = avs_score.json()


    # This gets the player id's and checks for goal scoring
    avs_players_info = requests.get("https://statsapi.web.nhl.com/api/v1/teams/21?expand=team.roster")
    player_info = avs_players_info.json()
    game_id = score['dates'][0]['games'][0]['gamePk']
    avs_stats = requests.get("https://statsapi.web.nhl.com/api/v1/game/" + str(game_id) + "/boxscore") # 2021020591 (<<<Blackhawks vs Avs Game ID, use to see stats from past game)
    stats = avs_stats.json()

    def home_away():
        if stats['teams']['home']['team']['name'] == "Colorado Avalanche":
            return "home"
        else:
            return "away"

    def player_loop():
        for x in range(0,len(player_info['teams'][0]['roster']['roster'])):
            player_id = player_info['teams'][0]['roster']['roster'][x]['person']['id']
            id_string = "ID" + str(player_id)
            if id_string in stats['teams'][home_away()]['players']:
                if stats['teams'][home_away()]['players'][id_string]['stats'] != {}:
                    player_name = stats['teams'][home_away()]['players'][id_string]['person']['fullName']
                    if player_name == "Pavel Francouz" or player_name == "Darcy Kuemper":
                        pass
                    else:
                        player_goal = stats['teams'][home_away()]['players'][id_string]['stats']['skaterStats']['goals']
                        print(id_string)
                        print(player_name + ": " + str(player_goal))


    # Need to figure out how to return name of goal scorer




    player_loop()



    # This determines when we score and runs a program
    home_team_name = score['dates'][0]['games'][0]['teams']['home']['team']['name']
    away_team_name = score['dates'][0]['games'][0]['teams']['away']['team']['name']
    home_team_score = score['dates'][0]['games'][0]['teams']['home']['score']
    away_team_score = score['dates'][0]['games'][0]['teams']['away']['score']


    if home_team_name == "Colorado Avalanche" and home_team_score != starting_score:
        print("AVS GOAL! Scored by ")
        os.system("afplay avs_goal_horn.wav&")
        print("New Score!!\nColorado Avalanche: " + str(home_team_score) + "\n" + away_team_name + ": " + str(away_team_score))
        starting_score = home_team_score
    elif away_team_name == "Colorado Avalanche" and away_team_score != starting_score:
        print("AVS GOAL!")
        os.system("afplay avs_goal_horn.wav&")
        print("New Score!!\nColorado Avalanche: " + str(away_team_score) + "\n" + home_team_name + ": " + str(home_team_score))
        starting_score = away_team_score


    time.sleep(30)





# if the avs score changes
#     Say "AVS GOAL" --done
#     Say who scored the goal --Need Help
#     Play Music --done
#     Show the new score --done
