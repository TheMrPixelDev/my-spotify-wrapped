"""Main module"""
import json
from typing import List
import argparse
from argparse import Namespace
from html_components import HTMLFile, HTMLHeadline
from data_parser import parse_artists, parse_playtime, parse_songs, parse_dates


DATA_PATH: str
OUTPUT_PATH: str


def init_arguments() -> None:
    """Function initializing the arguments of the script"""
    parser = argparse.ArgumentParser(
        prog="My Spotify Wrapped",
        description="A script which visualizes the exported data from you Spotify-Account."
    )

    parser.add_argument("-d", "--data_path", required=True)
    parser.add_argument("-s", "--out_path", required=True)

    args: Namespace = parser.parse_args()

    global DATA_PATH
    global OUTPUT_PATH
    DATA_PATH = args.data_path
    OUTPUT_PATH = args.out_path


def main() -> None:
    """Main function (execution starts here)"""
    with open(DATA_PATH, "r", encoding="UTF-8") as j_file:
        streams = json.loads(j_file.read())

        artists: List[str] = []
        songs: List[str] = []
        playtimes: List[int] = []
        playdays: List[str] = []

        for stream in streams:
            artists.append(stream["artistName"])
            songs.append(stream["trackName"])
            playtimes.append(stream["msPlayed"])
            playdays.append(stream["endTime"])

        final_html_file = HTMLFile(title="Spotify Statistics")
        final_html_file.add_component(HTMLHeadline("MY SPOTIFY WRAPPED", level=1))

        #####################
        # Analyzing artists #
        #####################
        artists_container = parse_artists(artists)
        final_html_file.add_component(artists_container)

        ###################
        # Analyzing songs #
        ###################
        songs_container = parse_songs(songs)
        final_html_file.add_component(songs_container)

        ######################
        # Analyzing playtime #
        ######################
        playtime_container = parse_playtime(playtimes)
        final_html_file.add_component(playtime_container)

        ######################
        # Analyzing playdays #
        ######################
        playdays_container = parse_dates(playdays, path=OUTPUT_PATH)
        final_html_file.add_component(playdays_container)

        with open(OUTPUT_PATH + "/spotify_stats.html", "w", encoding="UTF-8") as html_file:
            html_file.write(str(final_html_file))
            print(f"Successfully wrote stats to file ({OUTPUT_PATH})")

        with open(OUTPUT_PATH + "/style.css", "w", encoding="UTF-8") as css_file:
            css_file.write(
                """
                .container{border-radius:5px;border:2px solid black;margin:1rem;display:flex;
                flex-direction:column;background-color:rgba(255,255,255,0.1);}h1{margin:3rem;text-decoration:underline;
                text-decoration-style:dotted;text-align:center;}h2{margin:1rem;padding:1rem;
                background-color:rgb(157,250,217);
                border-radius:10px;color:black;}p{margin:1rem;}body{max-width:800px;margin: 0 auto;
                font-family:system-ui,-apple-system,BlinkMacSystemFont,'SegoeUI',Roboto,Oxygen,Ubuntu,Cantarell,
                'OpenSans',
                'HelveticaNeue',sans-serif;background-color:rgba(0,0,0,0.9);color:beige;}table{margin:1rem;}
                td{text-align:center;}
                """
            )


if __name__ == "__main__":
    init_arguments()
    main()
