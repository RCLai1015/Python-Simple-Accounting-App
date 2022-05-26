#Ricky Lai 
accounting = []
nums = 0
total = int(input("How much money do you have?"))
print("I have", total, "dollars!")
while True:
    record = input("Add an expense or income record with description and amount:")
    if record == "QUIT":
        print("{:<15s}".format("ITEMS"), "{:<15s}".format("IN/OUTCOMES"), "{:<15s}".format("CURRENT"))
        for i in range(0, nums*3, 3):
            print("{:<15s}".format(accounting[i]), "{:<15d}".format(accounting[i+1]), "{:<15d}".format(accounting[i+2]))
        break   
    accounting.append(record.split(" ")[0]) #1
    balance = int(record.split(" ")[1])
    accounting.append(balance) #2
    total = total + balance
    accounting.append(total) #3
    nums += 1
print("Now you have", total, "dollars")

