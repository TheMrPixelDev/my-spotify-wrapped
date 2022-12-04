from html_renderer import HTMLContainer, HTMLHeadline, HTMLParagraph, HTMLTable, HTMLiFrame
import datetime
import plotly.express as px
from pandas import DataFrame

def parse_artists(artists: list, count_of_top_artists=10, count_of_least_streamed_artists=10) -> HTMLContainer:
    unique_artists = list(set(artists))
    count_of_artists = []
    
    for artist in unique_artists:
        count_of_artists.append([
            artist, artists.count(artist)
        ])

    count_of_artists.sort(reverse=True, key=(lambda a: a[1]))

    artist_container = HTMLContainer()

    # Generating table with top artists
    top_artists_table = HTMLTable(["Artist", "Total Streams"])
    for i in range(0, count_of_top_artists + 1):
        top_artists_table.add_row(count_of_artists[i])
    artist_container.add_component(HTMLHeadline(f"Top {count_of_top_artists} Streamed Artists 👩‍🎨", level=2))
    artist_container.add_component(top_artists_table)
    # Adding amount of artists which have been streamed
    artist_container.add_component(HTMLParagraph(f"You have streamed <strong>{len(count_of_artists)}</strong> different artists and clicked the play button <strong>{len(artists)}</strong> times."))
    
    least_streamed_artists_table = HTMLTable(["Artist", "Total Streams"])
    for i in range(1, count_of_least_streamed_artists + 2):
        least_streamed_artists_table.add_row(count_of_artists[-i])
    artist_container.add_component(HTMLHeadline(f"{count_of_least_streamed_artists} Least Streamed Artists", level=2))
    artist_container.add_component(least_streamed_artists_table)

    return artist_container
    
def parse_songs(songs: list, count_of_top_songs=10) -> HTMLContainer:
    unique_songs = list(set(songs))
    count_of_songs = []
    for song in unique_songs:
        count_of_songs.append([
            song, songs.count(song)
        ])

    count_of_songs.sort(reverse=True, key=(lambda a: a[1]))

    songs_container = HTMLContainer()

    top_songs_table = HTMLTable(["Song", "Total Streams"])
    for i in range(0, count_of_top_songs + 1):
        top_songs_table.add_row(count_of_songs[i])
    songs_container.add_component(HTMLHeadline(f"Top {count_of_top_songs} Streamed Songs 🎵", level=2))
    songs_container.add_component(top_songs_table)
    
    amount_of_songs = len(count_of_songs)
    sum_of_streams = 0
    for song in count_of_songs:
        sum_of_streams += song[1]
    songs_container.add_component(HTMLParagraph(f"In average you listened to an individual song <strong>{round(sum_of_streams/amount_of_songs)}</strong> time(s)."))
    
    return songs_container

def parse_playtime(playtimes: list) -> HTMLContainer:
    total_playtime = 0
    for playtime in playtimes:
        total_playtime += playtime / 1000

    playtime_container = HTMLContainer()
    
    playtime_container.add_component(HTMLHeadline("Your Playtime ⌚", level=2))
    average_playtime_per_stream = round(total_playtime / len(playtimes) / 60, ndigits=2)
    playtime_container.add_component(HTMLParagraph(f"Your average stream time per song streamed is <strong>{average_playtime_per_stream} minutes</strong>."))
    playtime_container.add_component(HTMLParagraph(f"Additionally your longest stream took you about <strong>{round(max(playtimes) / 1000 / 60, ndigits=2)} minute(s)</strong> while your shortest stream was just <strong>{round(min(playtimes) / 1000 / 60, ndigits=4)}</strong> minute(s) long."))
    
    return playtime_container

def parse_playdays(playdates: list, path: str) -> HTMLContainer:
    dates = list(map(lambda datetime: datetime.split(" ")[0], playdates))
    unique_dates = list(set(dates))
    days_streamed = len(unique_dates)
    
    # [ [date, count] ]
    plays_per_day = []
    streams_per_day = []
    for date in unique_dates:
        streams = dates.count(date)
        plays_per_day.append([
            date, streams
        ])
        streams_per_day.append(streams)

    plays_per_day.sort(key=(lambda date: date[1]))
    plays_per_day.reverse()

    playdates_table = HTMLTable(["Date", "Streams"])
    for i in range(0, 11):
        date = datetime.date.fromisoformat(plays_per_day[i][0])
        playdates_table.add_row([
            date.strftime("%A %d %B %Y"),
            plays_per_day[i][1]
        ])

    df = DataFrame(
        dict(
            year = unique_dates,
            streams = streams_per_day
        )
    )

    fig = px.bar(df, x = "year", y = "streams", title="Amount of streams throughout the year")
    fig.write_html(path + "/stream_chart.html")
    
    playdates_container = HTMLContainer()
    playdates_container.add_component(HTMLHeadline("Top 10 Streams per Day", level=2))
    playdates_container.add_component(playdates_table)
    playdates_container.add_component(HTMLiFrame(src="stream_chart.html"))
    playdates_container.add_component(HTMLParagraph(f"You streamed from Spotify on <strong>{days_streamed}</strong> different days. Wow that's about {100 - round(days_streamed / 365, ndigits=2)}% of a year."))


    return playdates_container