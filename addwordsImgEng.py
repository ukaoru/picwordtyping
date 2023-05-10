# Time-stamp: <2023-05-10 21:30:15 uchik>

#!/usr/bin/env python
# coding: utf-8

""" 収集画像を確認しNewImagefolderに収容
needs: pip install pillow (as admin)
needs: pip install icrawler pysimplegui
"""
import os, sys, glob, shutil
from PIL import Image, ImageTk
from icrawler.builtin import BingImageCrawler
from icrawler.builtin import GoogleImageCrawler
import PySimpleGUI as sg

picN = 6
savedir = './NewImagefolder/'
if not os.path.exists(savedir): os.mkdir(savedir)
tmpdir = savedir + 'TmpNewWord/'
if not os.path.exists(tmpdir): os.mkdir(tmpdir)
picL = [''] * picN
swd = ''
sg.set_options(font=('Arial Bold', 25), text_color='black',
               background_color='grey')
# ------------------------------

def asksword():
    global swd
    layout2 = [[ sg.InputText(key='txt1', size=(15, 5),
                              font=('arial', 30)),
                 sg.Button('Search')],
               [ sg.Button('Exit') ]
    ]
    win2 = sg.Window('Type an English word to add', layout2)
    event2, vals2 = win2.read()
    if event2 == sg.WINDOW_CLOSED or event2 == 'Exit':
        sys.exit(0)
    if event2 == "Search":
        win2.close()
        print(f"vals2 = {vals2}")
        swd = vals2['txt1'].lower()
    return swd
    
def getpicL():
    """ return image filelist """
    global swd
    for f in glob.glob(savedir + 'TmpNewWord/*.*'):
        os.remove(f)
    dir = tmpdir
    if True:
        swd = asksword()
        #crawler = BingImageCrawler(storage={'root_dir': dir},
        crawler = GoogleImageCrawler(storage={'root_dir': dir},
                                     downloader_threads=4)
        crawler.crawl(keyword=swd, max_num=picN, #max_size=(600,600), 
                      filters={'type':'photo', 'size': 'medium'})
        picL0 = glob.glob(dir + '*.jpg')
        for f in picL0:
            sz1 = os.path.getsize(f)
            img = Image.open(f)
            img.thumbnail(size=(250, 250))
            f2 = f[:-4]+'.png'
            img.save(f2 , format="PNG")
            f3 = f[:-4]+'T.jpg'
            img.save(f3)
            sz2 = os.path.getsize(f2)
            sz3 = os.path.getsize(f3)
            print(f2, sz1, sz2, sz3)
            del img
        picL = glob.glob(dir + '*.png')
        print([os.path.basename(f) for f in picL])
    return picL

def savePics(picL, selL):
    dir = savedir + swd 
    if not os.path.exists(dir): os.mkdir(dir)
    for idx in selL:
        dstfn = picL[idx][:-4] + 'T.jpg'
        shutil.copy2(dstfn, dir)
        print("copy", idx, dstfn, dir)

# ------------------------------

szimg = (300, 200)
szcb = (13, 3)                  # 
while True:
    picL = getpicL()
    layout = [
        [sg.Text(f'"{swd}": Check only good images',
                 font=('arial', 30)), sg.Button('Submit') ],
        [sg.Image(filename=picL[n], size=szimg) for n in range(3)],
        [sg.Checkbox(f'{swd} {n}', key=f'C{n}', size=szcb)
         for n in range(3)],
           [sg.Image(filename=picL[n], size=szimg)
            for n in range(3, len(picL))],
           [sg.Checkbox(f'{swd} {n}', key=f'C{n}', size=szcb)
            for n in range(3, len(picL))]
    ]
    window = sg.Window('Add new words to ImageEnglish', layout,
                       size=(1000, 650))
    event, vals = window.read()

    if event == sg.WINDOW_CLOSED:
        sys.exit(0)
    if event == 'Submit':
        selL = [ ]
        for k in vals:
            if k.startswith('C') and vals[k]: selL.append(int(k[1]))
        msg = f'Are you sure with these {len(selL)} images? {selL}'
        if sg.popup_yes_no(msg).startswith('Y'):
            window.close() 
            savePics(picL, selL)
            swd = ''

# ------------------------------
