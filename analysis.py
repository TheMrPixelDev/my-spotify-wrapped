import pandas as pd

YEAR = 2022

df = pd.concat([pd.read_json("./MyData/StreamingHistory0.json"), pd.read_json("./MyData/StreamingHistory1.json")], axis=0) # type: ignore
df = df[df["endTime"].str.startswith(f"{YEAR}")]

# Split the 'endTime' column into 'endDate' and 'endTime'
df[['endDate', 'endTime']] = df['endTime'].str.split(' ', expand=True)

# Convert 'endDate' to datetime.date and 'endTime' to datetime.time
df['endDate'] = pd.to_datetime(df['endDate']).dt.date
df['endTime'] = pd.to_datetime(df['endTime'], format='%H:%M').dt.time

top_10_songs_by_count_streams = df[["artistName", "trackName"]].value_counts()[:10]
top_10_artists_by_count_streams = df[["artistName"]].value_counts()[:10]
top_10_spent_time_on_artist = df[["artistName", "msPlayed"]].groupby("artistName").sum().sort_values("msPlayed", ascending=False).apply(lambda ms: ms/1000/60/60)[:10] # time is given in hours
top_10_spent_time_on_song = df[["trackName", "msPlayed"]].groupby("trackName").sum().sort_values("msPlayed", ascending=False).apply(lambda ms: ms/1000/60/60)[:10] # time is given in hours
top_artist_for_each_day = (
    df.groupby(['endDate', 'artistName']).size().reset_index(name='count').sort_values(['endDate', 'count'], ascending=[True, False])
    .groupby('endDate')
    .head(1)
    .rename(columns={'artistName': 'topArtist', 'count': 'topArtistCount'})
    .reset_index(drop=True)
)
top_10_days_with_most_streams = df[["endDate"]].groupby("endDate")["endDate"].count().sort_values(ascending=False)[:10]
total_time_streamed = df[["msPlayed"]].sum().apply(lambda ms: ms/1000/60/60)["msPlayed"] # time is given in hours
amount_days_streams_occured = df[["endDate"]].nunique() # max is 365
amount_streams_for_each_day = df[["endDate"]].value_counts().sort_index(ascending=True)

print(amount_streams_for_each_day.values)

