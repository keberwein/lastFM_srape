import os
import pylast
import yaml
import pandas as pd
import urllib

# Set wd to directory containing yaml file.
os.chdir("lastFM_srape")

# Function to load API keys from yaml file.
def load_secrets():
    secrets_file = "pylast.yaml"
    if os.path.isfile(secrets_file):
        with open(secrets_file, "r") as f:
            doc = yaml.load(f)
    else:
        doc = {}
        try:
            doc["api_key"] = os.environ['PYLAST_API_KEY'].strip()
            doc["api_secret"] = os.environ['PYLAST_API_SECRET'].strip()
        except KeyError:
            print("Missing environment variables")
    return doc


secrets = load_secrets()
api_key = secrets["api_key"]
api_secret = secrets["api_secret"]
# Save credentials in one place.
network = pylast.LastFMNetwork(api_key, api_secret)

# Set wd to music library.
os.chdir("/media/santo/music/")
root = "/media/santo/music/"

# Read all the folder names in the music directory.
dirtree = os.listdir()

# Scan directory tree for folders with no cover art.
no_art = []
for dir in dirtree:
    folder = os.path.join(root, dir)
        if os.path.exists(os.path.join(folder, 'folder.png')) == False and os.path.exists(os.path.join(folder, 'folder.jpg')) == False:
            no_art.append(dir)

# Make sure everything in list is a character.
names = [str(i) for i in no_art]
# Make sure any artist name starting with "Anti" gets a "-" appended after.
names = [x.replace('Anti.', 'Anti-') for x in names]
# Clean the folder names of periods and special characters.
names = [x.replace('.', ' ') for x in names]
# Replace "The" at the end of directory names and append it to beginning.
names = [x.replace(', The', '') for x in names]
# Colapse double spaces.
names = [x.replace('  ', ' ') for x in names]
# Remove punctuation.
names = [x.replace("'", '') for x in names]
names = [x.replace(',', '') for x in names]
# Remove & symbol.
names = [x.replace('&', 'and') for x in names]
# Strip any leading / trailing whitespace.
names = [x.strip(' ') for x in names]

# Create data frame with old and new names to use as a master location list.
masterartist = pd.DataFrame({'original': no_art, 'modified': names})

for i in names:
    artistName = i
    try:  # If the artist name isn't recognized by last.fm, skip.
        artist = network.get_artist(artistName)
        image = artist.get_cover_image()
        ogfilename = masterartist[masterartist['modified'].str.contains(artistName)]
        foldername = ogfilename.iloc[0, 0]
        try:  # Skip if artist name throws a type error.
            urllib.request.urlretrieve(image, foldername + "/folder.png")
        except TypeError:
            pass
    except pylast.WSError:
        pass

   

   




