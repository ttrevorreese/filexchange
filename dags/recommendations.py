import sqlalchemy
import pandas as pd
from sqlalchemy.orm import sessionmaker
import requests
import json
from datetime import datetime
import datetime 
import sqlite3
<<<<<<< HEAD
TOKEN = "BQC9vQeypOtEkQvXOWlPWaq1y136iG3PTlURzhxaP3F-ALDGe2wnO23paN9CdlLak93gGjNFQ8T1g519A03BVDGsOvGr9nsRB50ainZzg_l5zUPqKyNOZipnQ7jYf8yizvyT4kZvTdeJ0K3swE1-BAxW_Z0xsdxes_2m9iFEBCgFb8GC6Pz-_G544cwsM4v_ses4sz7mxA7tSU86Yp6fVRXU8iSbwdqSJkGk9g6o2zWprIGhISq_XiySSJglttzDpEWP1X4q0tc7lVD1x3BbUaLNmgd-NsX3TM2mOoozY-1tNLNl3rV_c16FuWE4pJ87qE9VnAQVjJj1ZGpNZd2z9NPuUY2xZLxQ" #TOKEN LINK - https://developer.spotify.com/
=======
TOKEN = "BQC7NHaIwubN2-oPpxbK5zBMQVg5uqGE8U1TTcWIbtEA2I9lEJwGhjz4BE9vcgD3SK_oVI-n_uR3a_h9D1XoZghKw_KiJlRO-XhHPEeZ994wIh6EhmG6DldOY7Z7B1qYu5VLp-HrV_36YNAmW0nJVt9HY1Dg8cQbWkMoZFWqgjUfNZIyvtTdrrYpHrI_yQ8VrreQdZ9Efozf7FR45UYk_g-9GV4QoU-p1VMNuXzADlbW1GNxQ0Og1PicIIs1dsy1VSMCdBdSLxXUifWuDkA2mFIJLJMaWzSRjS_Pojep6-5khpK-fgR2cmw4HjncPl68NZT8AfuCeoifMfexLKmYGj5J1eXMjYny" #TOKEN LINK - https://developer.spotify.com/
>>>>>>> 061a6bf5bd1b7736764e4ccec10ed01212c79c80
def read_db():
    import sqlite3
    import pandas as pd

    # Create a connection to the SQLite database
    conn = sqlite3.connect('song_history.db')

    # Read the contents of the "song_history" table into a DataFrame
    song_df = pd.read_sql_query("SELECT * from song_history", conn)

    # Close the database connection
    conn.close()

    # Print the DataFrame
    make_rec(song_df)
    
def make_rec(song_df):
    import requests

    endpoint_url = "https://api.spotify.com/v1/recommendations?"

    limit=50
    market="GB"
    seed_genres="hip-hop"
    target_danceability=0.9

    import random

    # Select a random row from the song_df DataFrame
    random_row = song_df.sample()

    # Get the artistid from the selected row
    artist_id = random_row['artistid'].values[0]

    # Look up the corresponding artist name from the artist_name column
    artist_name = song_df.loc[song_df['artistid'] == artist_id, 'artist_name'].values[0]

    # Print the artist name
    print(f"Randomly selected artist: {artist_name}")

    seed_artists = artist_id # ID for Drake
    query = f'{endpoint_url}limit={limit}&market={market}&seed_genres={seed_genres}&target_danceability={target_danceability}'
    query += f'&seed_artists={seed_artists}'
    response =requests.get(query, 
                headers={"Content-Type":"application/json", 
                            "Authorization":"Bearer {token}".format(token = TOKEN)})

    #Put your token after the word bearer in the line above
    json_response = response.json()

    uris = []
    song_name = []
    name = []
    #r = requests.get("https://api.spotify.com/v1/me/player/recently-played?limit={limit}&after={time}".format(time=yesterday_unix_timestamp, limit = limit), headers = input_variables)
    #data = r.json()
    song_names = []
    artist_names = []
    played_at_list = []
    timestamps = []
    artistid = []

    for i in json_response['tracks']:
        # song_names.append(song["name"])
        # artist_names.append(song["album"]["artists"][0]["name"])
        # artistid.append(song["album"]['artists'][0]['id'])
                uris.append(i)
                print(f"\"{i['name']}\" by {i['artists'][0]['name']}")
                song_name.append(i['name'])
                name.append(i['artists'][0]['name'])

    # Create a dictionary from the song_name and name lists
    song_dict = {"Artist Name": name, "Song Name": song_name}

    # Convert the dictionary into a DataFrame
    rec_df = pd.DataFrame(song_dict)

    #Applying transformation logic
    Transformed_df=song_df.groupby(['timestamp','artist_name'],as_index = False).count()
    Transformed_df.rename(columns ={'played_at':'count'}, inplace=True)
    #Creating a Primary Key based on Timestamp and artist name
    Transformed_df["ID"] = Transformed_df['timestamp'].astype(str) +"-"+ Transformed_df["artist_name"]

    # Print the resulting DataFrame
    print(rec_df)
    make_db(rec_df)

    return Transformed_df[['song_name','artist_name']]

def make_db(rec_df):
       
    # Define the file path and database name
    db_path = "recommendations.db"
    # Create a SQLite database connection
    conn = sqlite3.connect(db_path)

    # Create the recommendations table in the database
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS recommendations
            (song_name text, name text)''')
    

    # Insert the DataFrame into the recommendations table
    rec_df.to_sql('recommendations', conn, if_exists='replace', index=False)

    # Commit the changes and close the database connection
    conn.commit()
    conn.close()

read_db()
