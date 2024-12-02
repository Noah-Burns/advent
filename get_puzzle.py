#!/usr/bin/python3
#
# Usage: get_puzzle.py YYDD
# For year YY day DD
#

from pathlib import Path
import requests
from sys import argv

PWD = Path(__file__).parent.resolve()
HEADERS = {
    "User-Agent": "https://github.com/Noah-Burns/advent by",
}

session_token = (PWD / "token.txt").read_text().strip()
# TODO test session token and prompt to renew if needed

year = argv[1][:2]
day = argv[1][2:]

puzzle_dir = PWD / year / day
Path.mkdir(puzzle_dir, parents=True, exist_ok=True)

url = f"https://adventofcode.com/20{year}/day/{day if int(day[0]) else day[1]}"

### Get input
input_file_path = puzzle_dir / f"input_{year}{day}.txt"

if not input_file_path.exists():
    puzzle_input = requests.get(f"{url}/input", cookies={"session": session_token}, headers=HEADERS).text
    Path.write_text(input_file_path, puzzle_input)

### Get example input(s)
puzzle = requests.get(url, cookies={"session": session_token}, headers=HEADERS).text.split("\n")

in_example = False
n_example = 0
example_lines = []

for line in puzzle:
    if line.startswith("<pre><code>"):
        in_example = True
        n_example += 1
        example_path = puzzle_dir / f"example_{n_example}_{year}{day}.txt"
        example_lines.append(line.replace("<pre><code>", ""))
        continue

    if in_example:
        if line.startswith("</code></pre>"):
            in_example = False

            if not example_path.exists():
                Path.write_text(example_path, "\n".join(example_lines))
            example_lines = []

        else:
            example_lines.append(line)

### Create code file
template_text = Path(PWD / "template.py").read_text()
code_path = puzzle_dir / f"main_{year}{day}.py"

if not code_path.exists():
    Path.write_text(
        code_path,
        template_text.replace("yy", year).replace("dd", day).replace("<LINK>", url),
    )
