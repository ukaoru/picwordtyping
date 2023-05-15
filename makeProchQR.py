# Time-stamp: <2023-05-15 11:20:55 uchik>

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
        #prstr = dt.datetime.now().strftime('%c')
        msg = f'{input} @ プロチャレ2023'
        print(msg)
        qrcode.make(msg).save(pic)
        img = Image.open(pic)
        img.thumbnail((200, 200), Image.Resampling.LANCZOS)
        st.image(img)
        st.write(msg)
        st.write(f'スクショ後に画面を閉じてください')
        with open('record.txt', mode='a') as f:
            f.write('\n'+msg)      

# --------------- main start
if __name__ == "__main__":
    # executed only once at the beginning
    if not 'txt' in st.session_state:
        st.text('「V+V番号+名前+読み仮名」を入力して「Enter」')
        st.text('　　　(V番号は、スタッフ予定表の一番左の列)')
        st.text_input('(例「V05 神谷王子 かみやおうこ」) ',
                      '', key='txt', on_change=inpstr)
        #st.button("Submit", on_click=inpstr)

# --------------- main end            
    
