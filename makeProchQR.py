# Time-stamp: <2023-05-11 17:25:04 uchik>

#!/usr/bin/env python
# coding: utf-8

""" makeProchQR.py w/ streamlit
needs: pip install streamlit qrcode
"""

import datetime as dt
import qrcode
import streamlit as st
from PIL import Image

def inpstr():
    if input := st.session_state.txt:
        pic = '_tmpQR.png'
        prstr = dt.datetime.now().strftime('%D %R')
        msg = f'{input} @ {prstr} (プロチャレ2023)'
        print(msg)
        qrcode.make(msg).save(pic)
        img = Image.open(pic)
        img.thumbnail((200, 200), Image.Resampling.LANCZOS)
        st.image(img)
        st.write('msg')
        st.write(f'スクショ後に画面を閉じてください')

# --------------- main start
if __name__ == "__main__":
    # executed only once at the beginning
    if not 'txt' in st.session_state:
        st.text_input('名前などIDとなる文字列を入力してください?', '',
                      key='txt', on_change=inpstr)

# --------------- main end            
    
