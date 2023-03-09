# Time-stamp: <2023-03-09 09:49:07 uchik>

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

# show an image
def showimg():
    pic = st.session_state.picL[st.session_state.idx]
    st.session_state.ans = pathlib.Path(pic).parent.name
    img = Image.open(pic)
    img.thumbnail((200, 200), Image.Resampling.LANCZOS)
    st.image(img)

# go to the next image, called by the next button
def gonext():
    st.session_state.idx += 1
    st.text_input('What is this?', '', key='txt', on_change=checkspell)
    showimg()
    st.write(f'Score: {st.session_state.point} / {st.session_state.idx}')
    print(st.session_state.idx, st.session_state.ans)

# check the spelling, called by the text_input ENTER
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
    gtts.gTTS(ans).save(tmpaudiofile)
    st.audio(tmpaudiofile)
    st.write(f'Score: {st.session_state.point} / {idx+1}')
    if idx % 20 == 19: st.balloons()
    st.button("Next", on_click=gonext)

# --------------- main start
if __name__ == "__main__":
    # executed only once at the beginning
    if not 'idx' in st.session_state:
        imgdir = './Imagefolder/'
        if not pathlib.Path(imgdir).exists(): sys.exit(0)
        dirL = glob.glob(imgdir+'*')
        picL = [f for d in dirL for f in glob.glob(d+'/*')]
        random.shuffle(picL)
        st.session_state.picL = picL
        st.session_state.point = st.session_state.idx = 0
        infostr = f'Nwords: {len(dirL)}, Npics: {len(picL)}'
        print(infostr)
        #print(len(picL), [pathlib.Path(f).parent.name for f in picL[:3]])

        st.text_input('What is this?', '', key='txt', on_change=checkspell)
        showimg()
        print(st.session_state.idx, st.session_state.ans)
        st.write(infostr)
# --------------- main end            
    
