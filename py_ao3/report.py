from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
from rich.table import Table
from textual.app import App, ComposeResult
from textual.widgets import Button, Footer, Header, Input, RichLog, Select, Label
from textual.containers import Horizontal, Grid
from textual.screen import ModalScreen

from py_ao3.consts import AUTHOR, __desc__ as DESC, GITHUB, __version__ as VERSION
from py_ao3.file_parse import extract_stories, get_file_path


def add_to_frequencies(
    frequencies: dict[str, dict[Any, int]], key: str, value: Any
) -> None:
    if not value:
        return
    if value not in frequencies[key]:
        frequencies[key][value] = 1
    else:
        frequencies[key][value] += 1


def count_frequencies(stories: list[dict[str, Any]]) -> dict[str, dict[Any, int]]:
    frequencies: dict[str, dict[Any, int]] = {
        "ratings": {},
        "characters": {},
        "series": {},
        "authors": {},
    }

    for story in stories:
        # Update ratings count
        add_to_frequencies(frequencies, "ratings", story["rating"])

        if not story["characters"]:
            continue

        # Update characters count
        for character in story["characters"]:
            add_to_frequencies(frequencies, "characters", character)

        if not story["series"]:
            continue

        # Update series count
        add_to_frequencies(frequencies, "series", story["series"])

        # Update the authors count
        add_to_frequencies(frequencies, "authors", story["author"])

    return frequencies


def convert_word_count(word_count: str) -> int:
    word_count = (
        word_count.lower().replace("~", "").replace("-", "").replace("k", "000")
    )
    return int(word_count)


def print_histogram(
    data: dict[Any, int], title: str, height: int = 5, width: int = 10
) -> None:
    plt.figure(figsize=(width, height))
    plt.bar(data.keys(), data.values(), color="skyblue")  # type: ignore
    plt.title(f"Histogram of {title}")
    plt.xlabel(title)
    plt.ylabel("Frequency")
    plt.show()


class QuitScreen(ModalScreen):
    """
    Screen with a dialog to quit.

    Reference: https://www.blog.pythonlibrary.org/2024/02/06/creating-a-modal-dialog-for-your-tuis-in-textual/
    """

    def compose(self) -> ComposeResult:
        yield Grid(
            Label("Are you sure you want to quit?", id="question"),
            Button("Quit", variant="error", id="quit"),
            Button("Cancel", variant="primary", id="cancel"),
            id="dialog",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "quit":
            self.app.exit()
        else:
            self.app.pop_screen()


class AboutDialog(ModalScreen):
    """
    Screen with an 'About' dialog showing application information.
    """

    def compose(self) -> ComposeResult:
        yield Grid(
            Label("About AO3 Report App", id="title", classes="title"),
            Label(DESC, id="desc"),
            Label(f"Version {VERSION}", id="version"),
            Label(f"Author: {AUTHOR}", id="author"),
            Label(f"GitHub: {GITHUB}", id="github"),
            Button("Close", id="close", variant="primary"),
            id="dialog-2",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "close":
            self.app.pop_screen()


class AO3ReportApp(App):
    CSS_PATH = "css/app.css"  # Link to the CSS file
    BINDINGS = [("q", "request_quit", "Quit")]

    def __init__(self):
        super().__init__()
        self.file_path: Path | None = None
        self.stories: list[dict[str, Any]] = []
        self.frequencies: dict[str, dict[Any, int]] = {}

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()

        # Group buttons in a horizontal container
        yield Horizontal(
            Button(label="Select File", id="select_file"),
            Button(label="Generate Report", id="generate_report"),
            Button(label="Quit", id="quit", classes="quit-button"),  # New Quit Button
            Button(label="About", id="about"),  # New About Button
            classes="button-group",  # Apply a CSS class to control layout
        )
        # Group select and input fields in another horizontal container
        yield Horizontal(
            Select(
                id="report_type",
                options=[
                    ("Top Stories by Rating", "rating"),
                    ("Top Stories by Words", "words"),
                    ("Top Characters", "characters"),
                    ("Top Series", "series"),
                    ("Top Authors", "authors"),
                    ("Histogram of Ratings", "hist_ratings"),
                    ("Histogram of Characters", "hist_characters"),
                    ("Histogram of Series", "hist_series"),
                    ("Histogram of Authors", "hist_authors"),
                ],
            ),
            Input(id="rows", placeholder="Enter number of rows (default 100)"),
            classes="input-group",  # Apply a CSS class to control layout
        )

        yield RichLog(id="output")

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id: str | None = event.button.id
        if button_id == "select_file":
            self.file_path = get_file_path()
            if self.file_path:
                self.query_one(RichLog).write(f"Selected File: {self.file_path}")
                self.stories = extract_stories(self.file_path)
                self.frequencies = count_frequencies(self.stories)
        elif button_id == "generate_report":
            await self.generate_report()
        elif button_id == "quit":
            self.action_request_quit()
        elif button_id == "about":
            self.show_about_dialog()

    async def generate_report(self) -> None:
        if not self.file_path:
            self.query_one(RichLog).write("No file selected!")
            return

        self.stories = extract_stories(self.file_path)
        report_type = self.query_one(Select).value
        output_widget: RichLog = self.query_one(RichLog)

        rows_input: str = self.query_one(Input).value
        top_n: int = int(rows_input) if rows_input.isdigit() else 100

        report_type_str = str(report_type)
        if report_type_str == "Select.BLANK":
            output_widget.write(f"Invalid report type: {report_type}")
        elif report_type == "rating":
            output_widget.write("Generating Top Stories by Rating...")
            self.print_top_table_stories(self.stories, sort="rating", top=top_n)
        elif report_type == "words":
            output_widget.write("Generating Top Stories by Words...")
            self.print_top_table_stories(self.stories, sort="words", top=top_n)
        elif (
            report_type == "characters"
            or report_type == "series"
            or report_type == "authors"
        ):
            output_widget.write(f"Generating Top {report_type_str}...")
            self.print_top_table(
                self.frequencies[report_type_str], report_type_str, top=top_n
            )
        elif report_type_str.startswith("hist_"):
            selection: str = report_type_str[5:]
            output_widget.write(f"Generating Histogram of {selection}...")
            data: dict[Any, int] = self.frequencies[selection]
            print_histogram(data, selection)
        else:
            output_widget.write(f"Invalid report type: {report_type}")

    def print_top_table(self, data: dict[str, int], title: str, top: int = 10) -> None:
        sorted_data: list[tuple[str, int]] = sorted(
            data.items(), key=lambda x: x[1], reverse=True
        )
        top_data: list[tuple[str, int]] = sorted_data[:top]
        table = Table()
        table.add_column(title, style="cyan")
        table.add_column("Frequency", style="magenta")
        if title == "authors":
            table.add_column("Author Link", style="yellow")

        for d, frequency in top_data:
            if title == "authors":
                link: str = f"https://archiveofourown.org/users/{d}/pseuds/{d}"
                table.add_row(d, str(frequency), link)
            else:
                table.add_row(d, str(frequency))

        self.query_one(RichLog).write(table)

    def print_top_table_stories(
        self,
        stories: list[dict[str, Any]],
        sort: str = "rating",
        top: int = 10,
    ) -> None:
        sorted_stories: list[dict[str, Any]] = sorted(
            [story for story in stories if story[sort] is not None],
            key=lambda x: convert_word_count(x[sort]) if sort == "words" else x[sort],
            reverse=True,
        )
        top_stories: list[dict[str, Any]] = sorted_stories[:top]
        table = Table()
        table.add_column("Title", style="cyan")
        table.add_column("Rating", style="magenta")
        table.add_column("Author", style="yellow")
        table.add_column("Characters", style="blue")
        table.add_column("Words", style="green")
        for story in top_stories:
            table.add_row(
                story["title"],
                str(story["rating"]),
                story["author"],
                " × ".join(story["characters"]),
                str(story["words"]),
            )

        self.query_one(RichLog).write(table)

    def show_about_dialog(self) -> None:
        """Action to display the about dialog."""
        self.push_screen(AboutDialog())

    def action_request_quit(self) -> None:
        """Action to display the quit dialog."""
        self.push_screen(QuitScreen())
