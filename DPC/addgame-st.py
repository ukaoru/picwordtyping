import streamlit as st
import random 

def ask():
    x = st.session_state.x = random.randint(1, 10)
    y = st.session_state.y = random.randint(1, 10)
    msg = f'What is {x} + {y} ?'
    st.text_input(msg, '', key='inp', on_change=check)

def check():
    x, y = st.session_state.x, st.session_state.y
    inp = st.session_state.inp
    ans = x + y    
    st.session_state.idx += 1

    msg = f'Wrong.  {x}  + {y} = {ans}, not {inp}.'
    if inp.isdigit() and int(inp) == ans:
        msg = f'Correct! {x}  + {y} = {ans}.'
        st.session_state.point += 1
        
    st.write(msg)
    #st.session_state.inp  = ''  # to clear text_input box
    st.write(f'Score: {st.session_state.point} / {st.session_state.idx}')
    st.button("Next", on_click=ask)

# --------------- main start
if not 'x' in st.session_state:
    st.session_state.point = st.session_state.idx = 0
    ask()
# --------------- main end            
