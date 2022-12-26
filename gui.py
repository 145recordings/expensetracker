import tkinter as tk
from tkcalendar import DateEntry


class Gui:

    total = 0.00

    #constructor
    def __init__(self,root):
        self.root = root
        self.constructMain()

    #initialize gui
    def constructMain(self):
    
        self.frame = tk.Frame(master=self.root)
        self.frame.pack()

        self.frame.option_add("*Font","Helvetica")

        self.lbl_title = tk.Label(master=self.frame,text="Expense Tracker",font=("Helvetica",18))
        self.lbl_title.grid(row=0,column=0,columnspan=5)

        
        self.listBox = tk.Listbox(self.frame, width=40,height=15)
        self.listBox.grid(row=2,column=0,columnspan=5,padx=5,pady=5)

        #Scrollbar code
        #self.scrollbar = tk.Scrollbar(self.frame)
        #self.scrollbar.config(command=self.listBox.yview)
        #self.scrollbar.grid(row=2,column=1, sticky=tk.NS)
        #self.listBox.config(yscrollcommand = self.scrollbar.set)

        self.btn_delete_entry = tk.Button(master=self.frame,text="Delete",command=self.deleteEntry)
        self.btn_delete_entry.grid(row=3,column=0)

        self.btn_edit_entry = tk.Button(master=self.frame,text="Edit",command=self.editEntry)
        self.btn_edit_entry.grid(row=3,column=1)

        self.btn_new_entry = tk.Button(master=self.frame,text="New",command=self.addEntry)
        self.btn_new_entry.grid(row=3,column=2)

        self.lbl_total = tk.Label(master=self.frame,text="Total: $" + str(self.total))
        self.lbl_total.grid(row=4,column=0,columnspan=3)


        #reads expenses.txt into a variable and splits it into a list based on a comma
        try:
            self.txt_file = open("expenses.txt","r")
            self.file_content = self.txt_file.read()
            self.file_list = self.file_content.split(",")
        except FileNotFoundError:
            print("File not found error...")
        finally:
            self.txt_file.close()

        
        #loads list box with current expenses from text file
        if self.file_list:
            for x in range(0,len(self.file_list),3):
                try:
                    namePlaceholder = self.file_list[x]
                    pricePlaceholder = self.file_list[x+1]
                    datePlaceholder = self.file_list[x+2]
                    self.total += float(pricePlaceholder)
                    self.listBox.insert(tk.END,namePlaceholder + " - $" + pricePlaceholder + " - " + datePlaceholder)
                    self.lbl_total.config(text="Total: " + f'${self.total:.2f}')
                except:
                    print("initial list box load error...")
        else:
            self.lbl_total.config(text="Total: " + f'${self.total:.2f}')
                
    #contains top level window for adding an entry plus relevant logic
    def addEntry(self):
        #writes to the text file all entry boxes and populates list box with said info
        def saveEntry():
            #erases text file and loads text file with info from file_list
            def eraseAndOverwrite():
                expenses_file = open("expenses.txt","w")
                expenses_file.close()
                expenses_file = open("expenses.txt","a")
                
                #write to file from file_list
                for x in range(len(self.file_list)):
                    if x == len(self.file_list) - 1:
                        print("reached end")
                        expenses_file.write(self.file_list[x])
                        break                       

                    expenses_file.write(self.file_list[x] + ",")
                    print(x)
                    
                expenses_file.close()


            if self.file_list != []:
                if self.file_list[0] == '':
                    self.file_list = []

            #input validation for price
            if len(self.entry_box_price.get()) == 0:
                return
            #if in any anything returns true it returns true
            elif any(i.isalpha() for i in self.entry_box_price.get()):
                return


            if len(self.entry_box_name.get()) == 0:
                self.file_list.append(" ")
                eraseAndOverwrite()
            else:
                self.file_list.append(self.entry_box_name.get())
                eraseAndOverwrite()

            if "$" in self.entry_box_price.get():
                    self.file_list.append(self.entry_box_price.get().strip("$"))
                    eraseAndOverwrite()               
            else:
                self.file_list.append(self.entry_box_price.get())
                eraseAndOverwrite()

            #append date to file from date widget
            self.file_list.append(str(self.date.get_date()))
            eraseAndOverwrite()
            
            
            #reset listbox and total and repopulate them
            self.listBox.delete(0,tk.END)
            self.total = 0
            for x in range(0,len(self.file_list),3):
                try:
                    namePlaceholder = self.file_list[x]
                    pricePlaceholder = self.file_list[x+1]
                    datePlaceholder = self.file_list[x+2]
                    self.total += float(pricePlaceholder)
                    self.listBox.insert(tk.END,namePlaceholder + " - $" + pricePlaceholder + " - " + datePlaceholder)
                    self.lbl_total.config(text="Total: " + f'${self.total:.2f}')
                except:
                    print("listbox load after new entry error...")
            
            print("Saving...")
            self.addEntryWindow.destroy()
            

        def cancelEntry():
            print("Canceling...")
            self.addEntryWindow.destroy()
            


        #creates the top level window addEntryWindow
        self.addEntryWindow = tk.Toplevel(master=self.frame)
        self.addEntryWindow.title("Add Entry")
        self.addEntryWindow.geometry("250x250")
        self.addEntryWindow.resizable(False,False)

        self.lbl_entry_name_prompt = tk.Label(master=self.addEntryWindow,text="Enter new entry name")
        self.lbl_entry_name_prompt.pack()
        self.entry_box_name = tk.Entry(master=self.addEntryWindow)
        self.entry_box_name.pack()
        self.lbl_entry_price_prompt = tk.Label(master=self.addEntryWindow,text="Enter new entry price")
        self.lbl_entry_price_prompt.pack()
        self.entry_box_price = tk.Entry(master=self.addEntryWindow)
        self.entry_box_price.pack()
        self.lbl_date_prompt = tk.Label(master=self.addEntryWindow,text="Select date")
        self.lbl_date_prompt.pack()
        self.date = DateEntry(master=self.addEntryWindow, width=16)
        self.date.pack()

        self.btn_save_entry = tk.Button(master=self.addEntryWindow,text="Save",command=saveEntry)
        self.btn_save_entry.pack()
        self.btn_cancel_entry = tk.Button(master=self.addEntryWindow,text="Cancel",command=cancelEntry)
        self.btn_cancel_entry.pack()

    #remove it from list, then rewrite the file with that list
    def deleteEntry(self):

        #get index of selection
        index = self.listBox.curselection()
        #remove proper items from file_list
        self.file_list.pop(index[0]*3)
        self.file_list.pop(index[0]*3)
        self.file_list.pop(index[0]*3)
        #clear file and rewrite file with file_list
        expenses_file = open("expenses.txt","w")
        expenses_file.close()
        expenses_file = open("expenses.txt","a")
        for x in range(len(self.file_list)):
            if x == len(self.file_list) - 1:
                expenses_file.write(self.file_list[x])
                break
            expenses_file.write(self.file_list[x] + ",")
                    
        expenses_file.close()

        #erase list box and repopulate it using file_list
        self.listBox.delete(0,tk.END)
        self.total = 0
        for x in range(0,len(self.file_list),3):
            try:
                namePlaceholder = self.file_list[x]
                pricePlaceholder = self.file_list[x+1]
                datePlaceholder = self.file_list[x+2]
                self.total += float(pricePlaceholder)
                self.listBox.insert(tk.END,namePlaceholder + " - $" + pricePlaceholder + " - " + datePlaceholder)
                self.lbl_total.config(text="Total: " + f'${self.total:.2f}')
            except:
                print("listbox load after new entry error...")
        if len(self.file_list) == 0:
            self.lbl_total.config(text="Total: " + f'${self.total:.2f}')

    #contains copy of addEntry with appropiate edits, including previous name and price from selection
    def editEntry(self):

        name = ""
        price = ""
        #get index of selection
        index = self.listBox.curselection()
        #read text file into file_list and fill name and price with selection
        try:
            txt_file = open("expenses.txt","r")
            file_content = txt_file.read()
            file_list = file_content.split(",")
            name = file_list[index[0]*3]
            price = file_list[index[0]*3+1]

        except FileNotFoundError:
            print("File not found error...")
        finally:
            self.txt_file.close()

        #begin addEntry copy with edits
        #re-insert the list to the listbox
        def saveEntry():

            def eraseAndOverwrite():
                expenses_file = open("expenses.txt","w")
                expenses_file.close()
                expenses_file = open("expenses.txt","a")
                
                #write to file from file_list
                for x in range(len(self.file_list)):
                    if x == len(self.file_list) - 1:
                        print("reached end")
                        expenses_file.write(self.file_list[x])
                        break                       

                    expenses_file.write(self.file_list[x] + ",")
                    print(x)
                    
                expenses_file.close()


            if self.file_list != []:
                if self.file_list[0] == '':
                    self.file_list = []

            #input validation for price
            if len(self.entry_box_price.get()) == 0:
                return
            #if in any anything returns true it returns true
            #cease function if price includes any alpha characters
            elif any(i.isalpha() for i in self.entry_box_price.get()):
                return

            #removes name from list at selection and adds " " or entry
            if len(self.entry_box_name.get()) == 0:
                self.file_list.pop(index[0]*3)
                self.file_list.insert(index[0]*3," ")
                eraseAndOverwrite()
            else:
                self.file_list.pop(index[0]*3)
                self.file_list.insert(index[0]*3,self.entry_box_name.get())
                eraseAndOverwrite()

            #remove price from list at selection and strip $ if present
            if "$" in self.entry_box_price.get():
                self.file_list.pop(index[0]*3+1)
                self.file_list.insert(index[0]*3+1,self.entry_box_price.get().strip("$"))
                eraseAndOverwrite()               
            else:
                self.file_list.pop(index[0]*3+1)
                self.file_list.insert(index[0]*3+1,self.entry_box_price.get())
                eraseAndOverwrite()

            #erase previous date and append new date to file from date widget
            self.file_list.pop(index[0]*3+2)
            self.file_list.insert(index[0]*3+2,str(self.date.get_date()))
            eraseAndOverwrite()
            
            
            
            #reset listbox and total and repopulate them using file_list
            self.listBox.delete(0,tk.END)
            self.total = 0
            for x in range(0,len(self.file_list),3):
                try:
                    namePlaceholder = self.file_list[x]
                    pricePlaceholder = self.file_list[x+1]
                    datePlaceholder = self.file_list[x+2]
                    self.total += float(pricePlaceholder)
                    self.listBox.insert(tk.END,namePlaceholder + " - $" + pricePlaceholder + " - " + datePlaceholder)
                    self.lbl_total.config(text="Total: " + f'${self.total:.2f}')
                except:
                    print("listbox load after new entry error...")

            
            print("Saving...")
            self.addEntryWindow.destroy()
            
        #logic for cancel button
        def cancelEntry():
            print("Canceling...")
            self.addEntryWindow.destroy()
            


        #creates the top level window for editEntry
        self.addEntryWindow = tk.Toplevel(master=self.frame)
        self.addEntryWindow.title("Edit Entry")
        self.addEntryWindow.geometry("250x250")
        self.addEntryWindow.resizable(False,False)

        self.lbl_entry_name_prompt = tk.Label(master=self.addEntryWindow,text="Enter new entry name")
        self.lbl_entry_name_prompt.pack()
        self.entry_box_name = tk.Entry(master=self.addEntryWindow)
        self.entry_box_name.insert(0,name)
        self.entry_box_name.pack()
        self.lbl_entry_price_prompt = tk.Label(master=self.addEntryWindow,text="Enter new entry price")
        self.lbl_entry_price_prompt.pack()
        self.entry_box_price = tk.Entry(master=self.addEntryWindow)
        self.entry_box_price.insert(0,price)
        self.entry_box_price.pack()
        self.lbl_date_prompt = tk.Label(master=self.addEntryWindow,text="Select date")
        self.lbl_date_prompt.pack()
        self.date = DateEntry(master=self.addEntryWindow, width=16)
        self.date.pack()

        self.btn_save_entry = tk.Button(master=self.addEntryWindow,text="Save edit",command=saveEntry)
        self.btn_save_entry.pack()
        self.btn_cancel_entry = tk.Button(master=self.addEntryWindow,text="Cancel",command=cancelEntry)
        self.btn_cancel_entry.pack()
        
        
        




        

