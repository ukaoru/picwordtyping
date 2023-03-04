# Time-stamp: <2023-03-04 16:18:29 hermite>

#!/usr/bin/env python
# coding: utf-8

""" wtypegame = Picwordtyping ｰ using streamlit
needs: pip install streamlit, gTTS
requires: gTTS
"""

import glob, random, pathlib
import streamlit as st
from PIL import Image
import gtts                     # Google TTS for pronunciation

def gonext():
    st.session_state.idx += 1
    st.session_state.ans = ''
    st.text_input('What is this?', '', key='txt', on_change=checkspell)
    showimg()
    print(st.session_state.idx, st.session_state.ans)

def showimg():
    pic = st.session_state.picL[st.session_state.idx]
    st.session_state.ans = pathlib.Path(pic).parent.name
    img = Image.open(pic)
    img.thumbnail((250, 250), Image.Resampling.LANCZOS)
    st.image(img)
    
def checkspell():
    tmpaudiofile = '_tmp.mp3'
    showimg()
    idx, ans = st.session_state.idx, st.session_state.ans
    if input := st.session_state.txt:
        if input.lower() == ans.lower():
            st.write(f'{idx}: "{ans}" Correct!')
            st.session_state.point += 1
        else:
            st.write(f'{idx}: It is not "{input}", but "{ans}"')

    st.session_state.txt  = ''  # to clear text_input box
    tts = gtts.gTTS(ans)
    tts.save(tmpaudiofile)
    st.audio(tmpaudiofile)
    st.write(f'Score: {st.session_state.point} / {idx+1}')
    st.button("Next", on_click=gonext)

def main():
    if st.session_state.ans == '':
        st.text_input('What is this?', '', key='txt', on_change=checkspell)
        showimg()
        print(st.session_state.idx, st.session_state.ans)

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
        st.session_state.ans = ''

    main()
            
    
