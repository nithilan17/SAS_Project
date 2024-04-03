from webscraper import webscraper

#1) name of the college
#2) url including the grid view
#3) tag of the box of the player data
#4) class of the box of the player data
#5) player specifier tag
#6) class of the player name
#7) class of the player year
#8) class of the player hometown
#9) year roster (ex: 23_24)

webscraper('illinois','https://fightingillini.com/sports/mens-basketball/roster/2023-24?view=2',
           'table', "sidearm-table sidearm-table-grid-template-1 sidearm-table-grid-template-1-breakdown-large",
           'tr', 'sidearm-table-player-name','roster_class','hometownhighschool','23_24')

webscraper('wisconsin','https://uwbadgers.com/sports/mens-basketball/roster?view=2',
           'table', "sidearm-table sidearm-table-grid-template-1 sidearm-table-grid-template-1-breakdown-large",
           'tr', 'sidearm-table-player-name','roster_class','player_hometown','23_24')