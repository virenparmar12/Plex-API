from flask import Flask, request,jsonify
import plexapi  
from plexapi.myplex import MyPlexAccount,MyPlexUser
from plexapi.server import PlexServer
from plexapi.library import Library
from plexapi.base import PlexObject
from plexapi.playlist import Playlist
import os


app = Flask(__name__)
token = os.environ['user_token']
baseurl = 'http://localhost:32400'
plex = PlexServer(baseurl,token)
print(token)


@app.route('/invite_friend',methods=['POST'])
def inviteFriend():
    request_data = request.get_json()
    username = request_data['username']
    password = request_data['password']
    friend_username = request_data['friendusername']
    print(username)
    print(password)
    print(friend_username)
    try:
        a = MyPlexAccount(username=f"{username}",password=f"{password}",token=token,session=None, timeout=None)
        a.inviteFriend(user=f"{friend_username}",server=plex,sections=None, allowSync=False, allowCameraUpload=False, allowChannels=False, filterMovies=None, filterTelevision=None, filterMusic=None)
        return "invited successfully"
    except:
        return "you aleady requested or username is wrong"    
    
@app.route('/create_folder',methods=['POST'])
def createFolder():
    request_data = request.get_json()
    lib_type = request_data['type']
    lib_name = request_data['name']
    
    b = Library(server=plex,data=None)
    if lib_type == "movie":
        b.add(name=f"{lib_name}",type=f"{lib_type}",agent="com.plexapp.agents.none",scanner="Plex Movie, Plex Movie Scanner, Plex Video Files Scanner, Plex Video Files",location="/Movies",language="en",enableCinemaTrailers=True,enableBIFGeneration=True,includeInGlobal=True)
        return "library created successfully"
    if lib_type == "photo":
        b.add(name=f"{lib_name}",type=f"{lib_type}",agent="com.plexapp.agents.none",scanner="Plex Photo Scanner",location="/Photos",language="en",enableAutoPhotoTags=True,enableBIFGeneration=True,includeInGlobal=True)
        return "library created successfully"
    if lib_type == "show":
        b.add(name=f"{lib_name}",type=f"{lib_type}",agent="com.plexapp.agents.none",scanner="Plex TV Series,Plex Series Scanner",location="/Shows",language="en",episodeSort=1,flattenSeasons=0,enableBIFGeneration=True,includeInGlobal=True)
        return "library created successfully"
    else:
        return "please give a valid type of library"

@app.route('/library_list',methods=['GET'])
def libraryList():
    c = PlexObject(server=plex,data=None)
    return f'{c.fetchItems(ekey="/library/sections/")}'

@app.route('/create_playlist',methods=['POST'])
def create_playlist():
    request_data = request.get_json()
    playlistname = request_data['name']
    section = request_data['section']
    d = Playlist(server=plex,data=None)
    d.create(server=plex,title=f"{playlistname}",smart=True,section=f"{section}")
    return "playlist created successfully"

@app.route('/listOfPlaylist',methods=['GET'])
def listOfPlaylist():
    return f'{plex.playlists()}'
if __name__ == '__main__':  
    app.run(host='localhost')