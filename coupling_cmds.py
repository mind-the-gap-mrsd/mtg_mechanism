import tkinter as tk
from Adafruit_IO import Client, Feed, Data

ADAFRUIT_IO_USERNAME = "ysudhansh"  
ADAFRUIT_IO_KEY = "aio_FNkZ38Hy1iXvCb7n1Pk0nqxWRav9"
aio = Client(key=ADAFRUIT_IO_KEY, username=ADAFRUIT_IO_USERNAME)
delimiter = ";"

def send():
    k114Cmd = k114.get("1.0", "end-1c")
    k115Cmd = k115.get("1.0", "end-1c")
    k116Cmd = k116.get("1.0", "end-1c")
    aio.send("mtg-mechanism.k114", k114Cmd)
    aio.send("mtg-mechanism.k115", k115Cmd)
    aio.send("mtg-mechanism.k116", k116Cmd)

tkTop = tk.Tk()
tkTop.geometry('150x170')
tkTop.title("Mind The Gap")

k114Label = tk.Label(text = "Khepera 114").pack()
k114 = tk.Text(tkTop, height = 1, width = 5, bg = "light yellow")
k114.pack()
k115Label = tk.Label(text = "Khepera 115").pack()
k115 = tk.Text(tkTop, height = 1, width = 5, bg = "light yellow")
k115.pack()
k116Label = tk.Label(text = "Khepera 116").pack()
k116 = tk.Text(tkTop, height = 1, width = 5, bg = "light yellow")
k116.pack()
sendButton = tk.Button(tkTop, height = 2, width = 5, text ="Send", command = lambda:send())
sendButton.pack()

tk.mainloop()