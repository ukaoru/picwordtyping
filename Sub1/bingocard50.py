# Time-stamp: <2023-03-26 08:53:05 uchik>

""" bingo5auto.py 中央は初めからワイルドカード
     ビンゴ揃いを自動検出
"""
#!/usr/bin/env python
# coding: utf-8

import sys, os, random
import datetime as dt
import pyxel

BINGO_MAX = 50                   # カードで一番大きい数字
SIZE = 32
CENTERPOS = 12
catpng = "cat.png"

# 1からmaxnumまでの整数をシャッフルし長さmaxnumのリストを返す
def genrandomseq(maxnum):
    seed = dt.datetime.now().microsecond
    random.seed(seed)
    fullL = list(range(1, BINGO_MAX + 1)) # from 1 to maxnum
    return random.sample(fullL, len(fullL))

class App:
    def __init__(self):
        pyxel.init(SIZE * 5, SIZE * 5 + 20, "ビンゴカード")
        if os.path.exists(catpng): 
            pyxel.image(0).load(0, 0, catpng)
        pyxel.mouse(True)

        idxL = genrandomseq(BINGO_MAX)[:24] # 先頭の24個をとる
        idxL.insert(CENTERPOS, 0)          # 中央に0を入れる
        self.bingoL = idxL  #[str(n) for n in idxL]
        #for i in range(5):
            #print(self.bingoL[i*5:i*5+5])
        self.doneL = [ CENTERPOS ] # 中央は最初から穴あき
        self.cpos = -1             # クリック状態にあるセル

        self.foundbingoL = [ ]
        self.checkL = [ ]            # [start, interval] pairs
        for i in range(5):      # vertical
            self.checkL.append([i, 5])
        for i in range(0, 25, 5):      # horizontal
            self.checkL.append([i, 1])
        self.checkL += [[0, 6], [4, 4]] # diagonal
        #print(checkL)

    def run(self):
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            #pyxel.quit()
            pass
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            cx = pyxel.mouse_x // SIZE
            cy = pyxel.mouse_y // SIZE
            pos = cy*5 + cx
            #print(pos, self.bingoL[pos], f"(cpos {self.cpos})")
            if pos == self.cpos:
                if pos in self.doneL:
                    self.doneL.remove(pos)
                else:
                    self.doneL.append(pos)
                self.cpos = -1
                self.findbingo()
            elif pos != CENTERPOS: # 中央でなければ
                self.cpos = pos
            #print(self.bingoL[pos])
                
    def draw(self):
        pyxel.cls(11)           # lightGreen 色をかえる
        mx = (pyxel.mouse_x // SIZE) * SIZE
        my = pyxel.mouse_y // SIZE * SIZE
        pyxel.rect(mx, my, SIZE, SIZE, 12) # lightBlue 色をかえる
        if self.cpos >= 0:
            pyxel.rect(self.cpos%5*SIZE, self.cpos//5*SIZE,
                       SIZE, SIZE, 10) # yellow
        for j in range(5):
            for i in range(5):
                pos = j * 5 + i
                if pos == CENTERPOS:
                    pyxel.blt(i*SIZE+6, j*SIZE+6, 0, 0, 0, 16, 16, 14) 
                else:
                    pyxel.text(i*SIZE+12, j*SIZE+12, str(self.bingoL[pos]), 1)
                if pos in self.doneL:
                    pyxel.circb(i*SIZE+14, j*SIZE+14, 10, 8) # red

        pyxel.line(0, SIZE*5, SIZE*5, SIZE*5, 1)
        if self.foundbingoL:
            pyxel.text(10, SIZE*5+8,
                       f"Bingo! ({len(self.foundbingoL)})", 8)

    def findbingo(self):
        foundL = []
        for p in self.checkL:
            seqL = []
            for k in range(5):
                if (pos := p[0]+p[1]*k) not in self.doneL: break
                seqL.append(pos)
            else:
                found = [self.bingoL[n] for n in seqL]
                foundL.append(found)
        self.foundbingoL = foundL
        if self.foundbingoL:
            print(len(self.foundbingoL), self.foundbingoL)


# ゲームの実行 ===============================-
if len(sys.argv) > 1: # 後ろに引数があったら読み手用
    fullL = genrandomseq(BINGO_MAX)
    print("読み手用:", fullL)
    sys.exit(0)
    
App().run()

# 0=くろ, 1=こいあお, 2=むらさき, 3=みどり, 4=ちゃいろ, 5=あお
# 6=みずいろ, 7=しろ, 8=あか, 9=オレンジ, 10=きいろ, 11=うすいみどり
# 12=うすいあお, 13=はいいろ, 14=ピンク, 15=はだいろ
