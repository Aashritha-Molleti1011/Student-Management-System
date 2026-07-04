import pymysql
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter as tk
# connection later
def connection():
    conn=pymysql.connect(
        host="localhost",user="root",password='',database="students_db"
    )
    return conn

def refreshTable():
    for data in my_tree.get_children():
        my_tree.delete(data)

    for array in read():  # Make sure you have a read() function that returns data
        my_tree.insert(parent='', index="end", iid=array, text="", values=(array), tag="orow")

    my_tree.tag_configure("orow", background="#EEEEEE", font=("Arial", 12))
    my_tree.grid(row=9, column=0, columnspan=11, padx=10, pady=20)


#gui

root = Tk()
root.title("student Registration system")
root.geometry("1080x720")    
my_tree=ttk.Treeview(root)

# functions later

#placeholder for entry
ph1=tk.StringVar()
ph2=tk.StringVar()
ph3=tk.StringVar()
ph4=tk.StringVar()
ph5=tk.StringVar()    

#set placeholder for values
def setph(word,num):
    if num==1:
        ph1.set(word)
    if num==2:
        ph2.set(word)
    if num==3:
        ph3.set(word)
    if num==4:
        ph4.set(word)
    if num==5:
        ph5.set(word)

def read():
    conn=connection()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM student")
    results=cursor.fetchall()
    conn.commit()
    conn.close()
    return results

def add():
    studid=str(studidEntry.get())
    fname=str(fnameEntry.get())
    lname=str(lnameEntry.get())
    address=str(addressEntry.get())
    phone=str(phoneEntry.get()) 

    if(studid=="" or studid==" ") or (fname=="" or fname==" ") or (lname=="" or lname==" ") or (address=="" or address==" ") or (phone=="" or phone==" "):
        messagebox.showinfo("Error","Please fill up the blank entry")
        return
    else:
        try:
            conn=connection()
            cursor=conn.cursor()
            cursor.execute("INSERT INTO student VALUES ('"+studid+"','"+fname+"','"+lname+"','"+address+"','"+phone+"')")
            conn.commit()
            conn.close()
        except:
            messagebox.showinfo("Error","Studid already exists")
            return  
    refreshTable()   

def reset():
    desicion = messagebox.askquestion("Warning!","Delete all data?")
    if desicion != "yes":
        return
    else:
        try:
            conn=connection()
            cursor=conn.cursor()
            cursor.execute("DELETE FROM student")
            conn.commit()
            conn.close()
        except Exception as e:
            messagebox.showerror("Error","sorry an error occured")
            return    
    refreshTable()

def delete():
    desicion = messagebox.askquestion("Warning!","Delete the selected data?")
    if desicion != "yes":
        return
    else:
        selected_item = my_tree.selection()[0]
        deleteData=str(my_tree.item(selected_item)['values'][0])
        try:
            conn=connection()
            cursor=conn.cursor()
            cursor.execute("DELETE FROM student Where studid='"+(deleteData)+"'")
            conn.commit()
            conn.close()
        except Exception as e:
            messagebox.showerror("Error","sorry an error occured")
            return 
           
    refreshTable()

def select():
    try:
        selected_item = my_tree.selection()[0]
        studid=str(my_tree.item(selected_item)['values'][0])
        fname=str(my_tree.item(selected_item)['values'][1])
        lname=str(my_tree.item(selected_item)['values'][2])            
        address=str(my_tree.item(selected_item)['values'][3])
        phone=str(my_tree.item(selected_item)['values'][4])

        setph(studid,1)
        setph(fname,2)
        setph(lname,3)
        setph(address,4)
        setph(phone,5)
    except:
            messagebox.showerror("Error","Please select a data row")

def search():
    studid=str(studidEntry.get())
    fname=str(fnameEntry.get())
    lname=str(lnameEntry.get())
    address=str(addressEntry.get())
    phone=str(phoneEntry.get()) 

    conn=connection()
    cursor=conn.cursor()      
    cursor.execute("SELECT * FROM student WHERE studid='"+
    studid+"' OR fname='"+
    fname+"' OR lname='"+
    lname+"' OR address='"+
    address+"' OR phone='"+
    phone+"'")
    
    try:
        result=cursor.fetchall()
        for num in range(0,5):
            setph(result[0][num],(num+1))

        conn.commit
        conn.close()
    except:
        messagebox.showerror("Error","No data found")
        return    
    refreshTable()

def update():
      selectedstudid=""
      try:
          selected_item = my_tree.selection()[0]
          selectedstudid=str(my_tree.item(selected_item)['values'][0])
      except:
          messagebox.showerror("Error","Please select a data row")
      studid=str(studidEntry.get())
      fname=str(fnameEntry.get())
      lname=str(lnameEntry.get())
      address=str(addressEntry.get())
      phone=str(phoneEntry.get())  
      
      if(studid=="" or studid==" ") or (fname=="" or fname==" ") or (lname=="" or lname==" ") or (address=="" or address==" ") or (phone=="" or phone==" "):
        messagebox.showinfo("Error","Please fill up the blank entry")
        return
      else:
        try:
            conn = connection()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE student
                SET fname=%s,
                    lname=%s,
                    address=%s,
                    phone=%s
                WHERE studid=%s
            """, (fname, lname, address, phone, selectedstudid))

            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Record Updated Successfully")
            refreshTable()

        except Exception as e:
            messagebox.showerror("Error", str(e))

            return  
        refreshTable()



# gvi
label=Label(root,text="Student Registration System (CRUD MATRIX)",font =("Arial Bold",30))
label.grid(row=0,column=0,rowspan=2,padx=50,pady=40)

studidLabel=Label(root,text="Stud ID",font=("Arial",15))
fnameLabel=Label(root,text="Firstname",font=("Arial",15))
lnameLabel=Label(root,text="Lastname",font=("Arial",15))
addressLabel=Label(root,text="Address",font=("Arial",15))
phoneLabel=Label(root,text="Phone",font=("Arial",15))

studidLabel.grid(row=3,column=0,columnspan=1,padx=50,pady=5,sticky='W')
fnameLabel.grid(row=4,column=0,columnspan=1,padx=50,pady=5,sticky='W')
lnameLabel.grid(row=5,column=0,columnspan=1,padx=50,pady=5,sticky='W')
addressLabel.grid(row=6,column=0,columnspan=1,padx=50,pady=5,sticky='W')
phoneLabel.grid(row=7,column=0,columnspan=1,padx=50,pady=5,sticky='W')

#textvariable later
studidEntry=Entry(root,width=55,bd=5,font=("Arial",15),textvariable=ph1)
fnameEntry=Entry(root,width=55,bd=5,font=("Arial",15),textvariable=ph2)
lnameEntry=Entry(root,width=55,bd=5,font=("Arial",15),textvariable=ph3)
addressEntry=Entry(root,width=55,bd=5,font=("Arial",15),textvariable=ph4)
phoneEntry=Entry(root,width=55,bd=5,font=("Arial",15),textvariable=ph5)

studidEntry.grid(row=3,column=0,columnspan=1,padx=50,pady=5,sticky='E')
fnameEntry.grid(row=4,column=0,columnspan=1,padx=50,pady=5,sticky='E')
lnameEntry.grid(row=5,column=0,columnspan=1,padx=50,pady=5,sticky='E')
addressEntry.grid(row=6,column=0,columnspan=1,padx=50,pady=5,sticky='E')
phoneEntry.grid(row=7,column=0,columnspan=1,padx=50,pady=5,sticky='E')

#command later
addBtn=Button(
    root,text='Add',padx=65,pady=10,width=10,bd=5,font=('Arial',15),bg="#EEEEEE",command=add
)
updateBtn=Button(
    root,text='Update',padx=65,pady=10,width=10,bd=5,font=('Arial',15),bg="#EEEEEE",command=update
)
deleteBtn=Button(
    root,text='Delete',padx=65,pady=10,width=10,bd=5,font=('Arial',15),bg="#EEEEEE",command=delete
)
searchBtn=Button(
    root,text='Search',padx=65,pady=10,width=10,bd=5,font=('Arial',15),bg="#EEEEEE",command=search
)
resetBtn=Button(
    root,text='Reset',padx=65,pady=10,width=10,bd=5,font=('Arial',15),bg="#EEEEEE",command=reset
)
selectBtn=Button(
    root,text='Select',padx=65,pady=10,width=10,bd=5,font=('Arial',15),bg="#EEEEEE",command=select
)
addBtn.grid(row=3,column=5,columnspan=1,rowspan=1)
updateBtn.grid(row=4,column=5,columnspan=1,rowspan=1)
deleteBtn.grid(row=5,column=5,columnspan=1,rowspan=1)
searchBtn.grid(row=6,column=5,columnspan=1,rowspan=1)  
resetBtn.grid(row=7,column=5,columnspan=1,rowspan=1)
selectBtn.grid(row=8,column=5,columnspan=1,rowspan=1)

style=ttk.Style()
style.configure("Treeview.Heading",font=("Arial Bold",15))
my_tree['columns']=("Stud ID","Firstname","Lastname","Address","Phone")

my_tree.column("#0",width=0,stretch=NO)
my_tree.column("Stud ID",anchor=W,width=170)
my_tree.column("Firstname",anchor=W,width=150)
my_tree.column("Lastname",anchor=W,width=150)
my_tree.column("Address",anchor=W,width=165)
my_tree.column("Phone",anchor=W,width=150)

my_tree.heading("Stud ID",text="Student ID",anchor=W)
my_tree.heading("Firstname",text="Firstname",anchor=W)
my_tree.heading("Lastname",text="Lastname",anchor=W)
my_tree.heading("Address",text="Address",anchor=W)
my_tree.heading("Phone",text="Phone",anchor=W)

refreshTable()
root.mainloop()