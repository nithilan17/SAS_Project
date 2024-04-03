from bs4 import BeautifulSoup
import requests 
import pandas as pd
import os 

#1) name of the college
#2) url including the grid view
#3) tag of the box of the player data
#4) class of the box of the player data
#5) player specifier tag
#6) class of the player name
#7) class of the player year
#8) class of the player hometown
#9) year roster (ex: 23_24)

def webscraper(college, url, box_tag, box_class, player_tag, player_name, player_year,player_hometown,year):
    roster = url
    result = requests.get(roster)
    content = result.text

    soup = BeautifulSoup(content, 'lxml')

    box = soup.find(box_tag, class_=box_class)

    players = box.find_all(player_tag)

    player_data = []
    for player in players:
        name = player.find(class_=player_name)
        academic_year_element = player.find(class_=player_year)
        hometown_highschool_element = player.find(class_=player_hometown)
        
        if name and academic_year_element and hometown_highschool_element:
            name = name.text.strip()
            academic_year = academic_year_element.text.strip()
            hometown_highschool = hometown_highschool_element.text.strip()
            
            player_data.append({
                'Name': name,
                'Academic Year': academic_year,
                'Hometown/High School': hometown_highschool
            })

    df = pd.DataFrame(player_data)

    df[['City', 'State']] = df['Hometown/High School'].str.extract(r'([A-Za-z\s]+),\s([A-Za-z.]+)')
    df.drop(columns=['Hometown/High School'], inplace=True)

    folder_name = f'{year}_csv_files'
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    df.to_csv(os.path.join(folder_name, f'{college}_{year}.csv'), index=False)
    print(f'{college} csv uploaded!')
