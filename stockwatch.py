import tkinter as tk
from tkinter import ttk, messagebox
import yfinance as yf
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def fetch_stocks(exchange):
    if exchange == "NYSE":
        return ["AAPL", "MSFT", "JNJ", "V", "WMT", "PG", "INTC", "CSCO", "T", "XOM"]  
    elif exchange == "NASDAQ":
        return ["GOOGL", "AMZN", "TSLA", "FB", "NVDA", "PYPL", "CMCSA", "ADBE", "NFLX", "PEP"]  
    elif exchange == "IDX":
        return ["BBCA.JK", "TLKM.JK", "UNVR.JK", "BBRI.JK", "BMRI.JK", "ASII.JK", "INDF.JK", "GGRM.JK", "ICBP.JK", "EXCL.JK"]  
    else:
        return []

def fetch_stock_data(symbol):
    try:
        stock = yf.Ticker(symbol)
        data = stock.history(period="1mo")  # Get data for the past month
        return data
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch data for the symbol. Please try again. Error: {e}")
        return None

def show_stock_data(symbol):
    data = fetch_stock_data(symbol)
    if data is None:
        return

    window = tk.Toplevel(root)
    window.title(f"Stock Data - {symbol}")

    label = tk.Label(window, text="Stock Data:")
    label.pack()

    fig, ax = plt.subplots(figsize=(8, 6))
    data['Close'].plot(ax=ax)
    ax.set_title(f"Stock Price for {symbol}")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price ($)")
    plt.xticks(rotation=45)
    plt.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack()

def show_exchange_stocks():
    selected_exchange = exchange_combobox.get()
    stocks = fetch_stocks(selected_exchange)
    stocks_text.delete('1.0', tk.END)
    for stock in stocks:
        stocks_text.insert(tk.END, stock + '\n')
        stocks_text.tag_add(stock, f'{stocks_text.index("end - 1c")} linestart', f'{stocks_text.index("end - 1c")} lineend')
        stocks_text.tag_bind(stock, "<Button-1>", lambda event, stock=stock: show_stock_data(stock))

root = tk.Tk()
root.title("Stock Viewer")

label = tk.Label(root, text="Select Exchange:")
label.grid(row=0, column=0)

exchange_combobox = ttk.Combobox(root, values=["NYSE", "NASDAQ", "IDX"])
exchange_combobox.grid(row=0, column=1)

show_stocks_button = tk.Button(root, text="Show Stocks", command=show_exchange_stocks)
show_stocks_button.grid(row=0, column=2)

stocks_text = tk.Text(root, height=20, width=50)
stocks_text.grid(row=1, columnspan=3)

label_symbol = tk.Label(root, text="Enter Stock Symbol:")
label_symbol.grid(row=2, column=0)

entry = tk.Entry(root)
entry.grid(row=2, column=1)

button = tk.Button(root, text="Show Stock Data", command=lambda: show_stock_data(entry.get()))
button.grid(row=2, column=2)

root.mainloop()