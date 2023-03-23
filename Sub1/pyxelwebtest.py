# Time-stamp: <2022-07-30 15:06:09 kaoru>

""" suikawariKB.py 方向キー版のスイカ割り
"""
#!/usr/bin/env python
# coding: utf-8

import os
import pyxel

CN1 = 7                         # 縦横のセル数
CSIZE = 16
catpng = "cat.png"

class App:
    def __init__(self):
        pyxel.init(CSIZE*(CN1+1), CSIZE*(CN1+1) + 20, "スイカわり",
                   fps = 5)     # チャタリング抑制にはfps=5など
        if os.path.exists(catpng): 
            pyxel.image(0).load(0, 0, catpng)
        self.suika_x = pyxel.rndi(1, CN1)  # スイカのx座標 
        self.suika_y = pyxel.rndi(1, CN1)  # スイカのy座標
        self.player_x = pyxel.rndi(1, CN1) # プレイヤーのx座標
        self.player_y = pyxel.rndi(1, CN1) # プレイヤーのy座標
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        self.dist = abs(self.player_x - self.suika_x) + abs(
            self.player_y - self.suika_y)
        if pyxel.btn(pyxel.KEY_LEFT) and self.player_x > 1:
            self.player_x -= 1
        if pyxel.btn(pyxel.KEY_RIGHT) and self.player_x < CN1:
            self.player_x += 1
        if pyxel.btn(pyxel.KEY_UP) and self.player_y > 1:
            self.player_y -= 1
        if pyxel.btn(pyxel.KEY_DOWN) and self.player_y < CN1:
            self.player_y += 1
    
    def draw(self):
        pyxel.cls(11)           # 
        for j in range(1, CN1+1):
            pyxel.line(CSIZE, CSIZE*j, CSIZE*CN1, CSIZE*j, 0)
            for i in range(1, CN1+1):
                pyxel.line(CSIZE*i, CSIZE, CSIZE*i, CSIZE*CN1, 0)
        pyxel.blt(self.player_x * CSIZE-8, self.player_y * CSIZE-8,
                  0, 0, 0, 16, 16, 9)
        mes, color = f"Distance: {self.dist}", 0
        if self.dist==0: mes, color = "Congratulations!", 8
        pyxel.text(10, CSIZE*(CN1+1)+8, mes, color)

# ゲームの実行 ===============================-
App()

# 0=くろ, 1=こいあお, 2=むらさき, 3=みどり, 4=ちゃいろ, 5=あお
# 6=いろ, 7=しろ, 8=あか, 9=オレンジ, 10=きいろ, 11=うすいみどり
# 12=うすいあお, 13=はいいろ, 14=ピンク, 15=はだいろ
