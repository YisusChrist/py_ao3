import re
from pathlib import Path
from tkinter import Tk, filedialog
from typing import Any

import chardet
from rich import print
from rich.markdown import Markdown


def process_line(line: str) -> str:
    if not line.startswith("- by") or line.startswith("- by ["):
        return line

    print(f"Original: {line}")

    url_format = "[{}](https://archiveofourown.org/users/{}/pseuds/{})"
    prefix = "- by "
    suffix = " ‚Üí "
    try:
        author, size = line.split(prefix)[1].split(suffix)
    except ValueError:
        print(f"[red]Error splitting line: {line}[/]")
        return line

    text: str = url_format.format(author, author, author)
    result: str = f"{prefix}{text}{suffix}{size}"

    print(f"Result: {result}")
    return result


def repair_data(file: str | Path, encoding: str) -> None:
    file = Path(file).resolve()
    if not file.exists():
        print(f"File not found: {file}")
        return

    content: str = get_file_content(file)

    results: list = []
    for line in content.split("\n"):
        results.append(process_line(line))

    # Calculate the result file name adding a suffix
    result_file: Path = file.with_name(f"{file.stem}_repaired{file.suffix}")
    result_file.write_text("\n".join(results), encoding=encoding)


def extract_stories(file: str | Path) -> list[dict[str, Any]]:
    content: str = get_file_content(file)
    # Extract the list of stories in the content
    """
    Each story has the following format:

    *[TITLE]*

    - [CHARACTERS] ([SERIES])

    - by [[AUTHOR]](...) → [WORDS]

    - [RATING][COMMENT]
    """
    # Define the regular expression for the story titles
    title_pattern = re.compile(r"^\*.*?\*", re.MULTILINE)

    # Find all titles
    titles = title_pattern.findall(content)

    # Split the content into sections based on the titles
    sections = title_pattern.split(content)

    # Initialize a list to hold the stories
    stories = []

    # Iterate over the titles and corresponding sections
    for i, section in enumerate(
        sections[1:], start=1
    ):  # Skip the first section, it's before the first title
        title: str = titles[i - 1]
        # Use regular expressions to find the other details
        characters_match = re.search(r"- (.*?) \((.*?)\)", section)
        author_match = re.search(r"- by \[(.*?)\]\(.*?\)", section)
        words_match = re.search(r" ‚Üí (.*?) words", section)
        rating_comment_match = re.search(r"- (.*?)/100, (.*)", section)

        if characters_match and author_match and rating_comment_match:
            characters = characters_match.group(1)
            series = characters_match.group(2)
            author = author_match.group(1)
            words = words_match.group(1) if words_match else "0"
            rating = rating_comment_match.group(1)
            comment = rating_comment_match.group(2)

            characters_list: list[str] = characters.split(" √ó ")
            # Create a dictionary for the story
            try:
                story: dict[str, Any] = {
                    "title": title,
                    "characters": characters_list,
                    "series": series,
                    "author": author,
                    "words": words,
                    "rating": int(rating),
                    "comment": comment,
                }
            except ValueError:
                print(f"[red]Error on section {i}[/]")
                print(Markdown(f"Title: {title}"))
                print(f"Characters: {characters}")
                print(f"Author: {author}")
                print(f"Words: {words}")
                print(f"Rating: {rating}")
                print(f"Comment: {comment}")

            # Add the story to the list
            stories.append(story)
        elif not characters_match and not author_match and not rating_comment_match:
            stories.append(
                {
                    "title": title,
                    "characters": None,
                    "series": None,
                    "author": None,
                    "words": None,
                    "rating": None,
                    "comment": None,
                }
            )
        else:
            print(f"[red]Error processing section {i}[/]")
            print(Markdown(f"Title: {title}"))
            print(f"Characters: {characters_match}")
            print(f"Author: {author_match}")
            print(f"Rating/Comment: {rating_comment_match}")
            print("")

    return stories


def get_file_content(file: str | Path) -> str:
    file = Path(file).resolve()

    encoding: str | None = "utf-8"
    try:
        content: str = file.read_text()
    except UnicodeDecodeError as e:
        print(f"Error reading file: {e}")
        # Detect file encoding
        with open(file, "rb") as f:
            encoding = chardet.detect(f.read())["encoding"]
        print(f"Detected encoding: {encoding}")
        if not encoding:
            return ""
        content = file.read_text(encoding=encoding)

    return content


def get_file_path() -> Path | None:
    # Create a Tk root window
    root = Tk()
    # Hide the main window
    root.withdraw()
    # Ask the user to select a file
    file_path: str = filedialog.askopenfilename()
    if not file_path:
        print("No file selected.")
        return None

    return Path(file_path).resolve()
