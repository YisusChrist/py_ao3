from pathlib import Path
from typing import Any

from rich.table import Table
from textual.app import App, ComposeResult
from textual.containers import Grid, Horizontal
from textual.screen import ModalScreen
from textual.widgets import (Button, Footer, Header, Input, Label, RichLog,
                             Select)

from py_ao3.consts import AUTHOR, CSS_PATH, GITHUB
from py_ao3.consts import __desc__ as DESC
from py_ao3.consts import __version__ as VERSION
from py_ao3.file_parse import extract_stories, get_file_path
from py_ao3.report import (
    count_frequencies,
    print_top_table,
    print_top_table_stories,
    print_histogram,
)


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
    CSS_PATH = CSS_PATH  # Link to the CSS file
    BINDINGS = [
        ("q", "request_quit", "Quit"),
        ("t", "app.toggle_dark", "Toggle Dark mode"),
    ]

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
            Button(label="About", id="about"),
            Button(label="Quit", id="quit", classes="quit-button"),
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
            Input(
                id="rows",
                placeholder="Enter number of rows (default 100)",
                type="number",
            ),
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

        report_type = self.query_one(Select).value
        output_widget: RichLog = self.query_one(RichLog)

        rows_input: str = self.query_one(Input).value
        top_n: int = int(rows_input) if rows_input else 100

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
        table: Table = print_top_table(data, title, top)
        self.query_one(RichLog).write(table)

    def print_top_table_stories(
        self, stories: list[dict[str, Any]], sort: str = "rating", top: int = 10
    ) -> None:
        table: Table = print_top_table_stories(stories, sort, top)
        self.query_one(RichLog).write(table)

    def show_about_dialog(self) -> None:
        """Action to display the about dialog."""
        self.push_screen(AboutDialog())

    def action_request_quit(self) -> None:
        """Action to display the quit dialog."""
        self.push_screen(QuitScreen())
