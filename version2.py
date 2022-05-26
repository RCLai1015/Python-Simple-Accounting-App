import sys, os

global fh # used everywhere
global spend # used in view(int, list)

def initialize():
    try:
        global fh
        global spend
        spend = 0
        fh = open("records.txt", "r+")
        filesize = os.path.getsize("records.txt") # if we lost the file contents
    except:
        fh = open('records.txt', "w+")
        total = input("How much money do you have?")
        try:
            total = int(total)
        except:
            print("Invalid value for money. Set to 0 by default.")
            total = "0"
        fh.write(str(total))
        return int(total), []
    else:
        if filesize == 0: # empty file
            total = input("How much money do you have?")
            try:
                total = int(total)
            except:
                print("Invalid value for money. Set to 0 by default.")
                total = "0"
            fh.write(str(total))
            return int(total), []
        else:
            print("Welcome Back!")
            total = fh.readline()
            acc = fh.readlines()
            return int(total), acc

def add(r): # add records
    global spend
    add_item = input("Add an expense or income record with description and amount (and comment):\n")
    try:
        check = add_item.split(" ")
        item = check[0]
        cost = int(check[1])
    except ValueError:
        print("Invalid value for money.")
        print("Fail to add a record")
        sys.stderr.write("#error: VALUE ERROR")
        return r
    except IndexError:
        print("The format of a record should be like this: breakfast -50.")
        print("Fail to add a record")
        sys.stderr.write("#error: FORMAT ERROR")
        return r
    
    ans = input(f'Would you like to add comment for {item} (y/n)?')
    add = ""
    if (ans == 'y' or ans == 'Y'):
        comment = input("Please input you comment:\n")
        add += item+","+str(cost)+","+comment+"\n"
    else:
        add += item+","+str(cost)+"\n"
    spend += cost
    r.append(add)
    return r

def delete(r): # delete records
    global spend
    del_item = input("Which record do you want to delete (item,cost)")
    if (del_item == "exit"):
        return r
    only_one = 0
    try:
        check = del_item.split(",")
        item = check[0]
        cost = int(check[1])
    except (ValueError, IndexError) as err:
        print("Invalid format.")
        print("Fail to delete a record.")
        return r
    for i in r:
        if (i == "\n"): # deal with redundant nextline in .txt
            continue 
        spec = i[:-1].split(",")
        d_item = spec[0]
        d_cost = int(spec[1])
        if (str(item) == str(d_item) and cost == d_cost):
            if only_one == 0:
                r.remove(i)
                spend -= cost
                print(f'delete {item} {cost} successfully!')
            else:
                ans = input("we found one more same records, do u want to del it (y/n)")
                if (ans == "y" or ans == "Y"):
                    spend -= cost
                    r.remove(i)
                elif (ans == "n" or ans == "N"):
                    print(f'delete {only_one} record(s)')
                    return r
            only_one += 1
    if only_one == 0:
        print(f'There\'s no record with {item}, {cost}')
        print("Fail to delete a record.")
    return r

def view(im, r): # records
    print("{:<15s}".format("Description"), "{:<15s}".format("AMOUNT"), "{:<15s}".format("COMMENT"))
    print("="*50)
    for i in r:
        if (i == "\n"):
            continue
        spec = i[:-1].split(",")
        item = spec[0]
        cost = int(spec[1])
        try: # check if i has comment
            comment = spec[2]
        except:
            print("{:<15s}".format(item), "{:<15d}".format(cost))
        else:
            print("{:<15s}".format(item), "{:<15d}".format(cost), "{:<15s}".format(comment))

    print("="*50)
    print(f'Now you have {im+spend} dollars.')

def save(im, r): # save data to records.txt
    im += spend
    fh.seek(0)
    fh.write(str(im)+"\n")
    for i in r:
        w = ""
        w += i
        fh.write(w)
    fh.close()

# main Ruei-Chi Lai 2022.4.17
initial_money, records = initialize()

while True:
    command = input("\nWhat do you want to do (add/view/delete/exit)?")
    if command == "add":
        records = add(records)
    elif command == "view":
        view(initial_money, records)
    elif command == "delete":
        records = delete(records)
    elif command == "exit":
        save(initial_money, records)
        break
    else:
        sys.stderr.write("Invalid command. Try again.\n")
