import json
import requests
from secrets import spotify_token, spotify_user_id, discover_weekly_id
from datetime import date

#class Images:
 #   def __init__(self):
 #       self.images = []
  #      self.height = 100
  #      self.width = 100
  #      self.url = "https://v4.software-carpentry.org/oop/basics/031.png"



class SaveSongs:
    def __init__(self):
        self.user_id = spotify_user_id
        self.spotify_token = spotify_token
        self.discover_weekly_id = discover_weekly_id
        self.tracks = ""
        self.new_playlist_id = ""

    def find_songs(self):
        #loop through playlists tracks and add them to a list
        print("Finding songs in discover weekly. . .")

        query = "https://api.spotify.com/v1/playlists/{}/tracks".format(discover_weekly_id)

        response = requests.get(query,
        headers={"Content-Type": "application/json",
                "Authorization": "Bearer {}".format(spotify_token)})

        response_json = response.json()
        print(response)

        for i in response_json["items"]:
            self.tracks += (i["track"]["uri"] + ",")
            
        self.tracks = self.tracks[:-1]

        self.add_to_playlist()

        print(self.tracks)
    
    def create_playlist(self):
        #create a new playlist
        
        print("Trying to create a playlist. . .")
        today = date.today()
        todayFormatted = today.strftime("%m/%d/%Y")
        query = "https://api.spotify.com/v1/users/{}/playlists".format(spotify_user_id)

        
        #image = [Images()]
        
        request_body = json.dumps({
            "name": todayFormatted + " discover weekly",
            "description": "here's your new discover weekly playlist :)",
            "public": False,
            #"images": image
        })

        response = requests.post(query, data=request_body, headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(spotify_token)
        })

        response_json = response.json()
        
        return response_json["id"]


    def add_to_playlist(self):
        # add the songs to the new playlist created
        print("Adding songs. . .")
        self.new_playlist_id = self.create_playlist()

        query = "https://api.spotify.com/v1/playlists/{}/tracks?uris={}".format(self.new_playlist_id, self.tracks)

    
        response = requests.post(query, headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(spotify_token)
        })

        print(response.json)

a = SaveSongs()
a.find_songs()