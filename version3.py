import sys, os
from typing import Type

""" created by Ricky Lai 2022.5.26 """

class Record:
    """Represent a record."""
    def __init__(self, cat, item, cost, comment = ""):
        """initialize"""
        self._cat = cat
        self._item = item
        self._cost = cost
        self._comment = comment[:-1] # ignore '\n' 
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
        print("{:<15s}".format(self._cat), "{:<15s}".format(self._item),  \
            "{:<15s}".format(self._cost), "{:<30s}".format(self._comment))

class Categories:
    """Maintain the category list and provide some methods."""
    def __init__(self):
        """initialize"""
        self._categories = ['expense', ['food', ['meal', 'snack', 'drink'], \
            'transportation', ['bus', 'railway']], 'income', ['salary', 'bonus']]
    
    def view(self):
        """recursively view categories"""
        def n(L, prefix = ()):
            if type(L) in {list, tuple}:
                i = 0
                for v in L:
                    if type(v) not in {list, tuple}:
                        i += 1
                    n(v, prefix+(i, ))
            else:
                s = " "*2*(len(prefix)-1)
                s += ". " + L
                print(s)
        n(self._categories)
 
    def is_category_valid(self, cat_name):
        """check if cat_name is in categories"""
        def n(L, name):
            if type(L) in {list, tuple}:
                for v in L:
                    p = n(v, cat_name)
                    if p == True:
                       return True
            return L == cat_name
        return n(self._categories, cat_name)

    def find_subcategories(self, cat_name):
        """use yield to implement find_subcategories"""
        def find_subcategories_gen(category, categories, found=False):
            if type(categories) == list:
                for index, child in enumerate(categories):
                    yield from find_subcategories_gen(category, child, found)
                    if child == category and index + 1 < len(categories) \
                        and type(categories[index + 1]) == list:
                        yield from find_subcategories_gen(category, categories[index + 1], True)
            else:
                if categories == category or found == True:
                    yield categories
        return [i for i in find_subcategories_gen(cat_name, self._categories)]   

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
            total = input("How much money do you have?")
            try:
                total = str(int(total))
            except:
                print("Invalid value for money. Set to 0 by default.")
                total = "0"
            fh.write(total)
            self._records = []
        else:
            if filesize == 0: # empty file
                total = input("How much money do you have?")
                try:
                    total = str(int(total))
                except:
                    print("Invalid value for money. Set to 0 by default.")
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
                    cat_name = temp[0]
                    item = temp[1]
                    cost = temp[2]
                    comment = temp[3]
                    self._records.append(Record(cat_name, item, cost, comment))                 
        finally:
            self._init_money = int(total)
    
    def add(self, record, cat: type[Categories]): # <IMPORTANT> cat is a class Categories
        """add record to Records object self._records[]"""
        try:
            temp = record.split(" ")
            cat_name = temp[0]
            item = temp[1]
            cost = temp[2]
        except ValueError:
            print("Invalid value for money.")
            print("Fail to add a record")
            sys.stderr.write("#error: VALUE ERROR")
            return
        except IndexError:
            print("The format of a record should be like this: breakfast -50.")
            print("Fail to add a record")
            sys.stderr.write("#error: FORMAT ERROR")
            return 

        if cat.is_category_valid(cat_name) == False:
            print("Can't find the category")
            sys.stderr.write("#error: CATEGORY ERROR")
            return
        
        ans = input(f'Would you like to add comment for {item} (y/n)?')
        if (ans == 'y' or ans == 'Y'):
            comment = input("Please input you comment:\n")
            comment += "\n"
            self._records.append(Record(cat_name, item, cost, comment))
        else:
            self._records.append(Record(cat_name, item, cost))
    
    def view(self):
        """it shows every records store in this Records object"""
        print("{:<15s}".format("Categories"), "{:<15s}".format("Description"), \
            "{:<15s}".format("AMOUNT"), "{:<30s}".format("COMMENT"))
        print("="*80)
        amount = self._init_money
        for i in self._records:
            amount += int(i.cost)
            i.show()
        print("="*80)
        print(f'YOU HAVE {amount} dollars now')
    
    def delete(self, record):
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
            print("Invalid format.")
            print("Fail to delete a record")
            return
        del_list = [] # we store the deleted records' index in del_list 
        for index, i in enumerate(self._records):
            if i.cat == cat_name and i.item == item and i.cost == str(cost):
                if del_num == 0:
                    print(f'delete {cat_name} {item} {cost} successfully!')
                    del_list.append(index)
                    del_num += 1
                else:
                    ans = input("we found one more same records, do u want to del it (y/n)")
                    if (ans == "y" or ans == "Y"):
                        print(f'delete {cat_name} {item} {cost} successfully!')
                        del_list.append(index)
                        del_num += 1
        for n, i in enumerate(del_list):
            del self._records[i-n] # i-n is the right index of the deleted item 
        print(f'we delete {del_num} record(s)')
        if del_num == 0:
            print(f'There\'s no record with {cat_name} {item} {cost}')
            print("Fail to delete a record")
            return
    
    def find(self, target_cat):
        """show target category and its subcategory"""
        if target_cat == []:
            print("We cannot find the category!")
            return
        print("Here's your expense and income records under category:", target_cat[0])
        print("{:<15s}".format("Categories"), "{:<15s}".format("Description"), \
            "{:<15s}".format("AMOUNT"), "{:<30s}".format("COMMENT"))
        print("="*80)
        amount = 0
        for i in self._records:
            if i.cat in target_cat:
                amount += int(i.cost)
                i.show()
        print("="*80)
        print(f'The total amount above is {amount}')
        

    def save(self):
        """save file"""
        dir_path = os.path.dirname(os.path.realpath(__file__))
        dir_name = dir_path + "/records.txt"
        fh = open(dir_name, "r+")
        fh.truncate(0)
        fh.seek(0)
        fh.write(str(self._init_money)+"\n")
        for i in self._records:
            w = ""
            w += i.cat + "," + i.item + "," + i.cost + "," + i.comment + "\n"
            fh.write(w)
        print("Saved successfully!")
        fh.close()

categories = Categories()
records = Records()
 
while True:
    command = input("\nWhat do you want to do (add/delete/view/view categories/find/exit)? ")
    if command == "add":
        record = input("Add an expense or income record with (cat item cost):\n")
        records.add(record, categories)
    elif command == "view":
        records.view()
    elif command == "delete":
        delete_record = input("Which record do you want to delete? (cat item cost)")
        records.delete(delete_record)
    elif command == "view categories":
        categories.view()
    elif command == "find":
        category = input('Which category do you want to find? ')
        target_categories = categories.find_subcategories(category)
        records.find(target_categories)
    elif command == "exit":
        records.save()
        break
    else:
        sys.stderr.write("Invalid command. Try again.\n")    

