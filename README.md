# osu-song-history
Pull songs from `Most Played Beatmaps` section of any osu player profile, given their player IDs.

![Most Played Beatmaps](https://i.imgur.com/TQPXeOk.png)


# Setup:
*Requires Python 3.11 and above*
1. Install Poetry (visit their website).
```
https://python-poetry.org/docs/#installation
```
2. Clone this repo.
```commandline
git clone https://github.com/hkohko/osu-song-history.git
```
3. Install dependencies.
```commandline
cd osu-song-history
poetry install
```
# How to Scrape and Save:
*Uses SQLite3*

**!!Navigate to `PROJECT_ROOT/scrape_osu_songs/` and create a folder named `songs`!!**

Scraping is a two step process:
In `./scrape_osu_songs/main.py`:
```py
if __name__ == "__main__":
    save_song(user_id_int=user_id, index_start, index_stop)  # downloads from profile
    parse_and_save()  # saves into .json files
```
`user_id` is the player's id.
`index_start` and `index_stop` refers to the number of `Most Played Beatmaps` displayed on the profile.

## Example:

**user_id**:
![ID](https://i.imgur.com/VhuVDSG.png)

**index:**
![index](https://i.imgur.com/9L2MyWi.png)

Based on the information above, a straightforward way is to simply write:
```py
if __name__ == "__main__":
    save_song(user_id_int=user_id, 0, 3900)  # start from 0 until 3900
    parse_and_save()  # saves to sqlite3 database
```
`save_song()` downloads the songs and generates `.json` files containing the raw data.

Each .json files contain a maximum of 100 songs. They are stored in `scrape_osu_songs/songs/<user_id>/`.

As the path suggests, each `user_id_int` has its own folder containing the `.json` files.

`parse_and_save()` is responsible for parsing the .json files and saving them to a database.


# Viewing the Data:
a simple GUI is provided to view and query the data.
1. Double click `./run.py`

### The GUI
![GUI](https://i.imgur.com/JGVl5sc.png)
### How to use:
> 1. Type in the `artist`, `title` or `source` (where the song originates from, e.g. SOUND VOLTEX) inside the input field.
> 2. Choose what you want to seach for: `Artist`, `Title`, or `Source`
> 3. Choose by what you want to sort the data with: `Artist` or `Title`.
> 3. Press `Search` or simply `Enter`.

The words are kinda weird but let me explain.

Based on the image above:

> From the database, show me data **where** the artist column contains keywords **like** 'miku'.

**By default, the program will search by keywords you type in, hence 'like'.**

However, if the `Exact?` box is checked, it will only show you **exact** matches.

`Sort by` choices are pretty straightforward, sort by either `Artist` or `Title`.
`Clear` simply clears the input field.

### The context menu (still being worked on):
![Context manu](https://i.imgur.com/cBDoWxH.png)
You can right-click on any entry, gives you (currently) 1 handy option, `Preview`.

`Preview` simply opens the browser and gives you a 10 second sample of the song.
It is similar to previewing the song on osu website itself.

There are different things being planned here. One obvious option is to simply bring you to YouTube where you can listen to the song.

We'll see.
