import os
import pylast
import yaml
import pandas as pd
from urllib import request

# Funtion to load API keys from yaml file
def load_secrets():
    secrets_file="pylast.yaml"
    if os.path.isfile(secrets_file):
        import yaml  # pip install pyyaml
        with open(secrets_file, "r") as f:
            doc=yaml.load(f)
    else:
        doc={}
        try:
            doc["api_key"]=os.environ['PYLAST_API_KEY'].strip()
            doc["api_secret"]=os.environ['PYLAST_API_SECRET'].strip()
        except KeyError:
            pytest.skip("Missing environment variables: PYLAST_USERNAME etc.")
    return doc
    
secrets=load_secrets()
api_key=secrets["api_key"]
api_secret=secrets["api_secret"]


network=pylast.LastFMNetwork(api_key, api_secret)

# Read all the folder names in the music directory.
dirtree=os.listdir()

# Strip any leading / trailing whitespace.
names=[x.strip(' ') for x in dirtree]
# Clean the folder names of periods and special characters.
names=[x.replace('.',' ') for x in names]
# Make sure any artist name starting with "Anti" gets a "-" appended after.
names=[x.replace('Anti ','Anti-') for x in names]
# Create data frame with old and new names to use as a master location list.
masterartist=pd.DataFrame({'original': dirtree, 'modified': names})

# See if there's a way to strip this ID out of mp3 tags. To double-check artist names.
# mbid = artist.get_mbid()

for i in names:
   print('go')

#  This should be a Try/Catch block. Any mismatechs should be quiet and written to a log file.
# If image is NULL, do something to re-check the artist name, ex. "Anti Heros" vs. "Anti-Heros"
artistName="Anti-Heros"
artist=network.get_artist(artistName)

# Here's the image payload.
image=artist.get_cover_image()

# Download the file from `url` and save it to the correct folder.
ogfilename=masterartist[masterartist['modified'].str.contains(artistName)]
foldername=ogfilename.iloc[0]

urllib.request.urlretrieve(image, foldername+"folder.png")


