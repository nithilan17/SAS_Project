from bs4 import BeautifulSoup
import requests 
import pandas as pd
import os 

def webscraper(school, year):
    roster = f"https://www.sports-reference.com/cbb/schools/{school}/men/{year}.html#all_roster"
    result = requests.get(roster)
    content = result.text
    year_abr2 = year%2000 
    year_abr = year_abr2 -1
    year_str = str(year_abr) + "_" + str(year_abr2)

    soup = BeautifulSoup(content, 'lxml')
    table = soup.find('table', class_= 'sortable stats_table')

    players_list = []

    # Iterate over each table row
    for row in table.find_all('tr')[1:]:  # Skip the first row (header row)
        columns1 = row.find_all('th')
        columns2 = row.find_all('td')

        player = columns1[0].text.strip()  # Player's name
        hometown = columns2[5].text.strip()  # Player's hometown
        high_school = columns2[6].text.strip()  # Player's high school
        
        players_list.append({
            'Player': player,
            'Hometown': hometown,
            'High School': high_school
        })

    df = pd.DataFrame(players_list)

    df[['City', 'State']] = df['Hometown'].str.extract(r'([A-Za-z\s]+),\s([A-Za-z.]+)')
    df.drop(columns=['Hometown'], inplace=True)

    df['High School'] = df['High School'].str.split(';').str[-1].str.strip()
    csv_folder = "csv_files"
    year_folder = year_str

    if not os.path.exists(csv_folder):
        os.makedirs(csv_folder)

    year_path = os.path.join(csv_folder, year_folder)
    if not os.path.exists(year_path):
        os.makedirs(year_path)

    df.to_csv(os.path.join(year_path, f'{school}_{year_str}.csv'), index=False)
    print(f'{school} csv uploaded!')
    return df
