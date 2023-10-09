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
1. Double click `./run_scrape.py`
### The scrape GUI
![scrape gui](https://i.imgur.com/x6OHJz0.png)
`ID` is the player's id.
`start` and `stop` refers to the number of `Most Played Beatmaps` displayed on the profile.

If `Store JSON to Database` is checked, the program will :
1. Download the `JSON` files
2. Parse the `JSON` files and store **ONLY:**
   - Artist
   - Title
   - Preview
   - Source

Otherwise, it only downloads and store the raw JSON files.
## Example:

**user_id**:
![ID](https://i.imgur.com/VhuVDSG.png)

**index:**
![index](https://i.imgur.com/9L2MyWi.png)

Based on the information above, a straightforward way is to simply type in:
![example](https://i.imgur.com/ebBVR6A.png)

Each `.json` files contain a maximum of 100 songs. They are stored in `scrape_osu_songs/songs/<user_id>/`.

As the path suggests, each `ID` has its own folder containing the `.json` files.

# Viewing the Data:
a simple GUI is provided to view and query the data.
1. Double click `./run_view.py`

### The view GUI
![GUI](https://i.imgur.com/JGVl5sc.png)
### How to use:
1. Type in the `artist`, `title` or `source` (where the song originates from, e.g. SOUND VOLTEX) inside the input field.
2. Choose what you want to search for: `Artist`, `Title`, or `Source`
3. Choose by what you want to sort the data with: `Artist` or `Title`.
4. Press `Search` or simply `Enter`.

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
