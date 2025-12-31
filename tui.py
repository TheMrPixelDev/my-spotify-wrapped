from textual.app import App, ComposeResult
from textual.widgets import DataTable, Static, Label, Sparkline
from textual.containers import Vertical
from analysis import top_10_artists_by_count_streams, top_10_songs_by_count_streams, top_10_spent_time_on_artist, top_10_spent_time_on_song, amount_streams_for_each_day

class WrappedApp(App):
    
    def compose(self) -> ComposeResult:
        yield StatisticsTable(["Artists", "Streams"], [(idx[0], val) for idx, val in top_10_artists_by_count_streams.items()], "Top 10 artists by count of individual streams") # type: ignore
        yield StatisticsTable(["Song", "Streams"], [(idx[0], val) for idx, val in top_10_songs_by_count_streams.items()], "Top 10 songs by count of streams") # type: ignore
        yield StatisticsTable(["Artist", "Time in hours"], [(idx[0], val) for idx, val in top_10_spent_time_on_artist.items()], "Top 10 artists by playback time") # type: ignore
        yield StatisticsTable(["Song", "Time in hours"], [(idx[0], val) for idx, val in top_10_spent_time_on_song.items()], "Top 10 songs by playback time") # type: ignore
        yield StatisticsTable(["Artist", "Time in hours"], [(idx[0], val) for idx, val in top_10_spent_time_on_artist.items()], "Top 10 artists by playback time") # type: ignore
        yield Sparkline(list(amount_streams_for_each_day.values))
        
class StatisticsTable(Static):
    
    def __init__(self, columns: list[str], values: list[tuple], title: str):
        super().__init__()
        self.columns = columns
        self.values = values
        self.title = title
    
    def compose(self) -> ComposeResult:
        with Vertical() as v:
            v.styles.padding = 3
            yield FancyLabel(title=self.title)
            table: DataTable = DataTable(name="Hello World")
            table.styles.height = "auto"
            yield table    
        
    def on_mount(self) -> None:
        table: DataTable = self.query(DataTable).first()
        table.add_columns(*self.columns)
        table.add_rows(self.values)
        
class FancyLabel(Static):
    
    def __init__(self, title: str):
        super().__init__(title)
        self.title = title
        self.styles.color = "pink"
        self.styles.padding = (0, 0, 1, 0)
        
    def compose(self) -> ComposeResult:
        yield Label(f"## [bold]{self.title}[/bold] ##")
        
if __name__ == "__main__":
    app = WrappedApp()
    app.run()