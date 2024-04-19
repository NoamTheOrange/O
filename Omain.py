from flask import Flask
from flask import request

import whisper
import os

#import webbrowser
#import time
from youtubesearchpython import VideosSearch
import requests
from bs4 import BeautifulSoup

Words = {
    "play" : "playMedia",
    "show" : "playMedia",
    "how" : "search"
}
broadcastText = "well helo there"

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

        print(payload)
        return(payload)

def runUpdate(ask):
    global broadcastText
    payload = {}
    if 'updateAll' in ask:
        mockData = {'status':{"stat1":[234,'green','gray'],"stat2":[984,'red','green']}}

        payload.update(mockData)
        text = ""
        text += broadcastText + "\n"

        payload.update({'text' : text})

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
                    return(payload)
                else:
                    return {"error":"select you wave file"}
            if 'update' in request.data:
                ask = request.data['update']
                runUpdate(ask)

    except Exception as e:
        return {"error":str(e)}
    
"""
run debuger:
export FLASK_APP=Omain.py
export FLASK_ENV=development
flask run --host=0.0.0.0
"""
    
