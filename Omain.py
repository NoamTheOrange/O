from flask import Flask
from flask import request

import whisper
import os
import pickle
import random
import string

#import webbrowser
#import time
from youtubesearchpython import VideosSearch
import requests
from bs4 import BeautifulSoup

Words = {
    "play" : "playMedia",
    "show" : "playMedia",
    "how" : "search",
    "create user" : "createUser"
}
broadcastText = "well hello there"

def createUser(transcript):
    userFile = pickle.load(open('userData.pkl', "rb"))
    generating = True
    ID = ""
    name = ""
    permissions = ""

    while generating == True:
        ID = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        for used in userFile:
            if ID == used:
                pass
        else:
            generating = False

    data = transcript.split()
    for dataPosition in range(len(data)):
        if dataPosition == "user":
            name = data[dataPosition +1]
        if dataPosition == "argument":
            permissions = data[dataPosition +1]

    user = {ID : {
        'name' : name,
        'permissions' : permissions,
        'message' : "".join("welcome"+name)}}

    with open('users.pickle', 'wb') as f:
        pickle.dump(user, f)
    f.close()
    return({"newID" : ID})

def playMedia(inp):
    for i in ["play","show"]:
        if i in inp:
            sPoint = inp.find(i) + len(i) + 1
            for j in ["on youtube"]:
                if j in inp:
                    ePoint = inp.find(j) - 1
                    data = inp[sPoint:ePoint]
                    print ("playing: " + data)
                    videosSearch = VideosSearch(data, limit = 2)
                    x = videosSearch.result()["result"][0]["id"]
                    return ({"Youtube":"https://www.youtube.com/watch?v=" + x})
                    #webbrowser.open("https://www.youtube.com/watch?v=" + x)      : client end
                    #time.sleep(1)
                    #keyboard.press_and_release('space')

def search(inp):
    for i in ["how does","google"]:
        if i in inp:
            if i == "how does":
                sPoint = inp.find(i) + 1
            else:
                sPoint = inp.find(i) + len(i) + 1
            data = inp[sPoint:]
            #webbrowser.open("https://www.google.com/search?client=firefox-b-d&q="+data)  : client end
            params = {
                "q": data,      	# query example
                "hl": "sv",      	# language
                "gl": "se",      	# country of the search, UK -> United Kingdom
                "start": 0,      	# number page by default up to 0
                #"num": 100      	# parameter defines the maximum number of results to return.
            }
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
            }
            info = []
            html = requests.get("https://www.google.com/search", params=params, headers=headers, timeout=30)
            soup = BeautifulSoup(html.text, 'lxml')
            try:
                snippet = soup.select_one(".hgKElc").text
            except:
                try:
                    snippet = soup.select_one(".lEBKkf span").text
                except:
                    snippet = None
            print (snippet)
            return({"Search" : ["https://www.google.com/search?client=firefox-b-d&q="+data, snippet]})



def runAudio(audio_name):
        model = whisper.load_model("base")
        result = model.transcribe(audio_name)
        Ctranscript = result["text"]
        os.remove(audio_name)
        transcript = Ctranscript.lower()

        payload = {}
        payload["transcript"] = transcript

        for word in Words:
            if word in transcript:
                if Words[word] == "playMedia":
                    payload.update(playMedia(transcript))
                if Words[word] == "search":
                    payload.update(search(transcript))
                if Words[word] == "createUser":
                    payload.update(createUser(transcript))

        print(payload)
        return(payload)

def runUpdate(ask, ID):
    global broadcastText
    payload = {'updateData':{}}
    if 'updateAll' in ask:
        mockData = {'status':{"stat1":[234,'green','gray'],"stat2":[984,'red','green']}}

        payload["updateData"].update(mockData)
        text = ""
        text += broadcastText + "\n"
        try:
            userFile = pickle.load(open('userData.pkl', "rb"))
            for user in userFile:
                if ID == user:
                    text += userFile[ID]['message'] + "\n"
        except:
            pass

        payload["updateData"].update({'text' : text})
        return(payload)

app = Flask(__name__)
@app.route("/",methods=["POST","GET"])
def main():
    try:
        if request.method=='POST':
         
            if 'audio' in request.files:
                audio=request.files['audio']
                audio_name=audio.filename
                if '.wav' in audio_name:
                
                    
                    audio.save(audio_name)

                    payload = runAudio(audio_name)
    
                    print(payload)
                else:
                    return {"error":"select you wave file"}
            elif 'update' in request.data:
                print("hej")
                ask = request.data['update']
                ID = request.data['ID']
                payload = runUpdate(ask, ID)
            print(payload)
            return(payload)

    except Exception as e:
        return {"error":str(e)}

if __name__ == '__main__':  
   app.run(debug = True, host='0.0.0.0')
    
"""
run debuger:
export FLASK_APP=Omain.py
export FLASK_ENV=development
flask run --host=0.0.0.0
"""
    
