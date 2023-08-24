# Time-stamp: <2023-06-24 11:13:28 uchik>

#!/usr/bin/env python
# coding: utf-8

""" engwordlesson.py = Picwordtyping ｰ using streamlit
 use limited-scale word list
needs: pip install streamlit, gTTS
requires: gTTS
"""

import glob, random, pathlib, sys, os
import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image
import gtts                     # Google TTS for pronunciation
import base64, time             # for pronunciation autoplay
import sys

tmpaudiofile = '_tmp.mp3'
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
    

imgdir = './AddedImagefolder/'
categories = [os.path.basename(f) for f in sorted(glob.glob(imgdir+'*'))]


def changeCategory(key):
    curCategory = st.session_state[key]
    words = glob.glob(imgdir + curCategory + '/*')
    images = [file for word in words for file in glob.glob(word + '/*.jpg')]
    random.shuffle(images)
    st.session_state.images = images
    st.session_state.showAnswer = False
    st.session_state.idx = 0
    
if (not 'curCategory' in st.session_state) or (not 'idx' in st.session_state) or (not 'showAnswer' in st.session_state) or (not 'images' in st.session_state):
    st.session_state.curCategory = categories[0]
    changeCategory("curCategory")

def decrementIndex():
    st.session_state.showAnswer = False
    nextIdx = st.session_state.idx - 1
    if (nextIdx < 0):
        nextIdx = len(st.session_state.images) - 1
    st.session_state.idx = nextIdx

def incrementIndex():
    st.session_state.showAnswer = False
    nextIdx = st.session_state.idx + 1
    if (nextIdx >= len(st.session_state.images)):
        nextIdx = 0
    st.session_state.idx = nextIdx


with st.sidebar:    
    option_menu("Categories", categories, on_change=changeCategory, key="curCategory")

st.header(st.session_state.curCategory)

prevCol, mainCol, nextCol = st.columns(3)

with prevCol:
    st.button("<", on_click=decrementIndex, use_container_width=True)

with nextCol:
    st.button("\>", on_click=incrementIndex, use_container_width=True)

with mainCol:
    index = st.session_state.idx
    if (index >= 0 and index < len(st.session_state.images)):
        curImageFilename = st.session_state.images[index]
        st.session_state.ans = pathlib.Path(curImageFilename).parent.name
        img = Image.open(curImageFilename)
        img.thumbnail((200, 200), Image.Resampling.LANCZOS)
        st.image(img)
    if st.button("Answer"):
        st.session_state.showAnswer = True

    if st.session_state.showAnswer:
        st.subheader(st.session_state.ans)
        gtts.gTTS(st.session_state.ans).save(tmpaudiofile)
        soundautoplay(tmpaudiofile)
        st.audio(tmpaudiofile)


st.markdown('&copy; 2023 NPO Challengepro')
