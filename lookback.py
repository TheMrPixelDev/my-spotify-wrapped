import json
from prettytable import PrettyTable


print("""
#############################
#  YOUR SPOTIFY STATISTICS  #
#############################
""")

ignored_artists = [
    "Edward Snowden",
    "Ashley Vance"
]

count_of_top_artists = 10
count_of_least_streamed_artists = 10

count_of_top_songs = 10

with open("StreamingHistory0.json", "r") as j_file:
    streams = json.loads(j_file.read())

    artists = []
    songs = []
    playtimes = []
    for stream in streams:
        artists.append(stream["artistName"])
        songs.append(stream["trackName"])
        playtimes.append(stream["msPlayed"])
    
    # Analyzing artists 
    unique_artists = list(set(artists))
    count_of_artists = []
    
    for artist in unique_artists:
        count_of_artists.append([
            artist, artists.count(artist)
        ])

    count_of_artists.sort(reverse=True, key=(lambda a: a[1]))

    top_artists_table = PrettyTable(["Artist", "Total Streams"])
    
    for i in range(0, count_of_top_artists + 1):
        top_artists_table.add_row(count_of_artists[i])

    print(f"Top {count_of_top_artists} streamed artists")
    print(top_artists_table)

    print(f"Amount of artists streamed: {len(count_of_artists)}")
    print(f"Total amount of streams: {len(streams)}")
    
    least_streamed_artists = PrettyTable(["Artist", "Total Streams"])    
    for i in range(1, count_of_least_streamed_artists + 2):
        least_streamed_artists.add_row(count_of_artists[-i])

    print(f"{count_of_least_streamed_artists} Least Streamed Artists")
    print(least_streamed_artists)

    print("===============================================")

    # Analyzing songs
    
    unique_songs = list(set(songs))
    count_of_songs = []
    for song in unique_songs:
        count_of_songs.append([
            song, songs.count(song)
        ])

    count_of_songs.sort(reverse=True, key=(lambda a: a[1]))
    top_songs_table = PrettyTable(["Song", "Total Streams"])
    for i in range(0, count_of_top_songs + 1):
        top_songs_table.add_row(count_of_songs[i])

    print(f"Top {count_of_top_songs} streamed songs")
    print(top_songs_table)

    amount_of_songs = len(count_of_songs)
    sum_of_streams = 0
    for song in count_of_songs:
        sum_of_streams += song[1]
    
    print(f"Average streams per song: {round(sum_of_streams/amount_of_songs)}")

    print("===============================================")

    # Analyzing playtime

    total_playtime = 0
    for playtime in playtimes:
        total_playtime += playtime / 1000
        
    average_playtime_per_stream = round(total_playtime / len(streams) / 60, ndigits=2)
    print(f"Average playtime per stream: {average_playtime_per_stream} minutes")