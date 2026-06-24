from bs4 import BeautifulSoup
import pandas as pd
import requests

BASE_URL = "https://www.google.com/search?q="


HEADERS = headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/137.0.0.0 Safari/537.36"
    ),
    "Accept": (
        "text/html,application/xhtml+xml,application/xml;q=0.9,"
        "image/avif,image/webp,image/apng,*/*;q=0.8"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Cache-Control": "max-age=0"
}

def get_coordinates(sector):
    search_term = f"sector {sector} gurgaon longitude & latitude"
    response = requests.get(BASE_URL + search_term, headers=HEADERS)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        coordinates_div = soup.find("div", class_="z0LcW t2b5cf")
        if coordinates_div:
            return coordinates_div.text
    return None


df = pd.DataFrame(columns=["Sector", "Coordinates"])

for sector in range(1,116):
    coordinates = get_coordinates(sector)
    df = df.append({"Sector":f"Sector {sector}", "Coordinates":coordinates}, ignore_index=True)

df.to_csv("gurgaon_sectors_coordinates.csv", index=False)