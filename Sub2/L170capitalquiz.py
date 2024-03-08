import pandas as pd
import random as rd
import sys

areaD = { 'A': 'アジア', 'Q': '中東', 'E': '欧州',
          'I': 'NIS諸国', 'F': 'アフリカ',
          'N': '北中米', 'S': '南米', 'O': 'オセアニア' }

file = '各国リスト.xlsx'
df = pd.read_excel(file, index_col='国名')

print(df.shape)

df1 = df[:55]
D = df1.to_dict(orient='index')
#D2 = D['首都名']

#print(D)

qL = list(D)
#print(qL)

import PySimpleGUI as sg

sg.theme('Purple')
sg.set_options(font=(None, 24))

layout = [
    [ sg.T(k=80, size=(20, 1)), ],
    [ sg.I(k=81, size=(20, 1)),
      sg.B('Go', bind_return_key=True),
      sg.B('Next'),],
    [ sg.ML(k=85, size=(30, 10)), ],
    ]
win = sg.Window('Quiz', layout, finalize=1)

def ask():
    global prob, ans, txt
    prob = rd.choice(qL)
    ans = D[prob]['首都名']
    txt = areaD[ D[prob]['地域'] ] + '\n'
    txt += f'首都は{ans} \n'
    txt += f"推計人口: {D[prob]['推計人口'] : ,}人 \n"
    txt += str(D[prob]['備考']) + "\n"
    win[80].update(prob)

ask()
while True:
    e, v = win.read()
    if e is None: break
    print(e, v)
    if e=='Go':
        myans = v[81]
        msg = 'Correct!' if myans in ans else f'Wrong, 正解は{ans}'    
        win[85].update(txt)
        sg.popup_quick(msg)
        win[81].update('')
    elif e=='Next':
        ask()
_


        



    
    

