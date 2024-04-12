import os
import time
from version_2.webscraper import webscraper
import pandas as pd

bigten = {'illinois'}

for i in range (2015,2025):
    for team in bigten:
        webscraper('illinois', i)
        time.sleep(1)