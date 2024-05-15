import pickle

data = pickle.load(open('dataColection.pickle', "rb"))
print(data)
for key in data:
    transcript = ""
    output = []
    print(data[key])
    x = input("do you want too rewrite? y/n")
    if x == 'y':
        transcript = input("write transcript (check seplling!):")
    else :
        transcript = data[key]
    output.append(input("now write outputs in order :"))
    x = ""
    while x != 'X':
        x = input()
        if x != 'X':
            output.append(x)
