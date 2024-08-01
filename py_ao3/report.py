from typing import Any

import matplotlib.pyplot as plt
from rich import box
from rich.table import Table


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
        # Update series count
        add_to_frequencies(frequencies, "series", story["series"])
        # Update the authors count
        add_to_frequencies(frequencies, "authors", story["author"])

        if not story["characters"]:
            continue
        # Update characters count
        for character in story["characters"]:
            add_to_frequencies(frequencies, "characters", character)

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


def print_top_table(data: dict[str, int], title: str, top: int) -> Table:
    sorted_data: list[tuple[str, int]] = sorted(
        data.items(), key=lambda x: x[1], reverse=True
    )
    top_data: list[tuple[str, int]] = sorted_data[:top]
    table: Table = create_empty_table()
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

    return table


def print_top_table_stories(
    stories: list[dict[str, Any]], sort: str, top: int = 10
) -> Table:
    sorted_stories: list[dict[str, Any]] = sorted(
        [story for story in stories if story[sort] is not None],
        key=lambda x: convert_word_count(x[sort]) if sort == "words" else x[sort],
        reverse=True,
    )
    top_stories: list[dict[str, Any]] = sorted_stories[:top]
    table: Table = create_empty_table()
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

    return table


def create_empty_table() -> Table:
    return Table(
        show_edge=False,
        show_header=True,
        expand=True,
        row_styles=["none", "dim"],
        box=box.SIMPLE,
    )
