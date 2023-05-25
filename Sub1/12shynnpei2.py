
import pyxel
import time
import os
SIZE = 50

def speaktext(txt, lang='en'):
    """
    import gtts, playsound
    tmpaudiofile = '_tmp.mp3'       
    gtts.gTTS(txt, lang=lang).save(tmpaudiofile)
    playsound.playsound(tmpaudiofile)
    os.remove(tmpaudiofile)    
    """
    pass

d = [[] * 4] * 4
d[0] = list(' BTU')
d[1] = list('MLOE')
d[2] = list('FYAH')
d[3] = list('SRPK')

ans = [[] * 4] * 4
ans[0] = list('BLUE')
ans[1] = list('MATH')
ans[2] = list('FORK')
ans[3] = list('SPY ')

class App:
    def __init__(self):
        pyxel.init(SIZE * 4, SIZE * 4, "ジグソーパズル")
        pyxel.mouse(True)
        self.white_x = 3
        self.white_y = 3
        self.kaisuu = 0
        self.soroi = [0,0,0,0]
        print("kotae    BLUE MATH FORK SPY ")
        self.hazime = time.time()
        pyxel.run(self.update, self.draw)
        
    def update(self):
        pass
        
    def draw(self):
        pyxel.cls(4)           # skincolor
        for i in range(3):
            pyxel.line(0, SIZE*(i+1), SIZE*4, SIZE*(i+1), 3)
            pyxel.line(SIZE*(i+1), 0, SIZE*(i+1), SIZE*4, 3)
            
        for i in range(4):
            for j in range(4):
                pyxel.text(25+i*SIZE, 25+j*SIZE, d[j][i], 10)
                if d[j][i] == ' ':
                    akix = i
                    akiy = j
        for k in range(4):
            if d[k] == ans[k]:
                if self.soroi[k] == 0:
                    self.soroi[k] = 1
                    print(k,"gyoume","sorotta!")
                    text = f'{k+1} line OK.' 
                    print(text)
                    speaktext(text)
                for i in range(4):
                    pyxel.text(25+i*SIZE, 25+k*SIZE, d[k][i], 12)
        if d[0] == ans[0] and d[1] == ans[1] and d[2] == ans[2] and d[3] == ans[3] and self.hazime != 0:
            print("kannseisitayo")
            self.owari = time.time()
            print(f'{self.owari - self.hazime:.1f}sec')
            self.hazime = 0
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            btnx,btny = pyxel.mouse_x//50,pyxel.mouse_y//50 
            self.kaisuu += 1
            print(pyxel.mouse_x//50, pyxel.mouse_y//50,
                  d[pyxel.mouse_y//50][pyxel.mouse_x//50],
                  self.kaisuu)
            if (btnx == akix + 1 and btny == akiy) or (btny == akiy + 1 and btnx == akix) or (
                btnx == akix - 1 and btny == akiy) or btny == akiy - 1 and btnx == akix:
                d[akiy][akix] = d[btny][btnx]
                d[btny][btnx] = ' '

App()           

# 0=くろ, 1=こいあお, 2=むらさき, 3=みどり, 4=ちゃいろ, 5=あお
    # 6=みずいろ, 7=しろ, 8=あか, 9=オレンジ, 10=きいろ, 11=うすいみどり
# 12=うすいあお, 13=はいいろ, 14=ピンク, 15=はだいろ
