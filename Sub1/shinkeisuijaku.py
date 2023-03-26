# Time-stamp: <2022-10-21 15:19:29 uchik>

""" shinkeisuijaku.py: 神経衰弱
"""
#!/usr/bin/env python
# coding: utf-8
import pyxel, random

Nsize = 4
Glen = 120//Nsize
DD = Glen * 9 // 20

class App:
    def resetgame(self):
        self.nums = list(range(1, Nsize*Nsize//2 + 1))
        self.nums *= 2
        if Nsize % 2: self.nums.append(0)
        random.shuffle(self.nums)
        self.headp = [0] * len(self.nums)
        self.doneL = [0 if v else 1 for v in self.nums]
        self.openpos = -1       # 1枚表になってる場所
        self.hist = [ ]
    
    def __init__(self):
        pyxel.init(Glen * Nsize, Glen * Nsize + 20, "神経すいじゃく")
        pyxel.mouse(True)
        self.resetgame()
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            cx, cy = pyxel.mouse_x // Glen, pyxel.mouse_y // Glen
            if 0<=cx<Nsize and 0<=cy<Nsize:
                pos = cy*Nsize + cx
                if not self.headp[pos]:
                    self.headp[pos] = 1
                    self.hist.append(pos)
                    if self.openpos == -1:
                        self.openpos = pos
                    elif self.nums[pos] == self.nums[self.openpos]:
                        self.doneL[pos] = self.doneL[self.openpos] = 1
                        self.openpos = -1
                    else:
                        self.openpos = -1
                else:
                    self.headp[pos] = 0
            print(len(self.hist), self.openpos, self.nums)
                
    def draw(self):
        pyxel.cls(7) 
        for j in range(Nsize):
            for i in range(Nsize):
                pos = j*Nsize+i
                if self.headp[pos]:
                    pyxel.rect(Glen*i, Glen*j, Glen, Glen, 11) 
                    pyxel.text(i*Glen+DD, j*Glen+DD, str(self.nums[pos]), 1)
                if self.doneL[pos]:
                    pyxel.rect(Glen*i, Glen*j, Glen, Glen, 10) 
                    pyxel.text(i*Glen+DD, j*Glen+DD, str(self.nums[pos]), 8)
                pyxel.line(Glen*i, 0, Glen*i, Glen*Nsize, 0)
            pyxel.line(0, Glen*j, Glen*Nsize, Glen*j, 0)
        pyxel.line(0, Glen*Nsize, Glen*Nsize, Glen*Nsize, 0)
        if sum(self.doneL) == len(self.doneL):
            pyxel.text(10, Glen*Nsize+8,
                       f"Congrats! ({len(self.hist)} steps)", 8)
# Main ===============================-
App()

# 0=くろ, 1=こいあお, 2=むらさき, 3=みどり, 4=ちゃいろ, 5=あお
# 6=みずいろ, 7=しろ, 8=あか, 9=オレンジ, 10=きいろ, 11=うすいみどり
# 12=うすいあお, 13=はいいろ, 14=ピンク, 15=はだいろ
