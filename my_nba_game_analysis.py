import csv
import re

def find_all_players(play_by_play_moves):  
    all_players = []
    for event in play_by_play_moves:
        name_pattern = re.compile(r'\w\. \w+', re.I)
        name = name_pattern.search(event[7])
        if name:
            all_players.append(name.group(0))
    
    all_players = list(set(all_players))
    return all_players

# Part I

def analyse_nba_game(play_by_play_moves):      
      
    all_players_data = []
    hteam = []
    ateam = []
    all_data = {"home_team": {"name": '', "players_data": hteam}, "away_team": {"name": '', "players_data": ateam}}

    for player in all_players:
        players_data = {"player_name": '', "FG": 0, "FGA": 0, "FG%": 0, "3P": 0, "3PA": 0, "3P%": 0, "FT": 0, "FTA": 0,
                        "FT%": 0, "ORB": 0, "DRB": 0, "TRB": 0, "AST": 0, "STL": 0, "BLK": 0, "TOV": 0, "PF": 0, "PTS": 0}
        players_data["player_name"] = player

        for event in play_by_play_moves:
            fg = fg_pattern.search(event[7])
            if fg:
                if fg.group(1) == player:
                    players_data['FGA'] += 1
                    if fg.group().find('3') != -1:
                        players_data['3PA'] += 1
                        if fg.group().find('makes') != -1:
                            players_data['FG'] += 1
                            players_data['3P'] += 1
                            players_data['PTS'] += 3
                    elif fg.group().find('makes') != -1:
                        players_data['FG'] += 1
                        players_data['PTS'] += 2

            ft = ft_pattern.search(event[7])
            if ft:
                if ft.group(1) == player:
                    players_data['FT'] += 1
                    players_data['PTS'] += 1

            fta = fta_pattern.search(event[7])
            if fta:
                if fta.group(1) == player:
                    players_data['FTA'] += 1

            orb = orb_pattern.search(event[7])
            if orb:
                if orb.group(1) == player:
                    players_data['ORB'] += 1

            drb = drb_pattern.search(event[7])
            if drb:
                if drb.group(1) == player:
                    players_data['DRB'] += 1

            ast = ast_pattern.search(event[7])
            if ast:
                if ast.group(1) == player:
                    players_data['AST'] += 1

            stl = stl_pattern.search(event[7])
            if stl:
                if stl.group(1) == player:
                    players_data['STL'] += 1

            tov = tov_pattern.search(event[7])
            if tov:
                if tov.group(1) == player:
                    players_data['TOV'] += 1

            pf = pf_pattern.search(event[7])
            if pf:
                if pf.group(1) == player:
                    players_data['PF'] += 1

            blk = blk_pattern.search(event[7])
            if blk:
                if blk.group(1) == player:
                    players_data['BLK'] += 1
            
            players_data['TRB'] = players_data['DRB'] + players_data['ORB']
            if players_data['FTA'] == 0:
                players_data['FT%'] = 0
            else:
                players_data['FT%'] = int(players_data['FT']/players_data['FTA']*1000)/1000
            
            if players_data['3PA'] == 0:
                players_data['3P%'] = 0
            else:
                players_data['3P%'] = int(players_data['3P']/players_data['3PA']*1000)/1000
                
            if players_data['FGA'] == 0:
                players_data['FG%'] = 0
            else:
                players_data['FG%'] = int(players_data['FG']/players_data['FGA']*1000)/1000

        all_players_data.append(players_data)
        
    for event in play_by_play_moves:
        all_data['home_team']['name'] = event[4]
        all_data['away_team']['name'] = event[3]
        misses = misses_pattern.search(event[7])
        drb = drb_pattern.search(event[7])
        
        for player_data in all_players_data:
            
            if misses:
                if misses.group(1) == player_data['player_name'] and all_data['home_team']['name'] == event[2]:
                    if player_data not in hteam: 
                        hteam.append(player_data)
                elif misses.group(1) == player_data['player_name'] and all_data['away_team']['name'] == event[2]:
                    if player_data not in ateam:
                        ateam.append(player_data)

            if drb:
                if drb.group(1) == player_data['player_name'] and all_data['home_team']['name'] == event[2]:
                    if player_data not in hteam:
                        hteam.append(player_data)
                elif drb.group(1) == player_data['player_name'] and all_data['away_team']['name'] == event[2]:
                    if player_data not in ateam:
                        ateam.append(player_data)
                
    return all_data

# Part II

def print_nba_game_stats(team_dict):
    header = list(team_dict['home_team']['players_data'][0].keys())
    stats = ['\t'.join(header)]
    columns_sum = []
    total_row = ['Team totals']
    print('\n Please enter "h" to print home team stats or "a" to print away team stats:')
    a = input()
    if a == 'h':
        for row in team_dict['home_team']['players_data']:
            stats.append('\t'.join(str(elem) for elem in list(row.values())))
            columns_sum.append(list(row.values())[1:])
        total_row.append('\t'.join(str(j) for j in [sum(elem[i] for elem in columns_sum) for i in range(len(columns_sum[0]))]))
        stats.append('\t'.join(str(j) for j in total_row))
        last_row = stats[-1].split('\t')
        last_row[3] = str(int(int(last_row[1])/int(last_row[2])*1000)/1000)
        last_row[6] = str(int(int(last_row[4])/int(last_row[5])*1000)/1000)
        last_row[9] = str(int(int(last_row[7])/int(last_row[8])*1000)/1000)
        stats[-1] = ('\t'.join(last_row))
        return '\n'.join(stats)
    elif a == 'a':
        for row in team_dict['away_team']['players_data']:
            stats.append('\t'.join(str(elem) for elem in list(row.values())))
            columns_sum.append(list(row.values())[1:])
        total_row.append('\t'.join(str(j) for j in [sum(elem[i] for elem in columns_sum) for i in range(len(columns_sum[0]))]))
        stats.append('\t'.join(str(j) for j in total_row))
        last_row = stats[-1].split('\t')
        last_row[3] = str(int(int(last_row[1])/int(last_row[2])*1000)/1000)
        last_row[6] = str(int(int(last_row[4])/int(last_row[5])*1000)/1000)
        last_row[9] = str(int(int(last_row[7])/int(last_row[8])*1000)/1000)
        stats[-1] = ('\t'.join(last_row))
        return '\n'.join(stats)
    else:
        print('Wrong input! Please enter "a" or "h"')
        
        print_nba_game_stats(team_dict)

if __name__ == "__main__":
    with open('nba_game_blazers_lakers_20181018.txt') as myFile:
        reader = csv.reader(myFile, delimiter = '|')
        play_by_play_moves = [each for each in reader]

    fg_pattern = re.compile(r'(\w\. \w+) (makes|misses)\s\d-pt', re.I)
    ft_pattern = re.compile(r'(\w\. \w+) makes free throw', re.I)
    fta_pattern = re.compile(r'(\w\. \w+) (makes|misses) free throw', re.I)
    orb_pattern = re.compile(r'Offensive rebound by (\w\. \w+)', re.I)
    drb_pattern = re.compile(r'Defensive rebound by (\w\. \w+)', re.I)
    ast_pattern = re.compile(r'assist by (\w\. \w+)', re.I)
    stl_pattern = re.compile(r'steal by (\w\. \w+)', re.I)
    tov_pattern = re.compile(r'Turnover by (\w\. \w+)', re.I)
    pf_pattern = re.compile(r'foul by (\w\. \w+)', re.I)
    blk_pattern = re.compile(r'block by (\w\. \w+)', re.I)
    misses_pattern = re.compile(r'(\w\. \w+) misses', re.I)
    
    all_players = find_all_players(play_by_play_moves)
    team_dict = analyse_nba_game(play_by_play_moves)

    print(team_dict)
    print(print_nba_game_stats(team_dict))