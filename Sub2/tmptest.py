# Time-stamp: <2023-05-11 17:11:22 uchik>

#!/usr/bin/env python
# coding: utf-8

""" makeProchQR.py w/ streamlit
needs: pip install streamlit qrcode
"""

import datetime as dt
import qrcode
import streamlit as st

def inpstr(input):
    prstr = dt.datetime.now().strftime('%D %R')
    msg = f'{input} @ {prstr} (プロチャレ2023)'
    print(msg)
    img = qrcode.make(msg).save('_tmpQR.png')        

# --------------- main start
if __name__ == "__main__":
    # executed only once at the beginning
    sss = input('名前などIDとなる文字列を入力してください? >')
    inpstr(sss)
    
# --------------- main end            
    
