import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
import traceback
import os
from tkinter import ttk
from tkinter import messagebox
from yahoo_finance_api2 import share
from yahoo_finance_api2.exceptions import YahooFinanceError
from datetime import date, datetime, timedelta
import sys

#Yahooファイナンスから実行した当日の2社の終値を取得する関数を追加、今週のMarket作成の自動化
#土日と終値確定前の判定を行い警告を出す関数の追加、数値エラーに対応するリセット機能 日付自動入力
#Line133に指定した日付の終値を取得するコード、Line30に先週の終値のcsvがあるか確認、なければ作成するコードを追加
do = 0
Thisweek = 20211028
Lastweek = 20211021
now = datetime.now()
n = now.year * 10000 + now.month * 100 + now.day
lastday = now - timedelta(weeks=1)
n2 = lastday.year * 10000 + lastday.month * 100 + lastday.day
last2day = now - timedelta(weeks=2)
n3 = last2day.year * 10000 + last2day.month * 100 + last2day.day


def Complement(Last):
    if os.path.isfile('Market_' + str(Last) + '.csv') is False:
        LD1 = Fetch(9697, Last)
        LD2 = Fetch(3382, Last)
        LD = open('Market_' + str(Last) + '.csv', 'w')
        LD.write(str(LD1) + ',' + str(LD2))
    else:
        pass


def Portfolio(Last=Lastweek, This=Thisweek):  # 入力された日付のデータを元に資産価値を計算する
    M_LastWeek = pd.read_csv('Market_' + str(Last) + '.csv', header=None)
    M_ThisWeek = pd.read_csv('Market_' + str(This) + '.csv', header=None)
    P_LastWeek = pd.read_csv('Portfolio_' + str(Last) + '.csv', header=None)

    Va = M_ThisWeek[0][0] * P_LastWeek[0][0] / M_LastWeek[0][0]
    Vb = M_ThisWeek[1][0] * P_LastWeek[1][0] / M_LastWeek[1][0]

    NPV_ThisWeek = Va + Vb + P_LastWeek[2][0]
    NPV_LastWeek = P_LastWeek[0][0] + P_LastWeek[1][0] + P_LastWeek[2][0]
    Vc = Va + Vb - 400

    FP = open('Portfolio_' + str(This) + '.csv', 'w')
    FP.write(str(Va) + ',' + str(Vb) + ',' + str(Vc))
    FP.close()
    return Va, Vb, NPV_ThisWeek, NPV_LastWeek


def basic():  # 利益率を求める
    FN1 = 'capcom.dat'
    FN2 = 'seven.dat'
    S1 = pd.read_table(FN1, header=None)
    v_S = S1.values
    daycounter1 = 0
    for t in v_S:
        if daycounter1 == 0:
            R1 = []
            daycounter1 = 1
        else:
            valuetoday1 = v_S[daycounter1][0]
            valueyesterday1 = v_S[daycounter1 - 1][0]
            x = valuetoday1
            y = valueyesterday1
            returntoday1 = (x - y) / y
            R1.append(returntoday1)  # appendでくっつける
            daycounter1 += 1
    S2 = pd.read_table(FN2, header=None)
    v_S2 = S2.values
    daycounter2 = 0
    for T in v_S2:
        if daycounter2 == 0:
            R2 = []
            daycounter2 = 1
        else:
            valuetoday2 = v_S2[daycounter2][0]
            valueyesterday2 = v_S2[daycounter2 - 1][0]
            m = valuetoday2
            n = valueyesterday2
            returntoday2 = (m - n) / n
            R2.append(returntoday2)  # appendでくっつける
            daycounter2 += 1
    return R1, R2


def ValueatRisk(X1, X2, NPV=Portfolio()[2]):  # ヒストリカル法でのVaRと5日間のVaRを計算する
    vt = []
    for p, q in zip(basic()[0], basic()[1]):
        v2 = NPV + X1 * p + X2 * q
        vt.append(v2)
    vt.sort()
    ii = []
    for i in range(1, len(vt)):  # 分位点計算
        if i <= 0.01 * len(vt):
            ii.append(int(i))
    i0 = max(ii) - 1
    HSVaR = NPV - vt[i0]
    # print(HSVaR)
    HSVaR5days = HSVaR * np.sqrt(5)
    # print(HSVaR5days)
    mu1 = np.mean(basic()[0])
    sigma1 = np.std(basic()[0])
    mu2 = np.mean(basic()[1])
    sigma2 = np.std(basic()[1])
    cor = np.corrcoef(basic()[0], basic()[1])
    rho = cor[0][1]
    muP = X1 * mu1 + X2 * mu2
    sigmaP = np.sqrt((X1 * sigma1) ** 2 + (X2 * sigma2) ** 2 + 2 * X1 * X2 * sigma1 * sigma2 * rho)
    DNVaR = 2.33 * sigmaP - muP
    # print(DNVaR)
    DNVaR5days = 2.33 * np.sqrt(5) * sigmaP - 5 * muP
    # print(DNVaR5days)
    return HSVaR, HSVaR5days, DNVaR, DNVaR5days


def todayM(code, Day):  # 今日の株価の終値を取得
    my_share = share.Share(str(code) + ".T")
    symbol_data = None
    try:
        symbol_data = my_share.get_historical(share.PERIOD_TYPE_DAY,
                                              int(Day),
                                              share.FREQUENCY_TYPE_DAY,
                                              1)
    except YahooFinanceError as e:
        print(e.message)
    TM = int(symbol_data['close'][-1])  # 終値だけを取得
    return TM


def Fetch(code, Fetchday): # 指定した日付の終値を持ってくる
    FetchDate = str(Fetchday)[:4] + '-' + str(Fetchday)[4:6] + '-' + str(Fetchday)[6:]  # YYYY-MM-DD

    my_share = share.Share(str(code) + ".T")
    symbol_data3 = None
    try:
        symbol_data3 = my_share.get_historical(
            share.PERIOD_TYPE_YEAR, 1,
            share.FREQUENCY_TYPE_DAY, 1)
    except YahooFinanceError as e:
        print(e.message)
        sys.exit(1)

    # print(symbol_data)
    # convert to pandas dataframe object
    df = pd.DataFrame(symbol_data3)
    df["datetime"] = pd.to_datetime(df.timestamp, unit="ms")
    print(df)
    # convert to Japanese Standard Time
    df["datetime_JST"] = df["datetime"] + timedelta(hours=9)
    FetchDate_Obj_S = datetime.strptime(FetchDate + ' 00:00',
                                                 "%Y-%m-%d %H:%M")  # convert the date str to date object
    FetchDate_Obj_E = datetime.strptime(FetchDate + ' 23:59', "%Y-%m-%d %H:%M")
    timestamp_S = int(round(FetchDate_Obj_S.timestamp())) * 1000
    timestamp_E = int(round(FetchDate_Obj_E.timestamp())) * 1000
    df = df[timestamp_S <= df['timestamp']]
    df = df[df['timestamp'] <= timestamp_E]
    # df = df[df['timestamp'] <= E_timestamp]
    df = df.reset_index(drop=True)
    return df['close'][0]

def MakeCSV(This):  # 今日の株価の終値のcsvを作成
    week = now.weekday()
    print(now.weekday())
    print(now.hour + now.minute / 100)
    if week == 5 or week == 6:  # 土日の判定、4連休まで対応
        messagebox.showinfo('警告', '本日の終値を参照できないため、最新の終値を取得しています')
        TM1 = todayM(9697, 4)  # カプコン
        TM2 = todayM(3382, 4)  # セブン
    elif 0 <= now.hour + now.minute / 100 <= 9:
        messagebox.showinfo('警告', 'まだ今日の株式市場は開いていません')
        pass
    elif now.hour + now.minute / 100 <= 15.30:  # 15時半前の判定
        messagebox.showinfo('警告', '終値が確定していないため、値が正確でない可能性があります')
        TM1 = todayM(9697, 1)
        TM2 = todayM(3382, 1)
    else:
        TM1 = todayM(9697, 1)
        TM2 = todayM(3382, 1)
    TD = open('Market_' + str(This) + '.csv', 'w')
    TD.write(str(TM1) + ',' + str(TM2))
    label = tk.Label(text="株価を取得しました")
    label.place(x=10, y=220)


def DataGet(code):  # 2年分データ取得用
    my_share = share.Share(str(code) + ".T")
    symbol_data2year = None
    try:
        symbol_data2year = my_share.get_historical(share.PERIOD_TYPE_YEAR, 2, share.FREQUENCY_TYPE_DAY, 1)
    except YahooFinanceError as e:
        print(e.message)
        messagebox.showinfo('Error', 'エラーが発生しました。リセットします')
        reset()
    return symbol_data2year['close']


# def Complement(): # 過去をさかのぼって株価データを補完したい

def Market():  # 2年分の株価終値を取得してdatファイルを作成します
    global do
    try:
        code1 = int(X1code.get())
        code2 = int(X2code.get())
        X1MClose = DataGet(code1)
        X2MClose = DataGet(code2)
        for p, q in zip(X1MClose, X2MClose):
            # print(p)
            FP = open(str(code1) + '.dat', 'a')
            FP.write(str(p))
            FP.write('\n')
            FP.close()
            # print(q)
            FP = open(str(code2) + '.dat', 'a')
            FP.write(str(q))
            FP.write('\n')
            FP.close()
    except ValueError:
        messagebox.showinfo('Error', '数値が入力されていないか、正しくありません')
        reset()
    do = 1


def run():  # 入力された日付・投資額を取得してポートフォリオ作成＆代入して計算
    global Thisweek
    global Lastweek
    global NPV
    global label
    global do
    global X1
    global X2
    if do == 1:
        do = 0
    try:
        twget = int(tw.get())
        lwget = int(lw.get())
        NPV = int(NPVData.get())
        X1 = int(X1set.get())
        X2 = int(X2set.get())
        if len(tw.get()) != 8 or len(lw.get()) != 8:
            messagebox.showinfo('Error', '入力された日付が正しくありません')
            reset()
            do = 1
        else:
            MakeCSV(twget)
            Complement(lwget)
            Portfolio(lwget, twget)
            label = tk.Label(text="ポートフォリオが作成されました")
            label.place(x=10, y=240)
            ValueatRisk(X1, X2, NPV)
            label99 = tk.Label(text=str(ValueatRisk(X1, X2, NPV)))
            label99.place(x=10, y=280)
    except ValueError or AttributeError:
        messagebox.showinfo('Error', 'エラーが発生しました。リセットします')
        reset()
        t = traceback.format_exc()  # エラーメッセージ表示
        print(t)
        do = 1


def reset():  # 一度計算した結果をリセット
    global do
    tw.delete(0, tk.END)  # 入力欄の0桁から最後まで削除
    lw.delete(0, tk.END)
    NPVData.delete(0, tk.END)
    X1set.delete(0, tk.END)
    X2set.delete(0, tk.END)
    X1code.delete(0, tk.END)
    X2code.delete(0, tk.END)
    do = 1


def close():  # ウインドウ削除
    global do
    do = 1
    root.destroy()


def default():  # グループ3のデフォルト数値を入力
    global do
    n = now.year * 10000 + now.month * 100 + now.day
    lastday = now - timedelta(weeks=1)
    n2 = lastday.year * 10000 + lastday.month * 100 + lastday.day
    tw.insert(tk.END, str(n))
    lw.insert(tk.END, str(n2))
    NPVData.insert(tk.END, "100")
    X1set.insert(tk.END, "250")
    X2set.insert(tk.END, "250")
    do = 0


root = tk.Tk()  # ウインドウの設定
root.title("VaR計算ツール")
root.geometry("540x360")
tw = tk.Entry(master=root, width=10, font=20)  # 数値入力欄の設定
tw.place(x=80, y=10)
lw = tk.Entry(master=root, width=10, font=20)
lw.place(x=80, y=30)
NPVData = tk.Entry(master=root, width=10, font=20)
NPVData.place(x=80, y=50)
X1set = tk.Entry(master=root, width=10, font=20)
X1set.place(x=80, y=70)
X2set = tk.Entry(master=root, width=10, font=20)
X2set.place(x=80, y=90)
X1code = tk.Entry(master=root, width=5, font=20)
X1code.place(x=300, y=10)
X2code = tk.Entry(master=root, width=5, font=20)
X2code.place(x=300, y=30)
button1 = tk.Button(master=root, text='実行', command=run,
                    fg='blue')  # 各ボタンの設定
button1.place(x=40, y=130)
button2 = tk.Button(master=root, text='リセット', command=reset,
                    fg='blue')
button2.place(x=80, y=130)
button3 = tk.Button(master=root, text='終了', command=close,
                    fg='blue')
button3.place(x=130, y=130)
button4 = tk.Button(master=root, text='株価データ取得', command=Market,
                    fg='blue')
button4.place(x=380, y=20)
button5 = tk.Button(master=root, text='自動入力', command=default,
                    fg='blue')
button5.place(x=170, y=130)
label1 = tk.Label(text='今週の日付')  # 各ラベルの設定
label1.place(x=0, y=10)
label2 = tk.Label(text='先週の日付')
label2.place(x=0, y=30)
label3 = tk.Label(text='NPV')
label3.place(x=0, y=50)
label4 = tk.Label(text='カプコン投資額')
label4.place(x=0, y=70)
label5 = tk.Label(text='セブン投資額')
label5.place(x=0, y=90)
label6 = tk.Label(text="HSVaR  HSVaR5days / DNVaR  DNVaR5days")
label6.place(x=10, y=260)
label7 = tk.Label(text='企業コード1')
label7.place(x=220, y=10)
label8 = tk.Label(text='企業コード2')
label8.place(x=220, y=30)
tw.insert(tk.END, str(n))
lw.insert(tk.END, str(n2))
NPVData.insert(tk.END, "100")
X1set.insert(tk.END, "250")
X2set.insert(tk.END, "250")
root.mainloop()
# ウインドウの設定
