import pandas as pd
import datetime
import numpy as np
from scipy import signal, interpolate
from tqdm import tqdm
def concat_file(str_bci,str_hot):
    data_hot = pd.read_csv(str_hot,skiprows=6)
    data_bci = pd.read_csv(str_bci,skiprows=7,names=['SampleIndex','1st_channel','2nd_channel','3rd_channel','4th_channel','5th_channel','6th_channel','7th_channel','8th_channel','x','y','z','Timestamp','ketsu'])
    
    #データ内の方を合わせる処理
    data_hot['Device time'] = pd.to_datetime(data_hot['Device time'])#datetime型に変換
    data_hot_date = data_hot['Device time'].map(lambda x: x.date())[0]#日付情報
    data_bci['Date'] = data_hot_date#日付列を追加
    data_bci = data_bci.ix[:,[0,1,2,3,4,5,6,7,8,9,10,11,14,12,13]]#列の移動
    data_bci['Date'] = data_bci['Date'].astype(str) + data_bci['Timestamp']#列の結合
    data_bci['Date'] = pd.to_datetime(data_bci['Date'])#datetime型に変換

    #どちらが先に計測を開始したか・先頭の時刻と末尾の時刻を取得
    if data_hot['Device time'].values[0] < data_bci['Date'].values[0] :
        time_head=data_bci['Date'].values[0]
        head_bci=True
        bci_head=0
    else:
        time_head=data_hot['Device time'].values[0]
        head_bci=False
        hot_head=0
    if data_hot['Device time'].values[-1] > data_bci['Date'].values[-1]:
        time_tail=data_bci['Date'].values[-1]
        tail_bci=True
        bci_tail=len(data_bci.index)
    else:
        time_tail=data_hot['Device time'].values[-1]
        tail_bci=False
        hot_tail=len(data_hot.index)

    #同時刻の検索（開始・終了）
    head_index=0
    tail_index=-1
    if head_bci==True:
        while time_head>data_hot['Device time'].values[head_index]:
            head_index+=1
        hot_head=head_index
    else:
        while time_head>data_bci['Date'].values[head_index]:
            head_index+=1
        bci_head=head_index
    if tail_bci==True:
        while time_tail<data_hot['Device time'].values[tail_index]:
            tail_index=tail_index-1
        hot_tail=tail_index
    else:
        while time_tail<data_bci['Date'].values[tail_index]:
            tail_index=tail_index-1
        bci_tail=tail_index

    #継続時刻期間が同じ時刻間の切り取り
    data_bci=data_bci[bci_head:bci_tail]
    data_hot=data_hot[hot_head:hot_tail]
    #print(len(data_bci.index))
    t = np.linspace(0, len(data_hot.index/10),len(data_hot.index))
    tt = np.linspace(0, len(data_hot.index/10),len(data_hot.index)*25)
    print(t)
    print(tt)

    y = [0,0,0,0,0,0]
    f =  [0,0,0,0,0,0]
    z = [0,0,0,0,0,0]
    change_columns_list = ["HbT change(left subtracted)","HbT change(right subtracted)","HbT change(left SD1cm)","HbT change(left SD3cm)","HbT change(right SD1cm)","HbT change(right SD3cm)"]
    print(len(change_columns_list))
    for i in range(len(change_columns_list)):
        print(i)
        print(type(change_columns_list[i]))
        y[int(i)] = data_hot[change_columns_list[i]]
        f[i] = interpolate.interp1d(t,y[i])
        z[i] = f[i](tt)
        print(z[i])

    print("sabun:")
    sabun = len(data_bci.index) - len(z[0])
    print(sabun)
    print("new_bci_tail_val")
    new_bci_tail_val = len(data_bci.index) - sabun
    print(new_bci_tail_val)
    print("data_bci(old):")
    bulk_out=int(len(data_bci.index)/len(data_hot.index))
    data_new=pd.DataFrame(columns=data_hot.columns)
    for i in tqdm(range(int(len(data_hot.index)))):
        for j in range(bulk_out):
            data_new=pd.concat([data_new,data_hot.iloc[i:i+1]])
    for i in tqdm(range(len(data_bci.index)%len(data_hot.index))):
        data_new=pd.concat([data_new,data_hot.iloc[len(data_hot.index)-1:len(data_hot.index)]])
    print(len(data_bci.index))
    print("data_bci(new):")
    count = len(data_bci.index)
    for i in tqdm(range(sabun)):
        data_bci = data_bci.drop(count)
        count -= 1
    print(len(data_bci.index))
    print("data_new(old):")
    print(len(data_new.index))
    print("data_new(new):")
    data_new = data_new[0:len(data_new.index)-sabun]
    print(len(data_new.index))

    for i in tqdm(range(len(change_columns_list))):
        data_new[change_columns_list[i]] = z[i]
    
    head_time = [0.0000]
    for i in tqdm(range(len(z[0]))):
        if i == 0:
            pass
        else:
            head_time.append(head_time[i-1]+0.004)
    data_new['Headset time(sec)'] = head_time
    #2つのデータフレームの結合
    data_bci=data_bci.reset_index()
    data_new=data_new.reset_index()
    data_all=pd.concat([data_bci,data_new],axis=1)

    data_all.to_csv('./to_csv_out_linear_ta.csv')
    print("ファイル作成が完了しました")
    """---note---
    Headset time(sec)を0.004ずつ加算していく
    スプライン変換（補間の種類）
    """