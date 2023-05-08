import sys
from typing import Type
import pycategory as pc
import pyrecord as pr
import tkinter as tk
from tkinter import messagebox

categories = pc.Categories()
records = pr.Records()

command = ""
root = tk.Tk()
root.geometry("1560x520")
root.title("RUEI-CHI LAI HW4")

def click_FIND():
    """click on the FIND button"""
    print("LOG: click on the FIND button") # LOG
    if find_ent.get() != "":
        records.find(find_ent.get(), records_listbox, total_money_lb)

def click_LISTALL():
    """click on the LISTALL button"""
    print("LOG: click on the LISTALL button") # LOG
    records.view(records_listbox, total_money_lb)

def click_UPDATE():
    """click on the UPDATE button"""
    print("LOG: click on the UPDATE button") # LOG
    try:
        int(update_initial_money_ent.get())
    except:
        print("Invalid Update")
        sys.stderr.write("#error: INVALID UPDATE ERROR")
        messagebox.showerror('ERROR', 'Invalid Update')
        return
    else:
        records_listbox.delete(0, "end") # clear the listbox
        records.update_initial_money(update_initial_money_ent.get(), records_listbox, total_money_lb)

def click_ADD():
    """click on the ADD button"""
    print("LOG: click on the ADD button") # LOG
    if command_ent.get() != "":
        records.add(command_ent.get(), comment_ent.get(), categories, records_listbox, total_money_lb)
        
def click_DEL():
    """click on the DEL button"""
    print("LOG: click on the DEL button") # LOG
    if command_ent.get() != "":
        records.delete(command_ent.get(), records_listbox, total_money_lb)

""" UI CANVAS """
# Entry 
find_ent = tk.Entry(root, width=40)
update_initial_money_ent = tk.Entry(root, width=40)
command_ent = tk.Entry(root, width=40)
comment_ent = tk.Entry(root, width=40)

find_ent.grid(row = 0, column=0, rowspan=2, padx = 5, pady=5)
update_initial_money_ent.grid(row=0, column=4, rowspan=2, columnspan=2, padx=5, pady=5)
command_ent.grid(row=3, column=4, padx=5, pady=5)
comment_ent.grid(row=4, column=4, padx=5, pady=5)

# Button
find_btn = tk.Button(root, text = "FIND", font = ("Helvetica", 15), command = click_FIND)
list_all_btn = tk.Button(root, text = "LISTALL", font = ("Helvetica", 15), command = click_LISTALL)
update_initial_money_btn = tk.Button(root, text = "UPDATE", font = ("Helvetica", 15), command = click_UPDATE)
add_btn = tk.Button(root, text = "ADD", font = ("Helvetica", 15), command = click_ADD)
del_btn = tk.Button(root, text = "DEL", font = ("Helvetica", 15), command = click_DEL)

find_btn.grid(row=0, column=1, rowspan=2, padx = 5, pady=5)
list_all_btn.grid(row=0, column=2, rowspan=2, padx = 5, pady=5)
update_initial_money_btn.grid(row=0, column=6, rowspan=2, padx=5, pady=5)
add_btn.grid(row=3, column=5, padx=5, pady=5)
del_btn.grid(row=3, column=6, padx=5, pady=5)

# Listbox
records_listbox = tk.Listbox(root, width=80, height=15, font = ("Consolas", 15))

records_listbox.grid(row=2, column=0, rowspan=2, columnspan=3, padx=5, pady=5)

# Label
init_lb = tk.Label(root, text = "Init money", font = ("Helvetica", 15))
cat_lb = tk.Label(root, text = "\
. expense\n\
  . food\n\
    . meal\n\
    . snack\n\
    . drink\n\
  . transportation\n\
    . bus\n\
    . railway\n\
. income\n\
  . salary\n\
  . bonus", font=("Helvetica", 15))
command_lb = tk.Label(root, text = "COMMAND", font = ("Helvetica", 15))
comment_lb = tk.Label(root, text = "COMMENT", font = ("Helvetica", 15))
total_money_lb = tk.Label(root, text = "Welcome to Ricky's accounting app", font = ("Helvetica", 15))

init_lb.grid(row=0, column=3, rowspan=2, padx = 5, pady=5)
cat_lb.grid(row=2, column=3, columnspan=4,padx=5, pady=5)
command_lb.grid(row=3, column=3, padx=5, pady=5)
comment_lb.grid(row=4, column=3, padx=5, pady=5)
total_money_lb.grid(row=4, column=0, padx=5, pady=5)

root.mainloop()
records.save()
