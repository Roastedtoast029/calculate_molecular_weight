from decimal import Decimal
import openpyxl
import tkinter as tk
import re

class calculate_molecular_weight(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.title("分子量計算ツール")
        self.master.geometry("500x300")


    # tkでの入出力
    def mw_gui():
        return


    # 計算機部分
    # ランレングス圧縮された分子式から分子量を計算
    # ex) C3H8O => 60.095
    def calculater(formula):
        return
    

root = tk.Tk()
app = calculate_molecular_weight(master=root)
app.mainloop()