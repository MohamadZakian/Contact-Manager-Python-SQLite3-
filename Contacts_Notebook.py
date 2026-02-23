
from tkinter import *
from tkinter import messagebox
import sqlite3

##### Creating Database
conn=sqlite3.connect("Contacts_Notebook.db")
cur=conn.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS Contacts_Database (First_name TEXT, Last_name TEXT, Address TEXT, Phone TEXT UNIQUE, Gender TEXT)")
conn.commit()



##### UI
root=Tk()
root.title("Contact Manager_mz")
root.geometry("600x600")

##### UI Labels
Label(root, text="First Name", font=("Arial",15), fg="black").grid(row=1, column=0)
entry1=Entry(root)
entry1.grid(row=2, column=0)

Label(root, text="Last Name", font=("Arial",15), fg="black").grid(row=3, column=0)
entry2=Entry(root)
entry2.grid(row=4, column=0)

Label(root, text="Address", font=("Arial",15), fg="black").grid(row=5, column=0)
entry3=Entry(root)
entry3.grid(row=6, column=0)

Label(root, text="Phone", font=("Arial",15), fg="black").grid(row=7, column=0)
entry4=Entry(root)
entry4.grid(row=8, column=0)

##### Entry for City Code
entry5=None

##### UI Radiobuttons Male/Female
gender_var=StringVar()
Radiobutton(root, text="Male", font=("Arial",10), fg="black", variable=gender_var, value="Male").grid(row=11, column=0)
Radiobutton(root, text="Female", font=("Arial",10), fg="black", variable=gender_var, value="Female").grid(row=12, column=0)





##################################################
##################################################
############## FUNCTION TO SAVE DATA #############
##################################################
##################################################

def save_data():
    global entry5
    
    name=entry1.get()
    lastname=entry2.get()
    address=entry3.get()
    phone=entry4.get()
    gender=gender_var.get()
     
    if not phone.isdigit():
        messagebox.showerror("Error","Phone must contain only digits!")
        return
    
    if gender == "":
        messagebox.showerror("Error","Please select gender!")
        return
    
    if len(phone) > 11:
        messagebox.showerror("Error","Phone number cannot exceed 11 digits!")
        return
    
    if len(phone) == 8 and not phone.startswith("09"):
        if entry5 is None:
            Label(root, text="City Code", font=("Arial",15), fg="black").grid(row=9, column=0)
            entry5=Entry(root)
            entry5.grid(row=10, column=0)
            messagebox.showinfo("Info","Please enter city code and press SAVE again")
            return
        
        elif entry5.get() == "":
            messagebox.showerror("Error","City Code is required!")
            return
            

        elif not entry5.get().isdigit():
            messagebox.showerror("Error","City Code must contain only digits!")
            return
        
            
        phone = entry5.get() + phone
    
    
   
    conn=sqlite3.connect("Contacts_Notebook.db")
    cur=conn.cursor()

    ##### Try: saving new contacts      ##### Except: not to save repetitive contacts
    try:
        conn.execute("INSERT INTO Contacts_Database (First_name, Last_name, Address, Phone, Gender) VALUES (?, ?, ?, ?, ?)",(name, lastname, address, phone, gender))
        conn.commit()
        messagebox.showinfo("Success","Data saved successfully!")

    except sqlite3.IntegrityError:
        messagebox.showerror("Error","This number already exists!")

    conn.close()





##################################################
##################################################
############ FUNCTION TO SEARCH DATA #############
##################################################
##################################################
                
def search_data():
    name=entry1.get()
    lastname=entry2.get()
    address=entry3.get()
    phone=entry4.get()

    conn=sqlite3.connect("Contacts_Notebook.db")
    cur=conn.cursor()
    
    ##### Searching data based on all entries 
    if  name != "":
        cur.execute("SELECT * FROM Contacts_Database WHERE First_name=?", (name,))
    elif  lastname != "":
        cur.execute("SELECT * FROM Contacts_Database WHERE Last_name=?", (lastname,))
    elif  address != "":
        cur.execute("SELECT * FROM Contacts_Database WHERE Address=?", (address,))
    elif  phone != "":
        cur.execute("SELECT * FROM Contacts_Database WHERE Phone=?", (phone,))
        
    else:
        messagebox.showerror("Error","Please enter something to search!")
        return
    
    result=cur.fetchone()
    conn.close()

    ##### Deleting and Inserting data automatically
    if result:
        entry1.delete(0, END)
        entry2.delete(0, END)
        entry3.delete(0, END)
        entry4.delete(0, END)

        entry1.insert(0, result[0])
        entry2.insert(0, result[1])
        entry3.insert(0, result[2])
        entry4.insert(0, result[3])

        gender_var.set(result[4])
    else:
        messagebox.showerror("Error", "Contact not found!")




##################################################
##################################################
############ FUNCTION TO EDIT DATA ###############
##################################################
##################################################

def edit_data():
    name=entry1.get()
    lastname=entry2.get()
    address=entry3.get()
    phone=entry4.get()
    gender=gender_var.get()
    
    ##### Correct phone number is required before applying any changes
    if phone == "":
        messagebox.showerror("Error","Please enter Phone number to edit contact!")
        return
    
    conn=sqlite3.connect("Contacts_Notebook.db")
    cur=conn.cursor()
        
    cur.execute("SELECT * FROM Contacts_Database WHERE Phone=?", (phone,))
    result=cur.fetchone()

    if not result:
        messagebox.showerror("Error","This Phone number does not exist!")
        conn.close()
        return
    
    
    
    ok_cancel=messagebox.askokcancel("Confirm","Please confirm to apply changes")
    
    if ok_cancel:
        cur.execute("UPDATE Contacts_Database SET First_name=?, Last_name=?, Address=? WHERE Phone=?", (name, lastname, address, phone))
        conn.commit()
        messagebox.showinfo("Success","Changes applied successfully!")
    
    conn.close()




##################################################
##################################################
############ FUNCTION TO DELETE DATA #############
##################################################
##################################################

def delete_data():
    phone=entry4.get()

    ##### Correct phone number is required before deleting data 
    if phone == "":
        messagebox.showerror("Error","Please enter Phone number to delete contact!")
        return
    
    conn=sqlite3.connect("Contacts_Notebook.db")
    cur=conn.cursor()
        
    cur.execute("SELECT * FROM Contacts_Database WHERE Phone=?", (phone,))
    result=cur.fetchone()

    if not result:
        messagebox.showerror("Error","This Phone number does not exist!")
        conn.close()
        return
    
    
    
    ok_cancel=messagebox.askokcancel("Confirm","Please confirm to delete this contact")
    
    if ok_cancel:
        cur.execute("DELETE FROM Contacts_Database WHERE Phone=?", (phone,))
        conn.commit()
        messagebox.showinfo("Success","Contact removed successfully!")
    
    conn.close()




##################################################
##################################################
############ FUNCTION TO COUNT DATA ##############
##################################################
##################################################

def number_of_contacts():
    conn=sqlite3.connect("Contacts_Notebook.db")
    cur=conn.cursor()
    
    cur.execute("SELECT Phone FROM Contacts_Database") 
    phones=cur.fetchall()
    
    total=len(phones)

    ##### Creating empty lists to separate and count contacts based on mobile/home
    mobile=[]
    landline=[]
    for i in phones:
        phone=i[0]

        if phone.startswith("09"):
            mobile.append(phone)
        else:
            landline.append(phone)
    
    totalmobile=len(mobile)
    totallandline=len(landline)

    conn.close()
            
    messagebox.showinfo("Info",f"Total number of contacts: {total}\n" f"Mobile: {totalmobile}\n" f"Landline: {totallandline}")




##################################################
##################################################
############ FUNCTION TO TYPE NUMBERS ############
##################################################
##################################################

def number_keys(num):
    
    ##### Focus is on the current active entry 
    current=root.focus_get()
    if isinstance(current, Entry):
        current.insert(END, num)
    


##### Buttons for Keypad

button_one=Button(root, text="1",font=("Arial", 15), fg="white", bg="dark blue",command=lambda: number_keys("1")).grid(row=3, column=2)
button_two=Button(root, text="2",font=("Arial", 15), fg="white", bg="dark blue",command=lambda: number_keys("2")).grid(row=3, column=3)
button_three=Button(root, text="3",font=("Arial", 15), fg="white", bg="dark blue",command=lambda: number_keys("3")).grid(row=3, column=4)

button_four=Button(root, text="4",font=("Arial", 15), fg="white", bg="dark blue",command=lambda: number_keys("4")).grid(row=4, column=2)
button_five=Button(root, text="5",font=("Arial", 15), fg="white", bg="dark blue",command=lambda: number_keys("5")).grid(row=4, column=3)
button_six=Button(root, text="6",font=("Arial", 15), fg="white", bg="dark blue",command=lambda: number_keys("6")).grid(row=4, column=4)

button_seven=Button(root, text="7",font=("Arial", 15), fg="white", bg="dark blue",command=lambda: number_keys("7")).grid(row=5, column=2)
button_eight=Button(root, text="8",font=("Arial", 15), fg="white", bg="dark blue",command=lambda: number_keys("8")).grid(row=5, column=3)
button_nine=Button(root, text="9",font=("Arial", 15), fg="white", bg="dark blue",command=lambda: number_keys("9")).grid(row=5, column=4) 

button_zero=Button(root, text="0",font=("Arial", 15), fg="white", bg="dark blue",command=lambda: number_keys("0")).grid(row=6, column=3)



##### Buttons for Functions

button_save=Button(root,text="save",font=("Arial", 10), fg="dark blue", bg="dark gray", command=save_data).grid(row=14, column=1)
button_search=Button(root,text="search",font=("Arial", 10), fg="dark blue", bg="dark gray", command=search_data).grid(row=15, column=1)
button_edit=Button(root,text="edit",font=("Arial", 10), fg="dark blue", bg="dark gray", command=edit_data).grid(row=16, column=1)
button_delete=Button(root,text="delete",font=("Arial", 10), fg="dark blue", bg="dark gray", command=delete_data).grid(row=17, column=1)
button_number_of_contacts=Button(root,text="number of contacts",font=("Arial", 10), fg="dark blue", bg="dark gray", command=number_of_contacts).grid(row=18, column=1)




root.mainloop()