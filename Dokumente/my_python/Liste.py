# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import time
import json

#global liste = []
#zahl = 3
#from main import liste


def loop():
    global a
    global b
    a = []
    zahl = 3
    while True:
        a.append(zahl)
        print(a)
        b = {
            'zahl': a
        }
        time.sleep(1.0)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print('Programm startet')
    try:
        loop()
    except KeyboardInterrupt:
        print('Programm beendet')
        with open('Test_Json.txt', 'w') as datei:
            json.dump(b, datei)