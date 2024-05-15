
import tkinter as tk
import pyaudio
import wave
import os
import requests
from datetime import datetime
from threading import Thread
import time

import webbrowser
from bs4 import BeautifulSoup
import pyttsx3
from youtubesearchpython import VideosSearch
import keyboard

privaleges = 0
UserID = ""

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
RECORD_SECONDS = 20

appONOFF = [True]
OutputText = ""


def record(stopper_var: tk.BooleanVar, frames_var: tk.Variable, gss: tk.IntVar, dir_var, button_text_var):
    if frames_var.get():
        decision = tk.messagebox.askyesno(title='there is alredy a recording', message='Do you want to over write it?')
        if not decision:
            return

    button_text_var.set('stop recording')
    stopper_var.set(True)

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* recording")

    frames = []

    while stopper_var.get():
        data = stream.read(CHUNK)
        frames.append(data)

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()
    gss.set(p.get_sample_size(FORMAT))
    frames_var.set(frames)
    print('record end')
    button_text_var.set('start recording')
    save(frames_var, gss.get(), dir_var)


def record_button(stopper_var: tk.BooleanVar, frames: tk.Variable, gss_var: tk.IntVar, dir_var, button_text_var):
    if not stopper_var.get():
        Thread(target=record, args=(stopper_var, frames, gss_var, dir_var, button_text_var)).start()
    else:
        stopper_var.set(False)


def save(frames, gss, directory):
    if not frames:
        tk.messagebox.showerror(title='No record', message='You made no record that can be sent')
        return

    file_name = datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%f') + ".wav"
    file_location = directory + '/' + file_name

    wf = wave.open(file_location, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(gss)
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames.get()))
    wf.close()
    FileSize = os.path.getsize(file_location)
    
    frames.set([])
    print("saved")
    param = {"type" : "audio"}
    send(file_location, "audio")
    os.remove(file_location)



def action(returnn):
    global OutputText
    print(returnn)
    if "SerAct" in returnn.keys():
        pass

    if "newID" in returnn.keys():
        global UserID
        UserID = returnn["newID"]

    if "Search" in returnn.keys():
        webbrowser.open(returnn["Search"][0])
        '''    :  server side
        params = {
            "q": returnn[1],          # query example
            "hl": "sv",          # language
            "gl": "se",          # country of the search, UK -> United Kingdom
            "start": 0,          # number page by default up to 0
            #"num": 100          # parameter defines the maximum number of results to return.
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
        '''
        print (returnn["Search"][1])
        OutputText = returnn["Search"][1]

        engine = pyttsx3.init()
        engine.say(returnn["Search"][1])
        engine.runAndWait()
        
    if "Youtube" in returnn.keys():
        #videosSearch = VideosSearch(returnn["Youtube"][0], limit = 2)
        #x = videosSearch.result()["result"][0]["id"]
        webbrowser.open(returnn["Youtube"])
        time.sleep(2)
        keyboard.press_and_release('space')

def send(payload,typee):
    global UserID
    url = 'http://192.168.0.229:5000/'
    if typee == "audio":
        with open(payload, 'rb') as audio:
            r = requests.post(url, data={"ID" : UserID}, files={"audio" : audio})
        action(r.json())
    elif typee == "ID":
        r = requests.post(url, files={"check ID" : payload})
        return(r.json())
    elif typee == "update":
        r = requests.post(url, data={"update" : payload, "ID" : UserID})
        return(r.json())
    print(r.json())




def checkDir(dir_path):
    cwd = os.getcwd()
    if os.path.isdir(dir_path):
        print("directory found")
        return
    else:
        os.mkdir(dir_path)


def checkID(ID):
    global privaleges
    global User
    r = send(ID, "ID")
    if r["ID"] == "valid":
        print("admin mode active")
        privaleges = 1
        User = ID
        return("admin")
    else:
        return("User ID")

def switchStatus(onoff, btnStatus, frame):
    #print(onoff.get())
    if onoff.get():
        btnStatus.config(text = "hide status")
        frame.grid(row = 2, column = 0)
        return onoff.set(False)
    else:
        btnStatus.config(text = "show status")
        frame.grid_forget()
        return onoff.set(True)

def Update(frame, OutMaiTex):
    global appONOFF
    while appONOFF[0]:
        for widget in frame.winfo_children():
            widget.destroy()
        
        returnn = send(["updateAll"],"update")
        print(returnn)
        data = returnn["updateData"]
        
        #data = {"status" : {"stat1" : [123,"gray","green"], "stat2" : [234,"green","red"]}}   #example data
        row = 0
        for name in data["status"]:
            Label = tk.Button(master = frame, text = name, bg = data["status"][name][1])
            Label.grid(row=row, column=0)
            LabelStat = tk.Label(master=frame,relief=tk.RAISED , text=data["status"][name][0], bg = data["status"][name][2])
            LabelStat.grid(row=row, column=1)

            row += 1
           
        
        global OutputText        
        OutMaiTex.insert(tk.END, OutputText)
         
        time.sleep(5)


def main():
    global appONOFF
    appONOFF = [True]
    top = tk.Tk()
    stopper_var = tk.BooleanVar(value=False)
    frames = tk.Variable(value=[])
    gss_var = tk.IntVar(value=0)
    dir_path = tk.StringVar(value='App\Odir')
    rec_var = tk.StringVar(value='start recording')
    ID = tk.StringVar(value='User ID')
    showStatus = tk.BooleanVar(value=True)
    global OutputText

    checkDir(dir_path.get())

    mainFrame = tk.Frame(master = top)
    loginFrame = tk.Frame(master = top, relief = tk.GROOVE, borderwidth = 5)
    statusFrame = tk.Frame(master = top)
    outputFrame = tk.Frame(master = top, relief = tk.GROOVE, borderwidth = 5)

    OutMaiTex = tk.Text(master = outputFrame,state = 'disabled', height = 5, width = 20)
    OutMaiTex.pack()

    btn1 = tk.Button(
        master = mainFrame, text="start recording", textvariable=rec_var,
        command=lambda: record_button(stopper_var, frames, gss_var, dir_path.get(), rec_var)
        )
    btn1.pack()

    if ID == "admin":
        checkcollor = 'green'
    else:
        checkcollor = 'black'
    IDentry = tk.Entry(master = loginFrame, textvariable=ID, fg=checkcollor)
    IDentry.pack()

    btn2 = tk.Button(
        master = loginFrame, text = "validate", height=1,width=6,
        command=lambda: ID.set(checkID(ID.get()))
        )
    btn2.pack(side=tk.LEFT)

    '''
    
    '''
    
    btnStatus = tk.Button(master = mainFrame, text="show status", command=lambda: switchStatus(showStatus, btnStatus, statusFrame))
    btnStatus.pack()
    '''
    if showStatus.get():
        print("dfsf")
        btnStatus.config(text = "hide status")
    else:
        print("sdajsda")
        btnStatus.config(text = "show status")
    '''
    

    mainFrame.grid(row = 0, column = 0)
    loginFrame.grid(row = 1, column = 0)
    outputFrame.grid(row = 0, column = 1)
    thred1 = Thread(target=Update, args=(statusFrame, OutMaiTex))
    thred1.start()

    top.mainloop()

    appONOFF[0] = False


    
       

if __name__ == '__main__':
    main()


