# Time-stamp: <2023-02-27 14:36:59 uchik>

#!/usr/bin/env python
# coding: utf-8

""" 画像タイピング using streamlit
needs: pip install streamlit
"""

import glob, random, pathlib
import streamlit as st
from PIL import Image

def gonext():
    idx = st.session_state.idx
    if input := st.session_state.txt:
        ans = st.session_state.ans
        if input.lower() == ans.lower():
            st.write(f'{idx}: "{ans}" Correct!')
            st.session_state.point += 1
        else:
            st.write(f'{idx}: It is not "{input}", but "{ans}"')
    st.session_state.txt  = ''  # to clear text_input box
    st.session_state.idx += 1
    st.write(f'Score: {st.session_state.point} / {st.session_state.idx}')

def main():
    imgArea = st.empty()
    idx = st.session_state.idx
    pic = st.session_state.picL[idx]
    pf = pathlib.Path(pic)
    ans = st.session_state.ans = pf.parent.name
    print(idx, ans, pf.name)
    
    st.text_input('What is this?', '', key='txt', on_change=gonext)
    img = Image.open(pic)
    img.thumbnail((250, 250), Image.LANCZOS)
    imgArea.image(img) #, caption = pf.name)
        
if __name__ == "__main__":
    if not 'idx' in st.session_state:
        st.session_state.idx = 0
        imgdir = './Imagefolder/'
        if not pathlib.Path(imgdir).exists(): sys.exit(0)
        dirL = glob.glob(imgdir+'*')
        picL = [f for d in dirL for f in glob.glob(d+'/*')]
        random.shuffle(picL)
        print(len(picL), [pathlib.Path(f).parent.name for f in picL[:3]])
        st.session_state.picL = picL
        st.session_state.point = 0
        
    main()
    
