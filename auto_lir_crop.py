#!/usr/bin/env python
#coding: UTF-8
import pandas as pd
#import numpy as np
import os,fnmatch

#file_load
PATH = '.'
def calc(filename):
    head = ["ElapsedCnt","DateTime","ElapsedTime","Event","ExtTrgEvent","ZeroSet","CH1_PR","CH1_BF","CH1_Doxy","CH1_Ddeoxy","CH1_Dtotal","CH1_735nm","CH1_810nm","CH1_850nm","CH1_DARK","CH2_PR","CH2_BF","CH2_Doxy","CH2_Ddeoxy","CH2_Dtotal","CH2_735nm","CH2_810nm","CH2_850nm","CH2_DARK"]
    df = pd.read_csv(filename,skiprows=1,names=head)
    #calc 右脳-左脳(CH2-CH1)
    lir = ((df.CH2_Doxy - df.CH2_Doxy.min()) - (df.CH1_Doxy - df.CH1_Doxy.min())).sum() / ((df.CH2_Doxy - df.CH2_Doxy.min()) + (df.CH1_Doxy - df.CH1_Doxy.min())).sum()
    return lir

#file_search
def find(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result

#path_search
def findpath(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in dirs:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result

def exportfile():
    lir_tmp = []
    try:
        lir_tmp.append(calc(find("preopen-nirs*",PATH)[0]))
    except:
        print("preopen-nirsファイルが見つかりません")
    try:
        lir_tmp.append(calc(find("preclose-nirs*",PATH)[0]))
    except:
        print("preclose-nirsファイルが見つかりません")
    try:
        lir_tmp.append(calc(find("write-nirs*",PATH)[0]))
    except:
        print("write-nirsファイルが見つかりません")
    try:
        lir_tmp.append(calc(find("postclose-nirs*",PATH)[0]))
    except:
        print("postclose-nirsファイルが見つかりません")
    try:
        exp_file = pd.DataFrame({"preopen":[lir_tmp[0]],"preclose":[lir_tmp[1]],"write":[lir_tmp[2]],"postclose":[lir_tmp[3]]})
        TO_CSV_FILENAME = "LIR-" + os.getcwd().split("/")[-3] +"-" + find("preopen-nirs*",PATH)[0].split('-')[2]
        exp_file.to_csv(TO_CSV_FILENAME,index=False)
    except:
        pass

#main
listofpath = findpath("crop",".")
startdir = os.getcwd()
for x in listofpath:
    os.chdir(x)
    print(x+"を実行中")
    #print(os.getcwd())
    exportfile()
    print(x+"の処理終了")
    os.chdir(startdir)
