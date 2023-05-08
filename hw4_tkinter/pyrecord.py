""" created by Ricky Lai 2022.6.6 """
from email import message
import sys, os, datetime
import tkinter as tk
from tkinter import messagebox
#date = date.year+"-"+str(date.month).zfill(2)+"-"+str(date.day).zfill(2)

class Record:
    """Represent a record."""
    def __init__(self, date, cat, item, cost, comment = ""):
        """initialize"""
        self._date = date
        self._cat = cat
        self._item = item
        self._cost = cost
        self._comment = comment[:-1] # ignore '\n'

    @property
    def date(self):
        """date"""
        return self._date
    @property
    def cat(self):
        """category"""
        return self._cat    
    @property
    def item(self):
        """item"""
        return self._item
    @property
    def cost(self):
        """cost"""
        return self._cost   
    @property
    def comment(self):
        """comment"""
        return self._comment

    def show(self):
        """show record"""
        print("{:<15s}".format(self._date), "{:<15s}".format(self._cat), "{:<15s}".format(self._item),  \
            "{:<15s}".format(self._cost), "{:<30s}".format(self._comment)) 

class Records:
    
    """Maintain a list of all the 'Record's and the initial amount of money."""
    def __init__(self):
        """initialize"""
        try:
            dir_path = os.path.dirname(os.path.realpath(__file__)) # current directory
            dir_name = dir_path + "/records.txt"
            fh = open(dir_name, "r+")
            filesize = os.path.getsize(dir_name) # if we lost the file contents
        except: # file doesn't exist 
            fh = open(dir_name, "w+")
            total = "0"
            fh.write(total)
            self._records = []
        else:
            if filesize == 0: # empty file
                total = "0"
                fh.write(total)
                self._records = []
            else: # file exists and has data
                print("Welcome Back!")
                total = fh.readline()
                acc = fh.readlines()
                self._records = []
                for i in acc:
                    if i == "\n":
                        continue
                    temp = i.split(",")
                    date_time = temp[0]
                    cat_name = temp[1]
                    item = temp[2]
                    cost = temp[3]
                    comment = temp[4]
                    self._records.append(Record(date_time, cat_name, item, cost, comment))                 
        finally:
            self._init_money = int(total)
    
    def add(self, record, comment, cat, listbox, total_money_label): # <IMPORTANT> cat is a class Categories
        """add record to Records object self._records[]"""
        try:
            temp = record.split(" ")
            if (len(temp) == 3):
                dt = datetime.date.today() # dt is an datetime object  
                date_time = str(dt.year) + "-" + str(dt.month).zfill(2) + "-" + str(dt.day).zfill(2) # form the format "2022-06-06"
                cat_name = temp[0]
                item = temp[1]
                cost = temp[2]
            elif (len(temp) == 4):
                date_time = temp[0]
                cat_name = temp[1]
                item = temp[2]
                cost = temp[3]
        except ValueError:
            print("Invalid value for money.")
            print("Fail to add a record")
            sys.stderr.write("#error: VALUE ERROR")
            messagebox.showerror('ERROR', 'Invalid value for money.')
            return
        except IndexError:
            print("The format of a record should be like this: food bread -50.")
            print("Fail to add a record")
            sys.stderr.write("#error: FORMAT ERROR")
            messagebox.showerror('ERROR', 'The format of a record should be like this food bread -50.')
            return 

        try:
            datetime.date.fromisoformat(date_time)
        except:
            print("Invalid datetime.")
            print("The format of date should be YYYY-MM-DD (pad zero)")
            sys.stderr.write("#error: DATETIME FORMAT ERROR")
            messagebox.showerror('ERROR', 'The format of date should be YYYY-MM-DD (pad zero).')
            return

        if cat.is_category_valid(cat_name) == False:
            print("Can't find the category")
            sys.stderr.write("#error: CATEGORY ERROR")
            messagebox.showerror('ERROR', 'Can'' find the category.')
            return
    
        if (comment != ""):
            comment += "\n"
        self._records.append(Record(date_time, cat_name, item, cost, comment))

        """update listbox"""
        listbox.delete(0, "end") # clear the listbox
        description = ("{:<12s} {:<12s} {:<12s} {:<8s} {:<10s}".format("DATETIME", "CATEGORIES", "DESCRIPTION", "AMOUNT", "COMMENT"))
        listbox.insert(tk.END, description)
        listbox.insert(tk.END, "="*80)
        amount = self._init_money
        for i in self._records:
            amount += int(i.cost)
            records_insert = ("{:<12s} {:<12s} {:<12s} {:<8s} {:<10s}".format(i.date, i.cat, i.item, i.cost, i.comment))
            listbox.insert(tk.END, records_insert)
        listbox.insert(tk.END, "="*80)
        total_money_label["text"] = f'Now you have {amount} dollars now'
        messagebox.showinfo('SUCCESSFULLY', 'add' + f' {cat_name} {item} {cost} {comment}' + 'successfully')

    def view(self, listbox, total_money_label):
        """it shows every records store in this Records object"""
        #print("{:<15s}".format("DATETIME"), "{:<15s}".format("CATEGORIES"), "{:<15s}".format("DESCRIPTION"), \
            #"{:<15s}".format("AMOUNT"), "{:<30s}".format("COMMENT"))
        #print("="*80)
        listbox.delete(0, "end") # clear the listbox
        description = ("{:<12s} {:<12s} {:<12s} {:<8s} {:<10s}".format("DATETIME", "CATEGORIES", "DESCRIPTION", "AMOUNT", "COMMENT"))
        listbox.insert(tk.END, description)
        listbox.insert(tk.END, "="*80)
        amount = self._init_money
        for i in self._records:
            amount += int(i.cost)
            records_insert = ("{:<12s} {:<12s} {:<12s} {:<8s} {:<10s}".format(i.date, i.cat, i.item, i.cost, i.comment))
            listbox.insert(tk.END, records_insert)
            #i.show()
        #print("="*80)
        listbox.insert(tk.END, "="*80)
        #print(f'YOU HAVE {amount} dollars now')
        total_money_label["text"] = f'Now you have {amount} dollars now'

        
    
    def delete(self, record, listbox, total_money_label):
        """delete record from Records object self._records[]"""
        if record == "exit":
            return
        del_num = 0
        try:
            temp = record.split(" ")
            cat_name = temp[0]
            item = temp[1]
            cost = int(temp[2])
        except (ValueError, IndexError) as err:
            print("Invalid Format.")
            print("Fail to delete a record")
            sys.stderr.write("#error: Invalid Format")
            messagebox.showerror('ERROR', 'Invalid Format')
            return
        del_list = [] # we store the deleted records' index in del_list 
        for index, i in enumerate(self._records):
            if i.cat == cat_name and i.item == item and i.cost == str(cost):
                if del_num == 0:
                    print(f'delete {cat_name} {item} {cost} successfully!')
                    del_list.append(index)
                    del_num += 1
                else:
                    ans = messagebox.askquestion('Message', 'We found one more same records, do u want to delete it?') 
                    if (ans == 'yes'):
                        print(f'delete {cat_name} {item} {cost} successfully!')
                        del_list.append(index)
                        del_num += 1
        for n, i in enumerate(del_list):
            del self._records[i-n] # i-n is the right index of the deleted item 
        #print(f'we delete {del_num} record(s)')
        if del_num == 0:
            print(f'There\'s no record with {cat_name} {item} {cost}')
            print("Fail to delete a record")
            messagebox.showwarning('Warning', f'There is no {cat_name} {item} {cost}')
            return

        messagebox.showinfo('Message', f'we delete {del_num} records(s)')
        """update listbox"""
        listbox.delete(0, "end") # clear the listbox
        description = ("{:<12s} {:<12s} {:<12s} {:<8s} {:<10s}".format("DATETIME", "CATEGORIES", "DESCRIPTION", "AMOUNT", "COMMENT"))
        listbox.insert(tk.END, description)
        listbox.insert(tk.END, "="*80)
        amount = self._init_money
        for i in self._records:
            amount += int(i.cost)
            records_insert = ("{:<12s} {:<12s} {:<12s} {:<8s} {:<10s}".format(i.date, i.cat, i.item, i.cost, i.comment))
            listbox.insert(tk.END, records_insert)
        listbox.insert(tk.END, "="*80)
        total_money_label["text"] = f'Now you have {amount} dollars now'

    def find(self, target_cat, listbox, total_money_label):
        """show target category and its subcategory"""
        if target_cat == []:
            print("We cannot find the category!")
            sys.stderr.write("#error: Can't find the category")
            messagebox.showerror('ERROR', 'Cannot find the category.')
            return
        #print("Here's your expense and income records under category:", target_cat[0])
        #print("{:<15s}".format("DATETIME"), "{:<15s}".format("CATEGORIES"), "{:<15s}".format("DESCRIPTION"), \
            #"{:<15s}".format("AMOUNT"), "{:<30s}".format("COMMENT"))
        #print("="*80)
        listbox.delete(0, "end") # clear the listbox
        description = ("{:<12s} {:<12s} {:<12s} {:<8s} {:<10s}".format("DATETIME", "CATEGORIES", "DESCRIPTION", "AMOUNT", "COMMENT"))
        listbox.insert(tk.END, description)
        listbox.insert(tk.END, "="*80)
        amount = 0
        for i in self._records:
            if i.cat in target_cat:
                amount += int(i.cost)
                records_insert = ("{:<12s} {:<12s} {:<12s} {:<8s} {:<10s}".format(i.date, i.cat, i.item, i.cost, i.comment))
                listbox.insert(tk.END, records_insert)
                #i.show()
        #print("="*80)
        listbox.insert(tk.END, "="*80)
        total_money_label["text"] = f'The total amount above is {amount}'
        #print(f'The total amount above is {amount}')
        

    def save(self):
        """save file"""
        print("LOG: save")
        dir_path = os.path.dirname(os.path.realpath(__file__))
        dir_name = dir_path + "/records.txt"
        fh = open(dir_name, "r+")
        fh.truncate(0)
        fh.seek(0)
        fh.write(str(self._init_money)+"\n")
        for i in self._records:
            w = ""
            w += i.date + "," + i.cat + "," + i.item + "," + i.cost + "," + i.comment + "\n"
            fh.write(w)
        #print("Saved successfully!")
        fh.close()

    def update_initial_money(self, money, listbox, total_money_label):
        """update initial money"""
        self._init_money = int(money)
        print("INITIAL MONEY NOW: ", money)

        """update listbox"""
        listbox.delete(0, "end") # clear the listbox
        description = ("{:<12s} {:<12s} {:<12s} {:<8s} {:<10s}".format("DATETIME", "CATEGORIES", "DESCRIPTION", "AMOUNT", "COMMENT"))
        listbox.insert(tk.END, description)
        listbox.insert(tk.END, "="*80)
        amount = self._init_money
        for i in self._records:
            amount += int(i.cost)
            records_insert = ("{:<12s} {:<12s} {:<12s} {:<8s} {:<10s}".format(i.date, i.cat, i.item, i.cost, i.comment))
            listbox.insert(tk.END, records_insert)
        listbox.insert(tk.END, "="*80)
        total_money_label["text"] = f'Now you have {amount} dollars now'
        