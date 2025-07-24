"""MP3 file manipulations."""

import json
from configparser import ConfigParser
from pathlib import Path
from typing import List
from typing_extensions import Annotated
from pydub import AudioSegment
from rich.console import Console
from rich.table import Table
import music_tag
import typer

app = typer.Typer()
console = Console()
config = ConfigParser()
config.read('config.ini')

@app.command()
def merge(
    files: Annotated[List[Path], typer.Argument(help='MP3 files to merge')],
    output: Annotated[str, typer.Argument(help='Output file')]):
    """Merge MP3 files into a single one. Non-MP3 files are ignored."""

    combined = AudioSegment.empty()

    with console.status('Merging files...'):
        for file in files:
            if file.match('*.mp3'):
                sound = AudioSegment.from_file(file, format='mp3')
                combined += sound

    with console.status('Exporting output...'):
        if not output.endswith('.mp3'):
            output = 'output.mp3'
        combined.export(output, format='mp3')

    print(f'Exporting finished: {output} created')


@app.command()
def read_tags(file: Annotated[str, typer.Argument(help='MP3 file to scan')]):
    """Print MP3 tags of a file. Enable or disable tags in the config.ini readTags section."""

    tags_to_print = []

    for tag in config['readTags']:
        if config['readTags'][tag] == 'yes':
            tags_to_print.append(tag)

    table = Table(title=str(file))
    table.add_column('Tag')
    table.add_column('Value')

    song = music_tag.load_file(file)

    for tag in tags_to_print:
        if not song[tag]:
            table.add_row(tag.capitalize(), '[red]Missing[/red]')
        else:
            table.add_row(tag.capitalize(), str(song[tag]))

    console.print(table)


@app.command()
def edit_tags(
    file: Annotated[str, typer.Argument(help='MP3 file to edit')],
    json_file: Annotated[str, typer.Argument(help='JSON file with tags to edit')]):
    """
    Edit tags of a MP3 file.
    
    Tags are indicated in a JSON file, such as:

    {
        "artist": "some great artist",
        "tracktitle": "super song",
        "year": "2025",
        "artwork": "path/to/artwork",
    }

    Read-only tags: bitrate, codec, length, channels, bitspersample and samplerate
    """

    song = music_tag.load_file(file)

    with open(json_file, mode='r', encoding='utf-8') as f:
        json_data = json.load(f)

    for tag in json_data:
        try:
            # Only artwork is special
            if tag == 'artwork':
                with open(json_data[tag], mode='rb') as img:
                    song['artwork'] = img.read()
            else:
                song[tag] = json_data[tag]
        except KeyError:
            console.print(f'[red]Unknown key: {tag}[/red]')

    song.save()
    print('Done')


if __name__ == '__main__':
    app()
