import urllib
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import requests
import datetime
import pygsheets


def url_ok(url):
    try:
        r = requests.head(url)
        if r:
            return True
    except Exception as ex:
        return False

# define the scope
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

gc = pygsheets.authorize(service_file='Covid SOS-05c234b81737.json')
ss = gc.open("Sheets")
sheet_instance = ss[0]

x = datetime.datetime.now()
time_ = str(x).split('.')[0]

# url = "http://covidhelpnagpur.in/"

url = "https://nsscdcl.org/covidbeds/"
website_is_up = url_ok(url)

if website_is_up:
    html = urlopen(url).read()
    soup = BeautifulSoup(html)

    for script in soup(["script", "style"]):
        script.decompose()

    strips = list(soup.stripped_strings)

    if 'Asst Commissioner' in strips:
        idx = strips.index('Asst Commissioner')
        O2_Beds = strips[idx:idx + 5:2]
        Non_O2_Beds = strips[idx + 5:idx + 10:2]
        ICU_Beds = strips[idx + 10:idx + 15:2]
        Ventilators = strips[idx + 15:idx + 20:2]

        data = [O2_Beds, Non_O2_Beds, ICU_Beds, Ventilators]
        last_updated = [time_, time_, time_, time_]
        df = pd.DataFrame(data, columns=['Type', 'Available', 'Occupied'])
        df['Last Updated'] = last_updated
        print(df)
        sheet_instance.set_dataframe(df, (1, 1))

else:
    print('No data retrieved')
