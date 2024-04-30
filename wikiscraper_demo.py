from bs4 import BeautifulSoup 
import requests 
import pandas as pd
import os 
import time

def wikiscraper(team_name, year_int):
    '''This wikiscraper takes the team name string and year integer and returns a list of that team's men's basketball roster for that year'''
    # team ex: "Illinois Fighting Illini"
    # year_int ex: 2024
    team = team_name.replace(" ", "_")
    year = str(year_int-1) + "-" + str(year_int%2000)
    # csv_folder = "csv_files"
    # year_path = os.path.join(csv_folder, year)
    # csv_file_path = os.path.join(year_path, f'{team}_{year}.csv')

    # if os.path.exists(csv_file_path):
    #     return
    try: 
        roster = f"https://en.wikipedia.org/wiki/{year}_{team}_men%27s_basketball_team"
        result = requests.get(roster)
        if(result.status_code == 404):
            roster = f"https://en.wikipedia.org/wiki/{year}_{team}_basketball_team"
            result = requests.get(roster)
            if(result.status_code == 404):
                print('error ' + team_name + " " + year)
                return
        content = result.text

        soup = BeautifulSoup(content, 'lxml')
        table = soup.find('table', class_= 'toccolours')
        table = table.find('table', class_='sortable')

        player_data = []

        rows = table.find_all('tr')
        for row in rows[1:]:
            cells = row.find_all('td')
            name = cells[2].text.strip().replace('\xa0(W)', '').split('(')[0].strip().split('[')[0].strip()
            try:
                hometown = cells[7].text.strip()
            except:
                hometown = cells[6].text.strip()
            player_data.append({'Team': team_name, 'Year': year_int, 'Name': name, 'Hometown': hometown})
    except:
        print("error thrown for " + team_name + " " + year)
        return

    # if not os.path.exists(csv_folder):
    #     os.makedirs(csv_folder)

    # if not os.path.exists(year_path):
    #     os.makedirs(year_path)

    # df.to_csv(csv_file_path, index=False)
    print(f'{team_name} CSV uploaded!')
    time.sleep(2)
    return player_data

# Take a team
teams = {"UAB Blazers"}
team_data = []
for team in teams:
    # for the sake of testing, we will just take data for 3 years
    for year in range (2024,2020,-1):
        # wikiscraper(team,year)
        team_data.extend(wikiscraper(team, year))

df = pd.DataFrame(team_data)
df.to_csv('Teams_Data.csv', index=False)

# will take like 11 minutes to run. to prevent getting blocked from the server