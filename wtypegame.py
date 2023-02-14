# Time-stamp: <2023-02-14 14:33:32 uchik>

#!/usr/bin/env python
# coding: utf-8

""" 画像タイピング using streamlit
needs: pip install streamlit
"""

import os, sys, glob, random, time
import pathlib
import streamlit as st
from PIL import Image

imgdir = './Imagefolder/'
if not os.path.exists(imgdir): sys.exit(0)

dirL = glob.glob(imgdir+'*')
picL = [f for d in dirL for f in glob.glob(d+'/*')]
random.shuffle(picL)
print(len(picL), picL[:3])

def main():
    idx = 0
    ansArea = st.empty()
    imgArea = st.empty()
    for idx in range(50):
        pic = picL[idx]
        pf = pathlib.Path(pic)
        ans = pf.parent.name
        print(idx, ans, pf.name)
        img = Image.open(pic)
        img.thumbnail((300, 300), Image.LANCZOS)
        imgArea.image(img)
        ansArea.write(f'{idx}: {ans} ({pf.name})')
        time.sleep(3)

    st.balloons()
        
if __name__ == "__main__":
    main()
    
