import requests
import pandas as pd
import time
import random

BASE_URL = "https://vocadb.net/api/songs"

START_YEAR = 2007
END_YEAR = 2025
ROWS_PER_YEAR = 320
SAMPLES_PER_YEAR = 32
ROWS_PER_SAMPLE = ROWS_PER_YEAR // SAMPLES_PER_YEAR

all_songs = []
seen_ids = set()

for year in range(START_YEAR, END_YEAR + 1):
    after_date = f"{year}-01-01T00:00:00Z"
    before_date = f"{year}-12-31T23:59:59Z"

    count_params = {
        "afterDate": after_date,
        "beforeDate": before_date,
        "songTypes": "Original",
        "getTotalCount": "true",
        "maxResults": 1
    }

    count_resp = requests.get(BASE_URL, params=count_params).json()
    total_available = count_resp.get("totalCount", 0)

    if total_available == 0:
        print(f"Año {year}: sin canciones disponibles, se omite")
        continue

    max_start = max(0, total_available - ROWS_PER_SAMPLE)
    collected_this_year = 0

    for _ in range(SAMPLES_PER_YEAR):
        random_start = random.randint(0, max_start)

        params = {
            "maxResults": ROWS_PER_SAMPLE,
            "start": random_start,
            "afterDate": after_date,
            "beforeDate": before_date,
            "sort": "PublishDate",
            "fields": "Tags",
            "songTypes": "Original"
        }
        resp = requests.get(BASE_URL, params=params)
        data = resp.json()
        items = data.get("items", [])

        for song in items:
            song_id = song.get("id")
            if song_id in seen_ids:
                continue
            seen_ids.add(song_id)

            all_songs.append({
                "id": song_id,
                "name": song.get("defaultName"),
                "artistString": song.get("artistString"),
                "songType": song.get("songType"),
                "publishDate": song.get("publishDate"),
                "lengthSeconds": song.get("lengthSeconds"),
                "favoritedTimes": song.get("favoritedTimes"),
                "ratingScore": song.get("ratingScore"),
                "status": song.get("status"),
            })
            collected_this_year += 1

        time.sleep(0.2)

    print(f"Año {year}: {collected_this_year} canciones ({SAMPLES_PER_YEAR} puntos dispersos, {total_available} disponibles)")

df = pd.DataFrame(all_songs)
df.to_csv("vocadb_songs_disperso.csv", index=False, encoding="utf-8-sig")
print(f"\nListo. {len(df)} filas guardadas en vocadb_songs_disperso.csv")