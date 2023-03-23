# Time-stamp: <2022-08-02 06:26:47 uchik>

""" tower1c.py 描画頻度を設定可能
"""
# coding: utf-8
import pyxel
fps = 5                         # 1/fps = 0.2sec毎に再描画

def redrawtower(n):
    pyxel.cls(7)
    pyxel.trib(120, 10, 100, 100, 140, 100, 0)
    cx, cy = 70-50*pyxel.cos(n), 90-50*pyxel.sin(n)
    pyxel.circ(cx, cy, 10, 8)
    pyxel.line(cx, cy, 70, 90, 10)
    pyxel.line(30, 90, 70, 90, 9)
    pyxel.rect(90, cy, 60, 10, 5)
    pyxel.text(103, cy+2, f'{pyxel.frame_count} frames', 10)

class App:
    def __init__(self):
        pyxel.init(200, 100, "動くタワーとお日さまC", fps)
        pyxel.mouse(True)
        self.deg = 0
        pyxel.run(self.update, self.draw)
    def update(self):
        pass
    def draw(self):
        if self.deg < 80 and pyxel.frame_count % fps == 0:
            self.deg += 10 
        redrawtower(self.deg)

# ======================
App()
        
