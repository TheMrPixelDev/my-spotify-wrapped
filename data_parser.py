"""This module parses the given data into virtual html components"""
import datetime
from typing import List, Tuple
import plotly.express as px
from pandas import DataFrame
from html_components import HTMLContainer, HTMLHeadline, HTMLParagraph, HTMLTable, HTMLiFrame
from helper_functions import count_individuals


def parse_artists(artists: list, count_of_top_artists=10, count_of_least_streamed_artists=10) -> HTMLContainer:
    """Parses statistics which are related directly to artists and returns an HTMLContainer-Component"""
    count_of_artists: List[Tuple[str, int]] = count_individuals(artists)
    count_of_artists.sort(reverse=True, key=(lambda a: a[1]))
    artist_container = HTMLContainer()

    # Generating table with top artists
    top_artists_table = HTMLTable(["Artist", "Total Streams"])
    total_streams_of_top_x = 0
    total_amount_of_streams = len(artists)
    for i in range(0, count_of_top_artists + 1):
        top_artists_table.add_row(count_of_artists[i])
        total_streams_of_top_x += count_of_artists[i][1]
    top_x_to_streams_ratio = round(total_streams_of_top_x/total_amount_of_streams*100, ndigits=2)
    
    artist_container.add_component(HTMLHeadline(f"Top {count_of_top_artists} Streamed Artists 👩‍🎨", level=2))
    artist_container.add_component(top_artists_table)
    # Adding amount of artists which have been streamed
    artist_container.add_component(HTMLParagraph(
        f"""
        You have streamed <strong>{len(count_of_artists)}</strong> 
        different artists and clicked the play button <strong>{total_amount_of_streams}</strong> times.
        This means that in average you streamed every single artist <strong>{round(len(artists)/len(count_of_artists) ,ndigits=2)}</strong> time(s).
        The streams you generated listening to your top {count_of_top_artists} most listened artists take up <strong>{top_x_to_streams_ratio}%
        </strong> of your total streams.
        """
    ))

    least_streamed_artists_table = HTMLTable(["Artist", "Total Streams"])
    for i in range(1, count_of_least_streamed_artists + 2):
        least_streamed_artists_table.add_row(count_of_artists[-i])
    artist_container.add_component(HTMLHeadline(f"{count_of_least_streamed_artists} Least Streamed Artists", level=2))
    artist_container.add_component(least_streamed_artists_table)

    return artist_container


def parse_songs(songs: List, count_of_top_songs=10) -> HTMLContainer:
    """Parses statistics which are related directly to songs and returns an HTMLContainer-Component"""
    count_of_songs: List[Tuple[str, int]] = count_individuals(songs)
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
    songs_container.add_component(HTMLParagraph(
        f"""
        In average you listened to an individual song 
        <strong>{round(sum_of_streams / amount_of_songs)}</strong> time(s).
        """
    ))

    return songs_container


def parse_playtime(times: List) -> HTMLContainer:
    """Parses statistics which are related directly to playtime of the user and returns an HTMLContainer-Component"""
    total_playtime = 0
    for playtime in times:
        total_playtime += playtime / 1000

    playtime_container = HTMLContainer()

    playtime_container.add_component(HTMLHeadline("Your Playtime ⌚", level=2))
    average_playtime_per_stream = round(total_playtime / len(times) / 60, ndigits=2)
    playtime_container.add_component(HTMLParagraph(
        f"Your average stream time per song streamed is <strong>{average_playtime_per_stream} minutes</strong>."))
    playtime_container.add_component(HTMLParagraph(
        f"""
        Additionally your longest stream took you about <strong>{round(max(times) / 1000 / 60, ndigits=2)} 
        minute(s)</strong> while your shortest stream was just <strong>{round(min(times) / 1000 / 60, ndigits=4)}
        </strong> minute(s) long.
        """
    ))

    return playtime_container


def parse_dates(dates: list, path: str) -> HTMLContainer:
    """
    Parses statistics which are related directly to dates the user
    listen to music and returns an HTMLContainer-Component
    """
    dates = list(map(lambda dt: dt.split(" ")[0], dates))
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

    plays_per_day.sort(key=(lambda d: d[1]))
    plays_per_day.reverse()

    dates_table = HTMLTable(["Date", "Streams"])
    for i in range(0, 11):
        date = datetime.date.fromisoformat(plays_per_day[i][0])
        dates_table.add_row((
            date.strftime("%A %d %B %Y"),
            plays_per_day[i][1]
        ))

    streams_in_year = DataFrame(
        dict(
            year=unique_dates,
            streams=streams_per_day
        )
    )

    fig = px.bar(streams_in_year, x="year", y="streams", title="Amount of streams throughout the year")
    fig.write_html(path + "/stream_chart.html")

    dates_container = HTMLContainer()
    dates_container.add_component(HTMLHeadline("Top 10 Streams per Day", level=2))
    dates_container.add_component(dates_table)
    dates_container.add_component(HTMLiFrame(src="stream_chart.html"))
    dates_container.add_component(HTMLParagraph(
        f"""
        You streamed from Spotify on <strong>{days_streamed}</strong> different days. Wow that's about 
        {100 - round(days_streamed / 365, ndigits=2)}% of a year.
        """
    ))

    return dates_container
