# Time-stamp: <2023-03-24 21:41:02 uchik>

""" eightpuzzle.py (8パズル、または15パズル)
 空きマスの隣をクリックして動かす
 実行時に問題を指定可能 python eightpuzzle.py 123456708 (0がアキ)  
"""
#!/usr/bin/env python
# coding: utf-8

import sys, os, random
import datetime as dt
import pyxel

three = 3                       # 4 in case of 15-puzzle
nine = three**2
SIZE = 50

seed = dt.datetime.now().microsecond
random.seed(seed)

def genprob():
    fullL = list(range(nine)) # from 0 to 8
    random.shuffle(fullL)
    return fullL

def invnum(prob):              # inversion number in permutation
    err = 0
    for i in range(nine):
        err += sum([int(prob[j]>prob[i]) for j in range(i)])
    return abs(err - 8)

def l1norm(p1, p2):
    x1, y1 = p1 % three, p1 // three
    x2, y2 = p2 % three, p2 // three
    return abs(x1-x2) + abs(y1-y2)

# ===============================-
class App:
    def __init__(self, prob):
        self.stat = prob
        pyxel.init(SIZE * three, SIZE * three + 20, "8パズル")
        pyxel.mouse(True)
        self.hist = [ self.stat ]
        self.completed = False
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            cx, cy = pyxel.mouse_x // SIZE, pyxel.mouse_y // SIZE
            pos = cy*three + cx
            if l1norm(pos, self.stat.index(0)) == 1:
                newstat = self.stat.copy()
                newstat[newstat.index(0)] = newstat[pos]
                newstat[pos] = 0
                self.stat = newstat
                self.hist.append(newstat)
                #parity, dist = invnum(newstat), l1norm(newstat.index(0), 8)
                #print(len(self.hist)-1, newstat, parity, dist, parity-dist)
            if self.stat == [(n+1)%nine for n in range(nine)]:
                print("Congratulations!")
                self.completed = True
    
    def draw(self):
        pyxel.cls(15)           # skincolor
        offset = SIZE*9//20
        mx = (pyxel.mouse_x // SIZE) * SIZE
        my = (pyxel.mouse_y // SIZE) * SIZE
        if l1norm(my//SIZE*three+mx//SIZE, self.stat.index(0)) == 1:
            pyxel.rect(mx, my, SIZE, SIZE, 12) # lightBlue
        for j in range(three):
            pyxel.line(0, SIZE*j, SIZE*three, SIZE*j, 0)
            for i in range(three):
                pyxel.line(SIZE*i, 0, SIZE*i, SIZE*three, 0)
                pos = j * three + i
                if (num := self.stat[pos]) > 0:
                    pyxel.text(i*SIZE+offset, j*SIZE+offset, str(num), 1)
        pyxel.line(0, SIZE*three, SIZE*three, SIZE*three, 0)
        if self.completed:
            pyxel.text(10, SIZE*three+8,
                       f"Congratulations! ({len(self.hist)-1} steps)", 8)


# ゲームの実行 ===============================-
if len(sys.argv) > 1: # 後ろに問題があったら
    prob = [int(c, 16) for c in sys.argv[1]] # hex for 15-puzzle
    parity, dist = invnum(prob), l1norm(prob.index(0), 8)
    if (parity-dist)%2:
        print(prob, parity, dist, "Unsolvable: 解けない問題です")
        sys.exit(1)
else:
    while True:                 # 解ける問題が生成されるまでループ
        prob = genprob()        
        parity, dist = invnum(prob), l1norm(prob.index(0), 8)
        if (parity-dist)%2 == 0: break
        print('Unsolvable', prob, parity, dist, parity-dist)
    
print(''.join([str(n) for n in prob]))
#print(0, prob, parity, dist, parity-dist)
App(prob)
