# Time-stamp: <2023-05-26 14:34:51 uchik>

#!/usr/bin/env python
# coding: utf-8

""" addcalcgame.py : number adding game
needs: pip install streamlit, gTTS
requires: gTTS
"""
import random
import streamlit as st
import gtts                     # Google TTS for pronunciation
import base64, time             # for pronunciation autoplay

uplim = 9                       # 20230513 sakamoto

# autoplay pronunciation
def soundautoplay(audiofile):
    audio_placeholder = st.empty()
    with open(audiofile, "rb") as f:
        contents = f.read()
    audioS = "data:audio/ogg;base64,%s"%(base64.b64encode(contents).decode())
    audio_html = """<audio autoplay=True>
                    <source src="%s" type="audio/ogg"></audio>"""%audioS
    #audio_placeholder.empty()
    time.sleep(0.5)             # need this
    audio_placeholder.markdown(audio_html, unsafe_allow_html=True)

def speaktext(txt, lang='en'):
    tmpaudiofile = '_tmp.mp3'
    gtts.gTTS(txt, lang=lang).save(tmpaudiofile)
    soundautoplay(tmpaudiofile)
    #st.audio(tmpaudiofile)
    
# go to the next image, called by the next button
def gonext():
    st.session_state.idx += 1
    giveprob()

# show a question and ask, called from init and gonext()
def giveprob():
    #uplim = (10**st.session_state.level)//2 - 1
    x = st.session_state.x = random.randint(1, uplim)
    y = st.session_state.y = random.randint(1, uplim)
    #st.session_state.ans = x + y
    st.session_state.ans = x - y
    msg = f'What is {x} - {y} ?'
    msg2 = f'What is {x} minus {y} ?'
    speaktext(msg2)
    st.text_input(msg, '', key='txt', on_change=checkans)
    st.write(f'Score: {st.session_state.point} / {st.session_state.idx}')
    #print(st.session_state.idx, st.session_state.ans)

# check the answer, called by the text_input ENTER
def checkans():
    idx, ans = st.session_state.idx, st.session_state.ans
    x, y = st.session_state.x, st.session_state.y 
    if inp := st.session_state.txt:
        if inp.replace('-', '').isdigit() and int(inp) == ans:
            msg = f'Correct! {x} - {y} = {ans}.'
            st.write(msg)
            speaktext(msg)
            st.session_state.point += 1
        else:
            msg = f'Wrong.  {x} - {y} = {ans}, not {inp}.'
            st.write(msg)
            speaktext(msg)
        st.session_state.txt  = ''  # to clear text_input box
        if idx % 10 == 9: st.balloons()
    else:
        st.write(f'{idx}: This is "{ans}"')
    st.button("Next", on_click=gonext)
    st.write(f'Score: {st.session_state.point} / {idx+1}')

# --------------- main start
if __name__ == "__main__":
    # executed only once at the beginning
    if not 'idx' in st.session_state:
        st.session_state.level = 2
        st.session_state.point = st.session_state.idx = 0
        giveprob()
        st.markdown('&copy; 2023 NPO Challengepro')
# --------------- main end            
    
