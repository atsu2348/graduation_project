from tkinter import *  # GUI関連
from tkinter import ttk
from tkinter import font
from tkinter import filedialog
from tkinter import messagebox
import os
import bci_hot1000_integration_linear_ta_deleted_trash  # 整形・結合するプログラム


def button_clicked_bci():  # bciのファイル選択
    fTyp = [("", "*.txt")]
    iDir = os.path.abspath(os.path.dirname(__file__))
    bci_file_select = filedialog.askopenfilename(
        filetypes=fTyp, initialdir=iDir)
    print(bci_file_select)
    bci_file.set(bci_file_select)


def button_clicked_nirs():  # nirsのファイル選択
    fTyp = [("", "*.csv")]
    iDir = os.path.abspath(os.path.dirname(__file__))
    nirs_file_select = filedialog.askopenfilename(
        filetypes=fTyp, initialdir=iDir)
    print(nirs_file_select)
    nirs_file.set(nirs_file_select)


def button_clicked_concat_start():  # 整形・結合開始ボタン
    bci_hot1000_integration_linear_ta.concat_file(
        bci_file.get(), nirs_file.get())
    messagebox.showinfo('File concat Tool', 'ファイル作成が完了しました。\n使用したファイルは以下の2つです。\n' +
                        bci_file.get() + '\n\n' + nirs_file.get())
    retry_question = messagebox.askquestion('File concat Tool', '同じ作業を続けますか？')
    if retry_question == "no":
        root.quit()


def exit_button():  # 終了ボタン
    exit_question = messagebox.askquestion('File concat Tool', '終了しますか？')
    if exit_question == "yes":
        root.quit()


# ファイル選択ダイアログの表示
root = Tk()  # ルートフレームの作成
root.title('File concat Tool')
# Frame1の作成
frame1 = ttk.Frame(root, padding=10)
frame1.grid()

# 参照ボタンの作成
bci_button = ttk.Button(frame1, text="select BCI file",
                        command=button_clicked_bci)
bci_button.grid(row=0, column=3)
# 参照ボタンの作成
nirs_button = ttk.Button(frame1, text="select NIRS file",
                         command=button_clicked_nirs)
nirs_button.grid(row=1, column=3)

# ラベルの作成
# 「ファイル」ラベルの作成
s = StringVar()
s.set('BCIファイル>>')
label1 = ttk.Label(frame1, textvariable=s)
label1.grid(row=0, column=0)
# 参照ファイルパス表示ラベルの作成
bci_file = StringVar()
file1_entry = ttk.Entry(frame1, textvariable=bci_file, width=50)
file1_entry.grid(row=0, column=2)

# ラベルの作成
# 「ファイル」ラベルの作成
t = StringVar()
t.set('NIRSファイル>>')
label2 = ttk.Label(frame1, textvariable=t)
label2.grid(row=1, column=0)
# 参照ファイルパス表示ラベルの作成
nirs_file = StringVar()
file2_entry = ttk.Entry(frame1, textvariable=nirs_file, width=50)
file2_entry.grid(row=1, column=2)
# root.withdraw()#ルートフレームを隠す

# Frame2の作成
frame2 = ttk.Frame(root, padding=(0, 5))
frame2.grid(row=1)
start_button = ttk.Button(
    frame2, text="開始", command=button_clicked_concat_start)
start_button.pack(side=LEFT)
quit_button = ttk.Button(frame2, text="終了", command=exit_button)
quit_button.pack(side=LEFT)

# ルートフレームを閉じるボタンが押されるまで出し続ける
root.mainloop()
