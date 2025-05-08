# Time-stamp: <2023-08-31 09:21:22 uchik>

#!/usr/bin/env python
# coding: utf-8

""" imageEngT.py  w/ Teacher-mode by Shaun
 use all words in Imagefolder and AddedImagefolder
needs: pip install streamlit, gTTS, SpeechRecognition
requires: gTTS, SpeechRecognition
"""

import glob, random, pathlib, sys, os
import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image
import gtts                     # Google TTS for pronunciation
import base64, time             # for pronunciation autoplay
import speech_recognition as sr

def recognize_speech(audio_value, recognition_api='google', language='en-US'):
    text = ""
    error = ""
    
    with sr.AudioFile(audio_value) as source:
        r = sr.Recognizer()
        audio_text = r.record(source)
        
        try:
            if recognition_api == 'google':
                text = r.recognize_google(audio_text, language=language)
            else:
                error = "Sorry, I did not understand that."
        except sr.UnknownValueError:
            error = "Sorry, I did not understand the speech. Please try again."
        except sr.WaitTimeoutError:
            error = "Sorry, I did hear any speech. Please try again."
        except sr.RequestError as e:
            error = f"Error: {e}. Please check your API credentials or internet connection."
        except Exception as e:
            error = f"Unexpected error: {e}. Please try again later."
    return text, error

def reset_recognized_speach_state_variables():
    st.session_state.recordingError = ""
    st.session_state.recordedText = ""
    if "recorded_answer" in st.session_state:
        del st.session_state["recorded_answer"]

tmpaudiofile = '_tmp.mp3'
# autoplay pronunciation
def soundautoplay(audiofile):
    audio_placeholder = st.empty()
    with open(audiofile, "rb") as f:
        contents = f.read()
    audioS = "data:audio/ogg;base64,%s"%(base64.b64encode(
        contents).decode())
    audio_html = """<audio autoplay=True>
                    <source src="%s" type="audio/ogg"></audio>"""%audioS
    audio_placeholder.empty()
    time.sleep(0.5)             # need this
    audio_placeholder.markdown(audio_html, unsafe_allow_html=True)


imgdir = './AddedImagefolder/'
categories = [os.path.basename(f) for f in sorted(
    glob.glob(imgdir+'*'))]


def changeCategory(key):
    curCategory = st.session_state[key]
    words = glob.glob(imgdir + curCategory + '/*')
    images = [file for word in words for file in glob.glob(
        word + '/*.jpg')]
    random.shuffle(images)
    st.session_state.images = images
    st.session_state.showAnswer = False
    st.session_state.playedAnswer = False
    reset_recognized_speach_state_variables()
    st.session_state.idx = 0

if (not 'curCategory' in st.session_state) or (
        not 'idx' in st.session_state) or (
            not 'showAnswer' in st.session_state) or (
                not 'images' in st.session_state):
    st.session_state.curCategory = categories[0]
    changeCategory("curCategory")

def decrementIndex():
    st.session_state.showAnswer = False
    st.session_state.playedAnswer = False
    reset_recognized_speach_state_variables()
    nextIdx = st.session_state.idx - 1
    if (nextIdx < 0):
        nextIdx = len(st.session_state.images) - 1
    st.session_state.idx = nextIdx

def incrementIndex():
    st.session_state.showAnswer = False
    st.session_state.playedAnswer = False
    reset_recognized_speach_state_variables()
    nextIdx = st.session_state.idx + 1
    if (nextIdx >= len(st.session_state.images)):
        nextIdx = 0
    st.session_state.idx = nextIdx


with st.sidebar:    
    option_menu("Categories", categories, on_change=changeCategory,
                key="curCategory")

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
        st.session_state.ans = pathlib.Path(
            curImageFilename).parent.name
        img = Image.open(curImageFilename)
        img.thumbnail((200, 200), Image.Resampling.LANCZOS)
        st.image(img)
    if st.button("Answer"):
        st.session_state.showAnswer = True

    if st.session_state.showAnswer:
        st.subheader(st.session_state.ans)
        gtts.gTTS(st.session_state.ans).save(tmpaudiofile)
        st.audio(tmpaudiofile)
        if not st.session_state.playedAnswer:
            st.session_state.playedAnswer = True
            soundautoplay(tmpaudiofile)
            reset_recognized_speach_state_variables()

    audio_value = st.audio_input("Record (must press stop manually)", key="recorded_answer")
    if audio_value:
        recognition_api = "google"
        language = "en-US"
        with st.spinner("Working..."):
            text, error = recognize_speech(audio_value, recognition_api, language)
            st.session_state.recordedText = text
            st.session_state.recordingError = error
        
        if st.session_state.recordingError != "":
            st.write(st.session_state.recordingError)
        elif st.session_state.recordedText != "":
            st.write("What was heard: ", st.session_state.recordedText)
            if st.session_state.recordedText.lower() == st.session_state.ans:
                st.write("BINGO")
            else:
                st.write("ERROR")


st.markdown('&copy; 2023 NPO Challengepro')
