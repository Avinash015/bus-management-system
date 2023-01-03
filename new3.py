import datetime
from tkinter import *
import tkinter.messagebox as mb
from tkinter import ttk
from tkcalendar import DateEntry  # pip install tkcalendar
import sqlite3
import sys
import os


# Creating the universal font variables
headlabelfont = ("Noto Sans CJK TC", 15, 'bold')
labelfont = ('Garamond', 14)
entryfont = ('Garamond', 12)

# Connecting to the Database where all information will be stored
connector = sqlite3.connect(r'BusManagement.db')
cursor = connector.cursor()

connector.execute(
"CREATE TABLE IF NOT EXISTS BUS_MANAGEMENT (SERVICE_NO INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, SOURCE TEXT, DESTINATION TEXT, TYPE_OF_BUS TEXT,  FARE INTEGER)"
)

# Creating the functions
def reset_fields():
   global service_no_strvar, source_strvar, destination_strvar, type_of_bus_strvar, fare_strvar

   for i in ['service_no_strvar', 'source_strvar', 'destination_strvar', 'type_of_bus_strvar', 'fare_strvar']:
       exec(f"{i}.set('')")

def reset_form():
   global tree
   tree.delete(*tree.get_children())

   reset_fields()

def display_records():
   tree.delete(*tree.get_children())

   curr = connector.execute('SELECT * FROM BUS_MANAGEMENT')
   data = curr.fetchall()

   for records in data:
       tree.insert('', END, values=records)

def add_record():
   global service_no_strvar, source_strvar, type_of_bus_strvar, destination_strvar,fare_strvar

   serviceno= service_no_strvar.get()
   source = source_strvar.get()
   destination = type_of_bus_strvar.get()
   typeofbus = destination_strvar.get()
   fare = fare_strvar.get()

   if not serviceno or not source or not  destination or not typeofbus or not fare:
       mb.showerror('Error!', "Please fill all the missing fields!!")
   else:
       try:
           connector.execute(
           'INSERT INTO BUS_MANAGEMENT (SERVICE_NO,SOURCE,DESTINATION,TYPE_OF_BUS,FARE) VALUES (?,?,?,?,?)', (serviceno,source,destination,typeofbus,fare)
           )
           connector.commit()
           mb.showinfo('Record added', f"Record of {serviceno} was successfully added")
           reset_fields()
           display_records()
       except:
           mb.showerror('Wrong type', 'The type of the values entered is not accurate. Pls note that the contact field can only contain numbers')

def remove_record():
   if not tree.selection():
       mb.showerror('Error!', 'Please select an item from the database')
   else:
       current_item = tree.focus()
       values = tree.item(current_item)
       selection = values["values"]

       tree.delete(current_item)

       connector.execute('DELETE FROM BUS_MANAGEMENT WHERE  SERVICE_NO=%d' % selection[0])
       connector.commit()

       mb.showinfo('Done', 'The record you wanted deleted was successfully deleted.')

       display_records()

def view_record():
   global service_no_strvar, source_strvar, type_of_bus_strvar, destination_strvar,  fare_strvar

   current_item = tree.focus()
   values = tree.item(current_item)
   selection = values["values"]

   service_no_strvar.set(selection[1]); source_strvar.set(selection[2])
   type_of_bus_strvar.set(selection[3]); destination_strvar.set(selection[4])
   fare_strvar.set(selection[5])

# Initializing the GUI window
main = Tk()
main.title('DataFlair School Management System')
main.geometry('1000x600')
main.resizable(0, 0)

# Creating the background and foreground color variables
lf_bg = 'MediumSpringGreen' # bg color for the left_frame
cf_bg = 'PaleGreen' # bg color for the center_frame

# Creating the StringVar or IntVar variables
service_no_strvar = StringVar()
source_strvar = StringVar()
type_of_bus_strvar = StringVar()
destination_strvar = StringVar()
fare_strvar = StringVar()

# Placing the components in the main window
Label(main, text="BUS MANAGEMENT SYSTEM", font=headlabelfont, bg='SpringGreen').pack(side=TOP, fill=X)

left_frame = Frame(main, bg=lf_bg)
left_frame.place(x=0, y=30, relheight=1, relwidth=0.2)

center_frame = Frame(main, bg=cf_bg)
center_frame.place(relx=0.2, y=30, relheight=1, relwidth=0.2)

right_frame = Frame(main, bg="Gray35")
right_frame.place(relx=0.4, y=30, relheight=1, relwidth=0.6)

# Placing components in the left frame
Label(left_frame, text="Service Number", font=labelfont, bg=lf_bg).place(relx=0.175, rely=0.05)
Label(left_frame, text="Source", font=labelfont, bg=lf_bg).place(relx=0.3, rely=0.18)
Label(left_frame, text="Destination", font=labelfont, bg=lf_bg).place(relx=0.275, rely=0.31)
Label(left_frame, text="Type Of Bus", font=labelfont, bg=lf_bg).place(relx=0.22, rely=0.44)
Label(left_frame, text="Fare", font=labelfont, bg=lf_bg).place(relx=0.3, rely=0.7)

Entry(left_frame, width=19, textvariable=service_no_strvar, font=entryfont).place(x=20, rely=0.1)
Entry(left_frame, width=19, textvariable=type_of_bus_strvar, font=entryfont).place(x=20, rely=0.23)
Entry(left_frame, width=19, textvariable=source_strvar, font=entryfont).place(x=20, rely=0.36)
Entry(left_frame, width=19, textvariable=fare_strvar, font=entryfont).place(x=20, rely=0.75)

OptionMenu(left_frame, destination_strvar, 'Luxury', "Ordinary").place(x=45, rely=0.49, relwidth=0.5)

Button(left_frame, text='Submit and Add Record', font=labelfont, command=add_record, width=18).place(relx=0.025, rely=0.85)

# Placing components in the center frame
Button(center_frame, text='Delete', font=labelfont, command=remove_record, width=15).place(relx=0.1, rely=0.25)
Button(center_frame, text='View', font=labelfont, command=view_record, width=15).place(relx=0.1, rely=0.35)
Button(center_frame, text='Reset', font=labelfont, command=reset_fields, width=15).place(relx=0.1, rely=0.45)
Button(center_frame, text='Delete database', font=labelfont, command=reset_form, width=15).place(relx=0.1, rely=0.55)

# Placing components in the right frame
Label(right_frame, text='Students Records', font=headlabelfont, bg='DarkGreen', fg='LightCyan').pack(side=TOP, fill=X)

tree = ttk.Treeview(right_frame, height=100, selectmode=BROWSE,
                   columns=('Service Number', "Source", "Destination", "Type of Bus", "Fare"))

X_scroller = Scrollbar(tree, orient=HORIZONTAL, command=tree.xview)
Y_scroller = Scrollbar(tree, orient=VERTICAL, command=tree.yview)

X_scroller.pack(side=BOTTOM, fill=X)
Y_scroller.pack(side=RIGHT, fill=Y)

tree.config(yscrollcommand=Y_scroller.set, xscrollcommand=X_scroller.set)

tree.heading('Service Number', text='Service Number', anchor=CENTER)
tree.heading('Source', text='Source', anchor=CENTER)
tree.heading('Destination', text='Destination', anchor=CENTER)
tree.heading('Type of Bus', text='Type of Bus', anchor=CENTER)
tree.heading('Fare', text='Fare', anchor=CENTER)

tree.column('#0', width=0, stretch=NO)
tree.column('#1', width=100, stretch=NO)
tree.column('#2', width=100, stretch=NO)
tree.column('#3', width=100, stretch=NO)
tree.column('#4', width=80, stretch=NO)

tree.place(y=30, relwidth=1, relheight=0.9, relx=0)
#if (st.button('Go')):
display_records()

    # Finalizing the GUI window
main.update()
main.mainloop()
