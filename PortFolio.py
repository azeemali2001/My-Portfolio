
from os import cpu_count
from tkinter import font
from tkinter import messagebox, Menu

import requests
import json
from tkinter import *
import sqlite3

from requests import api

#SQLite3 related info
con = sqlite3.connect('coin.db')
cursorObj = con.cursor()

#creating table
cursorObj.execute("CREATE TABLE IF NOT EXISTS coin(id INTEGER PRIMARY KEY,symbol TEXT,amount INTEGER,price REAL)")
con.commit()

#adding content to table
# cursorObj.execute("INSERT INTO coin(id,symbol,amount,price) VALUES(?,?,?,?)",(1,"BTC",2,42000))
# con.commit()

# cursorObj.execute("INSERT INTO coin(id,symbol,amount,price) VALUES(?,?,?,?)",(2,"ETH",8,3000))
# con.commit()

# cursorObj.execute("INSERT INTO coin(id,symbol,amount,price) VALUES(?,?,?,?)",(3,"USDT",92,1.05))
# con.commit()

# cursorObj.execute("INSERT INTO coin(id,symbol,amount,price) VALUES(?,?,?,?)",(4,"BNB",10,440))
# con.commit()


#tkinter related info
pycrypto = Tk()
pycrypto.title('My PortFolio')
pycrypto.iconbitmap('favicon.ico')


# coins =[
#     {
#         "symbol":"BTC",
#         "avg_buy_price":42000,
#         "no_of_coins":2
#     },
#     {
#         "symbol":"ETH",
#         "avg_buy_price":3000,
#         "no_of_coins":8
#     },
#     {
#         "symbol":"USDT",
#         "avg_buy_price":1.05,
#         "no_of_coins":92
#     },
#     {
#         "symbol":"BNB",
#         "avg_buy_price":440,
#         "no_of_coins":10
#     }
# ]

#some Basic Functions
def font_colour(val):
    if val >= 0:
        return "green"
    else:
        return "red"

def reset():
    for cell in pycrypto.winfo_children():            #destroying each cell 
        cell.destroy() 

    header()                                           # rewrite cell again
    portFolio()   







def portFolio():

    #Fetching all Data Base
    cursorObj.execute("SELECT * FROM coin")
    coins = cursorObj.fetchall()

    #Some Basic Function
    def add_coin():
        cursorObj.execute("INSERT INTO coin(symbol,amount,price) VALUES(?,?,?)",(symbol_add.get(),amount_of_coin_add.get(),price_add.get()))
        con.commit()
        messagebox.showinfo("Portfolio Popup","Coin Added Successfully")
        reset()

    def update_coin():
        cursorObj.execute("UPDATE coin SET symbol=?, price=?, amount=? WHERE id=?", (symbol_up.get(), price_up.get(), amount_of_coin_up.get(), key_up.get()))
        con.commit()
        messagebox.showinfo("Portfolio Popup","Coin Updated Succcessfully")
        reset()

    def delete_coin():
        cursorObj.execute("DELETE FROM coin WHERE id=?", (key_del.get(),))
        con.commit()
        messagebox.showinfo("Portfolio Popup","COin Deleted Successfully")
        reset()

    #api related info
    api_request = requests.get('https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?start=1&limit=300&convert=USD&CMC_PRO_API_KEY=3889ce63-c733-403d-8b7d-c41a2438b4ea')
    api = json.loads(api_request.content)

    total_buy_price = 0
    total_sell_price = 0 
    total_paid = 0
    pl_per_coin = 0
    total_pl = 0
    overall_pl = 0


    coin_row = 1

    for i in range(0,300):
        for coin in coins:
            if coin[1]==api["data"][i]["symbol"]:
            
                
                total_buy_price=coin[3]*coin[2]
                total_sell_price=api["data"][i]["quote"]["USD"]["price"]*coin[2]

                pl_per_coin = api["data"][i]["quote"]["USD"]["price"]-coin[3]
                total_pl = pl_per_coin*coin[2]

                # print(api["data"][i]["symbol"])
                # print(api["data"][i]["name"])
                # print("$ {0:.2F}".format(api["data"][i]["quote"]["USD"]["price"]))
                # print("------------------")

                # #summation
                total_paid+=total_buy_price
                overall_pl+=total_pl

                id = Label(pycrypto,text=i+1,bg="#F3F4F6",fg="black",font="lato 12",padx=2,pady=2,borderwidth=2,relief="groove")
                id.grid(row=coin_row,column=0,sticky=N+S+E+W)

                name = Label(pycrypto,text=api["data"][i]["symbol"],bg="#F3F4F6",fg="black",font="lato 12 ",padx=2,pady=2,borderwidth=2,relief="groove")
                name.grid(row=coin_row,column=1,sticky=N+S+E+W)

                amount_of_coin = Label(pycrypto,text=coin[2],bg="#F3F4F6",fg="black",font="lato 12",padx=2,pady=2,borderwidth=2,relief="groove")
                amount_of_coin.grid(row=coin_row,column=2,sticky=N+S+E+W)

                buy_price = Label(pycrypto,text="$ {0:.2F}".format(coin[3]),bg="#F3F4F6",fg="black",font="lato 12",padx=2,pady=2,borderwidth=2,relief="groove")
                buy_price.grid(row=coin_row,column=3,sticky=N+S+E+W)

                total_amount = Label(pycrypto,text="$ {0:.2F}".format(total_buy_price),bg="#F3F4F6",fg="black",font="lato 12",padx=2,pady=2,borderwidth=2,relief="groove")
                total_amount.grid(row=coin_row,column=4,sticky=N+S+E+W)

                price = Label(pycrypto,text="$ {0:.2F}".format(api["data"][i]["quote"]["USD"]["price"]),bg="#F3F4F6",fg="black",font="lato 12",padx=2,pady=2,borderwidth=2,relief="groove")
                price.grid(row=coin_row,column=5,sticky=N+S+E+W)

                p_l_percoin = Label(pycrypto,text="$ {0:.2F}".format(pl_per_coin),bg="#F3F4F6",fg=font_colour(float("{0:.2F}".format(pl_per_coin))),font="lato 12",padx=2,pady=2,borderwidth=2,relief="groove")
                p_l_percoin.grid(row=coin_row,column=6,sticky=N+S+E+W)

                p_l = Label(pycrypto,text="$ {0:.2F}".format(total_pl),bg="#F3F4F6",fg=font_colour(float("{0:.2F}".format(total_pl))),font="lato 12",padx=2,pady=2,borderwidth=2,relief="groove")
                p_l.grid(row=coin_row,column=7,sticky=N+S+E+W)


                coin_row+=1
                total_buy_price=0
    
    total_paid_amount = Label(pycrypto,text="$ {0:.2F}".format(total_paid),bg="#F3F4F6",fg=font_colour(float("{0:.2F}".format(total_paid))),font="lato 12",padx=2,pady=2,borderwidth=2,relief="groove")
    total_paid_amount.grid(row=coin_row,column=4,sticky=N+S+E+W)

    total_pl_ = Label(pycrypto,text="$ {0:.2F}".format(overall_pl),bg="#F3F4F6",fg=font_colour(float("{0:.2F}".format(overall_pl))),font="lato 12",padx=2,pady=2,borderwidth=2,relief="groove")
    total_pl_.grid(row=coin_row,column=7,sticky=N+S+E+W)

    #Refresh Button
    api = ""
    refresh = Button(pycrypto, text="Refresh", bg="#142E54", fg="white", command=reset ,font="Lato 12", borderwidth=2, relief="groove", padx="2", pady="2")
    refresh.grid(row=coin_row + 1, column=7, sticky=N+S+E+W)

    #Add button
    symbol_add = Entry(pycrypto, borderwidth=2, relief="groove")
    symbol_add.grid(row=coin_row+1, column=1,sticky=N+S+E+W)

    amount_of_coin_add = Entry(pycrypto,borderwidth=2,relief="groove")
    amount_of_coin_add.grid(row=coin_row+1,column=2,sticky=N+S+E+W)

    price_add = Entry(pycrypto,borderwidth=2,relief="groove")
    price_add.grid(row=coin_row+1,column=3,sticky=N+S+E+W)

    add_button = Button(pycrypto,text="Add coin",bg="#142E54",fg="white",command=add_coin,font="lato 12",borderwidth=2,relief="groove",padx=2,pady=2)
    add_button.grid(row=coin_row+1,column=4,sticky=N+S+E+W)

    #Update button
    key_up = Entry(pycrypto, borderwidth=2, relief="groove")
    key_up.grid(row=coin_row+2, column=0,sticky=N+S+E+W)

    symbol_up = Entry(pycrypto, borderwidth=2, relief="groove")
    symbol_up.grid(row=coin_row+2, column=1,sticky=N+S+E+W)

    amount_of_coin_up = Entry(pycrypto,borderwidth=2,relief="groove")
    amount_of_coin_up.grid(row=coin_row+2,column=2,sticky=N+S+E+W)

    price_up = Entry(pycrypto,borderwidth=2,relief="groove")
    price_up.grid(row=coin_row+2,column=3,sticky=N+S+E+W)

    up_button = Button(pycrypto,text="Update coin",bg="#142E54",fg="white",command=update_coin,font="lato 12",borderwidth=2,relief="groove",padx=2,pady=2)
    up_button.grid(row=coin_row+2,column=4,sticky=N+S+E+W)

    #Delete button
    key_del = Entry(pycrypto, borderwidth=2, relief="groove")
    key_del.grid(row=coin_row+3, column=0,sticky=N+S+E+W)

    del_button = Button(pycrypto,text="Delete Coin",bg="#142E54",fg="white",command=delete_coin,font="lato 12",borderwidth=2,relief="groove",padx=2,pady=2)
    del_button.grid(row=coin_row+3,column=4,sticky=N+S+E+W)

def header():
    id = Label(pycrypto,text="Portfolio ID",bg="#142E54", fg="white",font="lato 12 bold",padx=5,pady=5,borderwidth=2,relief="groove")
    id.grid(row=0,column=0,sticky=N+S+E+W)

    coin_name = Label(pycrypto,text="Coin Name",bg="#142E54", fg="white",font="lato 12 bold",padx=5,pady=5,borderwidth=2,relief="groove")
    coin_name.grid(row=0,column=1,sticky=N+S+E+W)

    no_of_coin = Label(pycrypto,text="Number of Coins",bg="#142E54", fg="white",font="lato 12 bold",padx=5,pady=5,borderwidth=2,relief="groove")
    no_of_coin.grid(row=0,column=2,sticky=N+S+E+W)

    buy_price = Label(pycrypto,text="Average Buy Price",bg="#142E54", fg="white",font="lato 12 bold",padx=5,pady=5,borderwidth=2,relief="groove")
    buy_price.grid(row=0,column=3,sticky=N+S+E+W)

    total_price = Label(pycrypto,text="Total Buy Price",bg="#142E54", fg="white",font="lato 12 bold",padx=5,pady=5,borderwidth=2,relief="groove")
    total_price.grid(row=0,column=4,sticky=N+S+E+W)

    curr_price = Label(pycrypto,text="Current Price",bg="#142E54", fg="white",font="lato 12 bold",padx=5,pady=5,borderwidth=2,relief="groove")
    curr_price.grid(row=0,column=5,sticky=N+S+E+W)

    pl_per_coin = Label(pycrypto,text="Profi/Loss per coin",bg="#142E54", fg="white",font="lato 12 bold",padx=5,pady=5,borderwidth=2,relief="groove")
    pl_per_coin.grid(row=0,column=6,sticky=N+S+E+W)

    total_pl = Label(pycrypto,text="Total Profit/Loss",bg="#142E54", fg="white",font="lato 12 bold",padx=5,pady=5,borderwidth=2,relief="groove")
    total_pl.grid(row=0,column=7,sticky=N+S+E+W)



header()
portFolio()


pycrypto.mainloop()
            
    


