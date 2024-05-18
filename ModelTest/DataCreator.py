import pickle
import csv

data = pickle.load(open('dataColection.pickle', "rb"))
newDataCashe = []

print(data)
for key in data:
    transcript = ""
    output = []
    print(data[key])
    if input("do you want too keep data? y/n") == "n":
        continue
    x = input("do you want too rewrite? y/n")
    if x == 'y':
        transcript = input("write transcript (check seplling!):")
    else :
        transcript = data[key]
    output.append(input("now write outputs in order (end with x):"))
    x = ""
    while x != 'x':
        x = input()
        if x != 'x':
            output.append(x)
    newDataCashe.append({"timeStamp":key, "input":transcript, "output":''.join(output)})

filename = 'trainingData.csv'   
fields = ['timeStamp', 'input', 'output']

with open(filename, 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fields)
 
    writer.writeheader()
 
    writer.writerows(newDataCashe)

open("dataColection.pickle", "w").close()