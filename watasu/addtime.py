#!/usr/bin/env python
# coding: UTF-8
import pandas as pd
# import numpy as np
import os
import fnmatch

START_TIME = "17:26:42"
END_TIME = "17:27:41"
head = ["Date", "Time", "COUNTER", "INTERPOLATED", "AF3", "F7", "F3", "FC5", "T7", "P7", "O1", "O2", "P8", "T8", "FC6", "F4", "F8", "AF4", "RAW_CQ", "CQ_AF3", "CQ_F7",
        "CQ_F3", "CQ_FC5", "CQ_T7", "CQ_P7", "CQ_O1", "CQ_O2", "CQ_P8", "CQ_T8", "CQ_FC6", "CQ_F4", "CQ_F8", "CQ_AF4", "CQ_CMS", "CQ_DRL", "GYROX", "GYROY", "MARKER"]
filename = "t_hasegawa-0-18.05.18.17.26.21.CSV"
df = pd.read_csv(filename, skiprows=1, names=head)
df_time = df["Time"]
df_time_sel = []
df_time_sel = df[(df_time >= START_TIME) & [(df_time < END_TIME)]]
# print(df)
# print(df_time)
print(df_time_sel)
df_time_sel.to_csv("tmp.csv", index=False)
