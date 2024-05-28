import streamlit as st
import pandas as pd
import gtts
import random, os

fname = 'sound.mp3'

def speaktext(txt, lang='en'):
    gtts.gTTS(txt).save(fname)
    st.audio(fname)

def ask():
    st.session_state.prob = prob = random.choice(st.session_state.qL)   
    msg = f'The capital of {prob}  ? '
    speaktext(msg)
    st.text_input(msg, '', key='inp', on_change=check)

def check():
    prob = st.session_state.prob
    inp = st.session_state.inp
    ans = st.session_state.D[prob]['Capital']
    st.session_state.idx += 1
    msg = f'Wrong. It is {ans}, not {inp}.'
    if inp.lower() == ans.lower():
        msg = f'Correct. {inp} is the capital of {prob}.'
        st.session_state.point += 1
    st.write(msg)
    speaktext(msg)
    st.write(f'Point is {st.session_state.point} / {st.session_state.idx}')
    st.button('Next', on_click=ask)

# ----------
if not 'idx' in st.session_state:
    file = 'worldcapitals.xlsx'
    dirname =  os.path.dirname(__file__)
    file = dirname + '/' + file
    df = pd.read_excel(file, index_col='Country')[:40]
    st.session_state.D = D = df.to_dict(orient='index')
    st.session_state.qL = list(D)
    st.session_state.idx = st.session_state.point = 0
    
    ask()
    

