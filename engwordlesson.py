# Time-stamp: <2023-06-07 15:52:22 uchik>

#!/usr/bin/env python
# coding: utf-8

""" engwordlesson.py = Picwordtyping ｰ using streamlit
 use limited-scale word list
needs: pip install streamlit, gTTS
requires: gTTS
"""

import glob, random, pathlib, sys, os
import streamlit as st
from PIL import Image
import gtts                     # Google TTS for pronunciation
import base64, time             # for pronunciation autoplay

# autoplay pronunciation
def soundautoplay(audiofile):
    audio_placeholder = st.empty()
    with open(audiofile, "rb") as f:
        contents = f.read()
    audioS = "data:audio/ogg;base64,%s"%(base64.b64encode(contents).decode())
    audio_html = """<audio autoplay=True>
                    <source src="%s" type="audio/ogg"></audio>"""%audioS
    audio_placeholder.empty()
    time.sleep(0.5)             # need this
    audio_placeholder.markdown(audio_html, unsafe_allow_html=True)

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
    askword()

# show an image and ask, called from init and gonext()
def askword():
    st.text_input('What is this?', '', key='txt', on_change=checkspell)
    showimg()
    st.button("Hint", on_click=checkspell)
    st.write(f'Score: {st.session_state.point} / {st.session_state.idx}')
    #print(st.session_state.idx, st.session_state.ans)

# check the spelling, called by the text_input ENTER
def checkspell():
    tmpaudiofile = '_tmp.mp3'
    showimg()
    idx, ans = st.session_state.idx, st.session_state.ans
    if input := st.session_state.txt:
        if input.lower() == ans.lower():
            st.write(f'{idx}: "{ans}" Correct!')
            st.session_state.point += 1
            st.button("Next", on_click=gonext)
        else:
            st.write(f'{idx}: It is not "{input}", but "{ans}"')
            st.text_input('Type yourself', '', key='txt1', on_change=gonext)
        st.session_state.txt  = ''  # to clear text_input box
        if idx % 20 == 19: st.balloons()
    else:
        st.write(f'{idx}: This is "{ans}"')
        st.text_input('Type yourself', '', key='txt1', on_change=gonext)
    st.write(f'Score: {st.session_state.point} / {idx+1}')
    gtts.gTTS(ans).save(tmpaudiofile)
    soundautoplay(tmpaudiofile)
    st.audio(tmpaudiofile)

# --------------- main start
if __name__ == "__main__":
    # executed only once at the beginning
    if not 'idx' in st.session_state:
        #imgdir = './Imagefolder/'
        imgdir = './AddedImagefolder/'
        if not pathlib.Path(imgdir).exists(): sys.exit(0)
        lessonL = [os.path.basename(f) for f
                   in sorted(glob.glob(imgdir+'*'))]
        sel = st.radio("Choose one", lessonL) 
        if st.button(label='Submit'):
            dirL = glob.glob(imgdir+sel+'/*')
            #print(dirL)
            picL = [f for d in dirL for f in glob.glob(d+'/*.jpg')]
            random.shuffle(picL)
            st.session_state.picL = picL
            st.session_state.point = st.session_state.idx = 0
            st.write(f'Nwords: {len(dirL)}, Npics: {len(picL)}')
            st.markdown('&copy; 2023 NPO Challengepro')
        
            askword()

# --------------- main end            
    
