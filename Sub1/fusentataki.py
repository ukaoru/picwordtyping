# Time-stamp: <2023-03-26 15:01:58 uchik>

""" fusentataki.py : 風船たたき
      叩いて消すと2つ増える。小さくて速い方がスコアが高い
"""
#!/usr/bin/env python
# coding: utf-8
import sys, os
import pyxel

MAX_BUB_SPEED = 12
NUM_INITIAL_BUBS = 5
Max_Rad = 30

SC_W, SC_H = 400, 200
fps = 20

class Bubble:
    def __init__(self):
        # pyxel.rndi = random.randint
        self.r = pyxel.rndi(Max_Rad//3, Max_Rad)
        self.posx = pyxel.rndi(self.r, SC_W - self.r)
        self.posy = pyxel.rndi(self.r, SC_H - self.r)
        self.velx = pyxel.rndi(-MAX_BUB_SPEED, MAX_BUB_SPEED)
        self.vely = pyxel.rndi(-MAX_BUB_SPEED, MAX_BUB_SPEED)
        self.color = pyxel.rndi(1, 15)
    def update(self):
        self.r -= 0.1
        self.posx += self.velx
        self.posy += self.vely
        if self.velx < 0 and self.posx < self.r: self.velx *= -0.9
        if self.velx > 0 and self.posx > SC_W - self.r: self.velx *= -0.9
        if self.vely < 0 and self.posy < self.r: self.vely *= -0.9
        if self.vely > 0 and self.posy > SC_H - self.r: self.vely *= -0.9
    
class App:
    def __init__(self):
        # display_scale=1 だと文字が小さすぎる
        pyxel.init(SC_W, SC_H+10, title="風船たたき", fps=fps)
        #pyxel.init(SC_W, SC_H+10, title="風船たたき", fps=fps, display_scale=2)
        pyxel.mouse(True)
        self.score = 0
        self.bubL = [Bubble() for _ in range(NUM_INITIAL_BUBS)]
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            for i,bub in enumerate(self.bubL):
                dx = bub.posx - pyxel.mouse_x
                dy = bub.posy - pyxel.mouse_y
                if dx * dx + dy * dy < bub.r * bub.r * 1.44: # サービス
                    point = int((Max_Rad - bub.r) *
                                (abs(bub.velx)+abs(bub.vely)+1))
                    self.score += point
                    newbL = [Bubble() for _ in range(2)] 
                    self.bubL += newbL
                    del self.bubL[i]
                    print(len(self.bubL), i, int(bub.r), point, self.score)
                    break
        for i, bub in enumerate(self.bubL):
            bub.update()
            if bub.r < 1: del self.bubL[i]
        if pyxel.btnp(pyxel.KEY_SPACE):
            newbL = [Bubble() for _ in range(2)] 
            self.bubL += newbL

    def draw(self):
        pyxel.cls(0)
        for bub in self.bubL:
            pyxel.circ(bub.posx, bub.posy, bub.r, bub.color)
        pyxel.rect(0, SC_H, SC_W, 20, 15)
        pyxel.text(10, SC_H+2, f"Score: {self.score}", 0)
        if not self.bubL:
            pyxel.text(SC_W//2, SC_H+2, "Hit SPACE to restart", 8)

# ゲームの実行 ===============================-
App()

