# ADGSTUDIOS 2021 - Open Music Build Database
# Script - builddb.py
import os
import glob
import json 

# where path is the directory where the mp3 files are stored
path = "./"
songs = glob.glob(path + "/*/*.mp3", recursive = True)

# our paylaod will be stored in a list
metadata = []

print('Preparing to build database...')

for song in songs:
    # checking if path is valid
    if os.path.exists(song):
        # GitHub Restriction - 100MB files limit from CLI (100MB = 100,000,000 bytes))
        if (os.path.getsize(song) / (1024*1024)) < 100:
            metadata.append({'name':os.path.basename(song).replace('.mp3','').replace('.MP3',''),'cover':'./static/img/nomusicicon.png','source':song.replace('\\','/')})

print('We have ' + str(len(metadata)) + ' songs to add to the database.')

print('Writing to database... as songdata.json')
# creating a json file
with open("songdata.json", "w") as outfile: 
    json.dump(metadata, outfile) 

#injecting to JavaScript File
print('Adding Config to file...')
for root, dirs, files in os.walk("/"):
    for file in files:
        if file.endswith(".js"):
            if (file == 'script.js'):
                jsfile = os.path.join(root, file)
                with open(jsfile, 'r') as file :
                    filedata = file.read()
                    # Replace the target string
                filedata = filedata.replace('{payload}', str(metadata))
                    # Write the file out again
                with open(jsfile, 'w') as file:
                    file.write(filedata)
