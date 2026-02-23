import customtkinter as ctk 
import tkinter as tk 
from tkinter import ttk
import pymysql 
from CTkListbox import *
from CTkMessagebox import *
from CTkMenuBar import *
from tkinter import messagebox
from PIL import Image,ImageTk
import time
import datetime
import os


ctk.set_appearance_mode('light')
ctk.set_default_color_theme('blue')

# ── Pastel Colour Palette ──────────────────────────────────────
PASTEL_BG        = "#FDF6F0"  # warm cream  (main frames)
PASTEL_FRAME2    = "#F5E6DC"  # soft peach  (secondary frames)
PASTEL_ACCENT    = "#D4907E"  # dusty rose  (buttons)
PASTEL_ACCENT_HV = "#B87060"  # deep rose   (hover)
PASTEL_ENTRY     = "#FFFFFF"  # white       (entry bg)
PASTEL_ENTRY_TXT = "#7A5C58"  # warm brown  (entry text)
PASTEL_LABEL     = "#6B4F4F"  # mauve-brown (labels)
PASTEL_BORDER    = "#D4907E"  # dusty rose  (entry border)
PASTEL_MENU_BG   = "#F5E6DC"  # peach       (menubar)
PASTEL_DROP_HV   = "#E8C5BB"  # blush       (dropdown hover)
db=pymysql.connect(host='localhost',user="root",password='',database="rbs")
cursor=db.cursor()

current_date=datetime.datetime.now()
formatted_date=current_date.strftime("%Y-%m-%d")
formatted_time=current_date.strftime("%H:%M:%S")

root=ctk.CTk()
root.geometry("1280x900+50+50")
root.title("Retail Billing System")
root.resizable(False,False)


#Created a menubar
menubar=CTkMenuBar(master=root,bg_color=PASTEL_MENU_BG,padx=25)
menubar_button1=menubar.add_cascade("View")
menubar_button2=menubar.add_cascade("Delete")
menubar_button3=menubar.add_cascade("Add")

#dropdown options for each options in the menu
View_dropdown=CustomDropdownMenu(widget=menubar_button1)
View_Employees=View_dropdown.add_submenu("Employee")

def ViewRecruitedEmployees():
    ViewRecruitedEmployeesPanel=ctk.CTkToplevel(root)
    ViewRecruitedEmployeesPanel.title("View Recruited Employees")
    ViewRecruitedEmployeesPanel.geometry("800x800+200+200")
    ViewRecruitedEmployeesFrame=ctk.CTkFrame(master=ViewRecruitedEmployeesPanel,fg_color=PASTEL_BG,height=750,width=750)
    ViewRecruitedEmployeesFrame.pack(padx=10,pady=10,expand=True,fill='both')

    ViewRecruitedEmployeesTree=ttk.Treeview(master=ViewRecruitedEmployeesFrame,height=5,columns=('E_ID','E_NAME','E_USERNAME','E_PASSWORD'),show='headings')
    ViewRecruitedEmployeesTree.pack(padx=10,pady=10,fill='both',expand=True)


    ViewRecruitedEmployeesTree.heading("#1",text="ID")
    ViewRecruitedEmployeesTree.heading("#2",text="Name")
    ViewRecruitedEmployeesTree.heading("#3",text="Username")
    ViewRecruitedEmployeesTree.heading("#4",text="Password")
    
    ViewRecruitedEmployeesTree.column("#1",width=50)
    ViewRecruitedEmployeesTree.column("#2",width=75)
    ViewRecruitedEmployeesTree.column("#3",width=100)
    ViewRecruitedEmployeesTree.column("#4",width=100)
    try:
        cursor.execute("SELECT * FROM employee_details")
        db.commit()
        ViewRecruitedEmployeesResult=cursor.fetchall()
        for result in ViewRecruitedEmployeesResult:
            ViewRecruitedEmployeesTree.insert('','end',values=result)
    except Exception as e :
        CTkMessagebox(title='Error',message=str(e),icon='cancel')


View_Employees.add_option(option="View Recruited Employees",command=ViewRecruitedEmployees)
View_Employees.add_option(option="View Fired Employees")
View_Employees.add_option(option="View Resigned Employees")
View_products=View_dropdown.add_submenu("Product")
View_products.add_option(option="View Product Sales")
View_products.add_option(option="View Products Added")

Delete_dropdown=CustomDropdownMenu(widget=menubar_button2)


#function to remove the employee from the system
def RemoveEmployee():
    RemoveEmployeePanel=ctk.CTkToplevel(root)
    RemoveEmployeePanel.geometry("500x500+150+150")
    RemoveEmployeePanel.resizable(False,False)
    RemoveEmployeePanel.title("Remove Employee")

    RemoveEmployeeFrame=ctk.CTkFrame(master=RemoveEmployeePanel,fg_color=PASTEL_BG,height=450,width=450)
    RemoveEmployeeFrame.pack(padx=10,pady=10,expand=True,fill='both')

    EmployeeIDLabel=ctk.CTkLabel(master=RemoveEmployeeFrame,text="Employee ID: ",font=ctk.CTkFont('Microsoft YaHei UI Bold',20),text_color=PASTEL_LABEL)
    EmployeeIDLabel.place(relx=0.12,rely=0.055)
    EmployeeIDEntry=ctk.CTkEntry(master=RemoveEmployeeFrame,placeholder_text="Employee ID",height=30,width=225,font=ctk.CTkFont('Microsoft YaHei UI Bold',16),placeholder_text_color=PASTEL_ENTRY_TXT,text_color=PASTEL_ENTRY_TXT,fg_color=PASTEL_ENTRY,border_color=PASTEL_BORDER,border_width=2)
    EmployeeIDEntry.place(relx=0.42,rely=0.05)

    def FetchEmployee():
        EmployeeID=EmployeeIDEntry.get()
        
        #initial conditions
        if EmployeeID=="":
            CTkMessagebox(title='Error',message='Please enter the ID of the Employee',icon='warning')
            return 
        if not(EmployeeID.isdigit()):
            CTkMessagebox(title='Error',message="Please enter a valid Employee ID",icon='warning')
            return

        
        
        #check if employee is already removed or not
        check_ID="SELECT * FROM removed_employees WHERE E_ID=%s"
        cursor.execute(check_ID,(EmployeeID,))
        removed_id_check=cursor.fetchone()
        if removed_id_check:
            CTkMessagebox(title='Error',message="The employee has been removed already",icon='warning')
            return
        
        try: 
            FetchEmployeeQuery="SELECT E_ID,E_NAME,E_USERNAME,E_PASSWORD FROM employee_details WHERE E_ID=%s"
            cursor.execute(FetchEmployeeQuery,(EmployeeID,))
            db.commit()
            result=cursor.fetchone()
            
            if result:
                FetchEmployeeTree=ttk.Treeview(master=RemoveEmployeeFrame,height=1,columns=('E_ID','E_NAME','E_USERNAME','E_PASSWORD'),show='headings')
                FetchEmployeeTree.place(relx=0.05,rely=0.25)

                
                FetchEmployeeTree.heading("#1",text="E ID")
                FetchEmployeeTree.heading("#2",text="Employee Name")
                FetchEmployeeTree.heading("#3",text="Employee Username")
                FetchEmployeeTree.heading("#4",text="Employee Password")

                FetchEmployeeTree.column("#1",width=50)
                FetchEmployeeTree.column("#2",width=125)
                FetchEmployeeTree.column("#3",width=125)
                FetchEmployeeTree.column("#4",width=125)
                
                E_ID,E_NAME,E_USERNAME,E_PASSWORD=result
                FetchEmployeeTree.insert('','end',values=(E_ID,E_NAME,E_USERNAME,E_PASSWORD))

                ReasonLabel=ctk.CTkLabel(master=RemoveEmployeeFrame,text="Reason: ",font=ctk.CTkFont('Microsoft YaHei UI Bold',20),text_color=PASTEL_LABEL)
                ReasonLabel.place(relx=0.15,rely=0.45)
                ReasonComboBox=ctk.CTkComboBox(master=RemoveEmployeeFrame,text_color=PASTEL_ENTRY_TXT,fg_color=PASTEL_ENTRY,hover=True,dropdown_hover_color=PASTEL_DROP_HV,button_hover_color=PASTEL_ACCENT_HV,button_color=PASTEL_ACCENT,dropdown_fg_color=PASTEL_ENTRY,dropdown_font=ctk.CTkFont('Microsoft YaHei UI Bold',16),height=40,width=175,values=["Resigned","Fired"],font=ctk.CTkFont('Microsoft YaHei UI Bold',16))
                ReasonComboBox.place(relx=0.35,rely=0.44)
                ReasonComboBox.set("Resigned")

                def FinalRemoveEmployee():
                    Reason=ReasonComboBox.get()
                    Remove_employee_query="DELETE FROM employee_details WHERE E_ID=%s"
                    try:
                        cursor.execute(Remove_employee_query,(EmployeeID,))
                        db.commit()
                        if cursor.rowcount>0:
                            CTkMessagebox(title='SUCCESS',message="Employee Removed Succesfully",icon='check')
                            record_removed_employee_entry="INSERT INTO removed_employees(E_ID,E_NAME,Reason,DateFired,TimeFired) VALUES(%s,%s,%s,%s,%s)"
                            try:
                                cursor.execute(record_removed_employee_entry,(EmployeeID,E_NAME,Reason,formatted_date,formatted_time))
                                db.commit()
                                record_result=cursor.rowcount()
                                if record_result:
                                    CTkMessagebox(title='Success',message="Record for removed employee stored succesfully",icon='check')
                                    return
                                else:
                                    CTkMessagebox(title='Error',message="There was an error storing the record",icon='cancel')
                                    return
                            except Exception as e:
                                CTkMessagebox(title='error',message=str(e),icon='cancel')
                        else:
                            CTkMessagebox(title='Error',message="There was an error",icon='cancel')
                            return
                    except Exception as e:
                        CTkMessagebox(title='Error',message=str(e),icon='cancel')
                        


                RemoveEmployeeButton=ctk.CTkButton(master=RemoveEmployeeFrame,text='Remove Employee',font=ctk.CTkFont('Microsoft YaHei UI Bold',20),fg_color=PASTEL_ACCENT,hover_color=PASTEL_ACCENT_HV,text_color='white',cursor='hand2',width=200,height=38,command=FinalRemoveEmployee)
                RemoveEmployeeButton.place(relx=0.23,rely=0.65)


            else:
                CTkMessagebox(title='Error',message="The ID of the employee does not exist",icon='warning')
                return

        except Exception as e:
            CTkMessagebox(title='Error',message=str(e),icon='warning')
            RemoveEmployeePanel.withdraw()
            root.deiconify()

        

    ViewEmployeeButton=ctk.CTkButton(master=RemoveEmployeeFrame,text='View Employee',font=ctk.CTkFont('Microsoft YaHei UI Bold',20),fg_color=PASTEL_ACCENT,hover_color=PASTEL_ACCENT_HV,text_color='white',cursor='hand2',width=200,height=38,command=FetchEmployee)
    ViewEmployeeButton.place(relx=0.28,rely=0.15)




Delete_dropdown.add_option(option="Remove Employee",command=RemoveEmployee)
Delete_dropdown.add_option(option="Remove Supplier")
Delete_dropdown.add_option(option="Delete Bill")

Add_dropdown=CustomDropdownMenu(widget=menubar_button3)

#function to add Employeed
def AddEmployee():
    AddEmployeePanel=ctk.CTkToplevel(root)
    AddEmployeePanel.geometry("400x400+150+150")
    AddEmployeePanel.title("Add Employee")
    AddEmployeePanel.resizable(False,False)

    AddEmployeeFrame=ctk.CTkFrame(master=AddEmployeePanel,fg_color=PASTEL_BG,height=350,width=350)
    AddEmployeeFrame.pack(padx=5,pady=5,expand=True,fill='both')

    EmployeeNameLabel=ctk.CTkLabel(master=AddEmployeeFrame,text="Employee Name: ",font=ctk.CTkFont('Microsoft YaHei UI Bold',16),text_color=PASTEL_LABEL)
    EmployeeNameLabel.place(relx=0.01,rely=0.05)
    EmployeeNameEntry=ctk.CTkEntry(master=AddEmployeeFrame,placeholder_text="Employee Name",height=30,width=225,font=ctk.CTkFont('Microsoft YaHei UI Bold',15),placeholder_text_color=PASTEL_ENTRY_TXT,text_color=PASTEL_ENTRY_TXT,fg_color=PASTEL_ENTRY,border_color=PASTEL_BORDER,border_width=2)
    EmployeeNameEntry.place(relx=0.41,rely=0.05)



    EmployeeUsernameLabel=ctk.CTkLabel(master=AddEmployeeFrame,text="Username: ",font=ctk.CTkFont('Microsoft YaHei UI Bold',16),text_color=PASTEL_LABEL)
    EmployeeUsernameLabel.place(relx=0.01,rely=0.35)
    EmployeeUsernameEntry=ctk.CTkEntry(master=AddEmployeeFrame,placeholder_text="Employee Username",height=30,width=225,font=ctk.CTkFont('Microsoft YaHei UI Bold',15),placeholder_text_color=PASTEL_ENTRY_TXT,text_color=PASTEL_ENTRY_TXT,fg_color=PASTEL_ENTRY,border_color=PASTEL_BORDER,border_width=2)
    EmployeeUsernameEntry.place(relx=0.41,rely=0.35)


    EmployeePasswordLabel=ctk.CTkLabel(master=AddEmployeeFrame,text="Password: ",font=ctk.CTkFont('Microsoft YaHei UI Bold',16),text_color=PASTEL_LABEL)
    EmployeePasswordLabel.place(relx=0.01,rely=0.65)
    EmployeePasswordEntry=ctk.CTkEntry(master=AddEmployeeFrame,placeholder_text="Employee Password",height=30,width=225,font=ctk.CTkFont('Microsoft YaHei UI Bold',15),placeholder_text_color=PASTEL_ENTRY_TXT,text_color=PASTEL_ENTRY_TXT,fg_color=PASTEL_ENTRY,border_color=PASTEL_BORDER,border_width=2)
    EmployeePasswordEntry.place(relx=0.41,rely=0.65)


    def AddEmployeeFinal():
        EmployeeName=EmployeeNameEntry.get()
        EmployeeUsername=EmployeeUsernameEntry.get()
        EmployeePassword=EmployeePasswordEntry.get()

        if not(EmployeeName or EmployeePassword or EmployeeUsername):
            CTkMessagebox(title='Error',message="Please enter the details",icon='warning')
            return
        

        if EmployeeUsername==EmployeePassword:
            CTkMessagebox(title='Error',message="Employee Password and Username cannot be the same",icon='warning')
            return
        
        try:
            Add_employee_query="INSERT INTO employee_details(E_NAME,E_USERNAME,E_PASSWORD,DateAdded,TimeAdded) VALUES(%s,%s,%s,%s,%s)"
            cursor.execute(Add_employee_query,(EmployeeName,EmployeeUsername,EmployeePassword,formatted_date,formatted_time))
            db.commit()
            CTkMessagebox(title='Success',message="Employee Hired",icon='check')
            AddEmployeePanel.withdraw()
            root.deiconify()
        except Exception as e:
            CTkMessagebox(title='Error',message=str(e),icon='warning')
            AddEmployeePanel.withdraw()
            root.deiconify()


    AddEmployeeButton=ctk.CTkButton(master=AddEmployeeFrame,text='Add Employee',font=ctk.CTkFont('Microsoft YaHei UI Bold',20),fg_color=PASTEL_ACCENT,hover_color=PASTEL_ACCENT_HV,text_color='white',cursor='hand2',width=200,height=38,command=AddEmployeeFinal)
    AddEmployeeButton.place(relx=0.25,rely=0.85)




Add_dropdown.add_option(option="Add Employee",command=AddEmployee)



#function to Add Supplier
def AddSupplier():
    AddSupplierPanel=ctk.CTkToplevel(root)
    AddSupplierPanel.geometry("400x300+150+150")
    AddSupplierPanel.resizable(False,False)
    AddSupplierPanel.title("Add Supplier Panel")
    


    AddSupplierFrame=ctk.CTkFrame(master=AddSupplierPanel,fg_color=PASTEL_BG,width=250,height=250)
    AddSupplierFrame.pack(padx=5,pady=5,fill='both',expand=True)


    SupplierNameLabel=ctk.CTkLabel(master=AddSupplierFrame,text="Supplier Name: ",font=ctk.CTkFont('Microsoft YaHei UI Bold',16),text_color=PASTEL_LABEL)
    SupplierNameLabel.place(relx=0.01,rely=0.15)
    SupplierNameEntry=ctk.CTkEntry(master=AddSupplierFrame,placeholder_text="Supplier Name",height=30,width=225,font=ctk.CTkFont('Microsoft YaHei UI Bold',15),placeholder_text_color=PASTEL_ENTRY_TXT,text_color=PASTEL_ENTRY_TXT,fg_color=PASTEL_ENTRY,border_color=PASTEL_BORDER,border_width=2)
    SupplierNameEntry.place(relx=0.41,rely=0.15)


    def AddSupplierFinal():
        SupplierName=SupplierNameEntry.get()

        if SupplierName=="":
            CTkMessagebox(title='Error',message="Please Enter the supplier name",icon='warning')
            return
        
        try:
            Add_supplier_query="INSERT INTO supplierdetails(SupplierName,DateAdded,TimeAdded) VALUES(%s,%s,%s)"
            cursor.execute(Add_supplier_query,(SupplierName,formatted_date,formatted_time))
            if cursor.rowcount>0:
                CTkMessagebox(title='Success',message="Supplier Listed Succesfully",icon='check')
                AddSupplierPanel.withdraw()
                root.deiconify()
            else:
                CTkMessagebox(title='Error',message="There was an error",icon='cancel')
        except pymysql.IntegrityError as e:
            if e.args[0]==1062: #mysql error for duplicate entry
                CTkMessagebox(title='Error',message="Supplier Already Exists",icon='warning')
                return
        except Exception as e:
            CTkMessagebox(title='Error',message=str(e),icon='warning')

            

    AddSupplierButton=ctk.CTkButton(master=AddSupplierFrame,text='Add Supplier',font=ctk.CTkFont('Microsoft YaHei UI Bold',20),fg_color=PASTEL_ACCENT,hover_color=PASTEL_ACCENT_HV,text_color='white',cursor='hand2',width=200,height=38,command=AddSupplierFinal)
    AddSupplierButton.place(relx=0.25,rely=0.55)




Add_dropdown.add_option(option="Add Supplier",command=AddSupplier)






View_dropdown.configure(fg_color=PASTEL_MENU_BG,hover_color=PASTEL_DROP_HV,font=ctk.CTkFont('Microsoft YaHei UI Bold',15))
View_Employees.configure(fg_color=PASTEL_MENU_BG,hover_color=PASTEL_DROP_HV,font=ctk.CTkFont('Microsoft YaHei UI Bold',15))
View_products.configure(fg_color=PASTEL_MENU_BG,hover_color=PASTEL_DROP_HV,font=ctk.CTkFont('Microsoft YaHei UI Bold',15))
Delete_dropdown.configure(fg_color=PASTEL_MENU_BG,hover_color=PASTEL_DROP_HV,font=ctk.CTkFont('Microsoft YaHei UI Bold',15))
Add_dropdown.configure(fg_color=PASTEL_MENU_BG,hover_color=PASTEL_DROP_HV,font=ctk.CTkFont('Microsoft YaHei UI Bold',15))




WelcomeFrame=ctk.CTkFrame(master=root,height=75,fg_color=PASTEL_FRAME2)
WelcomeFrame.pack(pady=10,fill='x')
WelcomeLabel=ctk.CTkLabel(master=WelcomeFrame,text="🛒  Retail Billing System",font=ctk.CTkFont('Microsoft YaHei UI Bold',28),text_color=PASTEL_LABEL)
WelcomeLabel.pack(expand=True)

#Another frame to select between Add Product or sell it
OptionsFrame=ctk.CTkFrame(master=root,height=60,fg_color=PASTEL_FRAME2,corner_radius=8)
OptionsFrame.pack(pady=5,padx=15,fill='x')

DataManipulationFrame=ctk.CTkFrame(master=root,height=800,fg_color=PASTEL_BG,corner_radius=10)
DataManipulationFrame.pack(pady=10,padx=15,fill='both')


#function that will save the current bill number to a file
def save_bill_number(bill_number):
    with open("bill_number.txt","w") as file:
        file.write(str(bill_number))


#Function to retrieve the last saved bill number
def get_last_bill_number():
    if os.path.exists("bill_number.txt"):
        with open("bill_number.txt","r") as file:
            return int(file.read())
    else:
        return 0 #default bill number if file doesn't exist

#update the global bill number when the application starts
global_bill_number=get_last_bill_number()

#function that will toggle the content of frames upon pressing of button
def toggle_content():
    if AddProductButton.winfo_ismapped():
        AddProductButton.pack_forget()
        AddProduct()
    elif DeleteProductButton.winfo_ismapped():
        DeleteProductButton.pack_forget()
        DeleteProduct()
    elif BillingAreaButton.winfo_ismapped():
        BillingAreaButton.pack_forget()
        BillingArea()


def clear_display_frame():
    for widget in DataManipulationFrame.winfo_children():
        widget.destroy()


def AddProduct():
    clear_display_frame()
    ProductNameLabel=ctk.CTkLabel(master=DataManipulationFrame,text="Product Name: ",font=ctk.CTkFont('Microsoft YaHei UI Bold',26),text_color=PASTEL_LABEL)
    ProductNameLabel.place(relx=0.25,rely=0.075)
    ProductNameEntry=ctk.CTkEntry(master=DataManipulationFrame,placeholder_text="Product Name",width=300,height=45,font=ctk.CTkFont('Microsoft YaHei UI Bold',20),placeholder_text_color=PASTEL_ENTRY_TXT,text_color=PASTEL_ENTRY_TXT,fg_color=PASTEL_ENTRY,border_color=PASTEL_BORDER,border_width=2)
    ProductNameEntry.place(relx=0.45,rely=0.075)

    QuantityLabel=ctk.CTkLabel(master=DataManipulationFrame,text="Quantity: ",font=ctk.CTkFont('Microsoft YaHei UI Bold',26),text_color=PASTEL_LABEL)
    QuantityLabel.place(relx=0.32,rely=0.175)
    QuantityEntry=ctk.CTkEntry(master=DataManipulationFrame,placeholder_text="Quantity",width=300,height=45,font=ctk.CTkFont('Microsoft YaHei UI Bold',20),placeholder_text_color=PASTEL_ENTRY_TXT,text_color=PASTEL_ENTRY_TXT,fg_color=PASTEL_ENTRY,border_color=PASTEL_BORDER,border_width=2)
    QuantityEntry.place(relx=0.45,rely=0.175)

    PurchaseRateLabel=ctk.CTkLabel(master=DataManipulationFrame,text="Purchase Rate: ",font=ctk.CTkFont('Microsoft YaHei UI Bold',26),text_color=PASTEL_LABEL)
    PurchaseRateLabel.place(relx=0.25,rely=0.275)
    PurchaseRateEntry=ctk.CTkEntry(master=DataManipulationFrame,placeholder_text="Purchase Rate",width=300,height=45,font=ctk.CTkFont('Microsoft YaHei UI Bold',20),placeholder_text_color=PASTEL_ENTRY_TXT,text_color=PASTEL_ENTRY_TXT,fg_color=PASTEL_ENTRY,border_color=PASTEL_BORDER,border_width=2)
    PurchaseRateEntry.place(relx=0.45,rely=0.275)
    
    SalesRateLabel=ctk.CTkLabel(master=DataManipulationFrame,text="Sales Rate: ",font=ctk.CTkFont('Microsoft YaHei UI Bold',26),text_color=PASTEL_LABEL)
    SalesRateLabel.place(relx=0.3,rely=0.375)
    SalesRateEntry=ctk.CTkEntry(master=DataManipulationFrame,placeholder_text="Sales Rate",width=300,height=45,font=ctk.CTkFont('Microsoft YaHei UI Bold',20),placeholder_text_color=PASTEL_ENTRY_TXT,text_color=PASTEL_ENTRY_TXT,fg_color=PASTEL_ENTRY,border_color=PASTEL_BORDER,border_width=2)
    SalesRateEntry.place(relx=0.45,rely=0.375)

    SupplierNameLabel=ctk.CTkLabel(master=DataManipulationFrame,text="Supplier Name: ",font=ctk.CTkFont('Microsoft YaHei UI Bold',26),text_color=PASTEL_LABEL)
    SupplierNameLabel.place(relx=0.23,rely=0.475)
    SupplierNameListBox=CTkListbox(master=DataManipulationFrame,text_color=PASTEL_ENTRY_TXT,fg_color=PASTEL_ENTRY,height=35,width=275,hover_color=PASTEL_DROP_HV,highlight_color=PASTEL_ACCENT,font=ctk.CTkFont('Microsoft YaHei UI Bold',20))
    SupplierNameListBox.place(relx=0.45,rely=0.475)
    
    #Code to select supplier from supplier details
    SupplierSelect="SELECT SupplierName from supplierdetails"
    cursor.execute(SupplierSelect)
    suppliers=cursor.fetchall()
    for supplier in suppliers:
        SupplierNameListBox.insert('end',supplier[0])
    

    def AddProduct2():
        ProductName=ProductNameEntry.get()
        Quantity=QuantityEntry.get()
        PurchaseRate=PurchaseRateEntry.get()
        SalesRate=SalesRateEntry.get()

        if ProductName=="" or PurchaseRate=="" or SalesRate=="":
            CTkMessagebox(title="Error",message="Please fill up the empty fields",icon="warning")
            return
        if not(PurchaseRate.isdigit() or SalesRate.isdigit()):
            CTkMessagebox(title="Error",message="Please enter valid rate",icon="warning")
            return
        if not(Quantity.isdigit()):
            CTkMessagebox(title="Error",message="Please enter valid quantity",icon="warning")
            return
        if SupplierNameListBox=="":
            CTkMessagebox(title="Error",message="Please Select Valid Supplier",icon="warning")
            return
        
        try:
            PurchaseRate=float(PurchaseRate)
            SalesRate=float(SalesRate)
            Quantity=int(Quantity)
            Profit=SalesRate-PurchaseRate

            # Get selected supplier name and corresponding ID
            selected_supplier_name=SupplierNameListBox.get(SupplierNameListBox.curselection())
            select_supplier_name="SELECT SupplierID FROM supplierdetails WHERE SupplierName=%s"
            cursor.execute(select_supplier_name,(selected_supplier_name,))
            supplier_id=cursor.fetchone()[0]




            ProductInsert="INSERT INTO productdetails(ProductName,Quantity,PurchaseRate,SalesRate,Profit,SupplierID) VALUES(%s,%s,%s,%s,%s,%s)"
            cursor.execute(ProductInsert,(ProductName,Quantity,PurchaseRate,SalesRate,Profit,supplier_id))
            db.commit()
            CTkMessagebox(title="Success",message="Product Added Succesfully",icon='check')
        except Exception as e:
            CTkMessagebox(title="Error",message=str(e),icon='warning')

    AddProductButton2=ctk.CTkButton(master=DataManipulationFrame,text="ADD PRODUCT",font=ctk.CTkFont('Microsoft YaHei UI Bold',26),fg_color=PASTEL_ACCENT,hover_color=PASTEL_ACCENT_HV,text_color='white',height=50,width=400,command=AddProduct2)
    AddProductButton2.place(relx=0.32,rely=0.575)

AddProductButton=ctk.CTkButton(master=OptionsFrame,text='Add Product',font=ctk.CTkFont('Microsoft YaHei UI Bold',20),fg_color=PASTEL_ACCENT,hover_color=PASTEL_ACCENT_HV,text_color='white',cursor='hand2',width=200,height=38,command=AddProduct)
AddProductButton.pack(side='left',padx=10,pady=8,expand=True)

#function that will delete the product from the inventory
def DeleteProduct():
    clear_display_frame()
    ProductIDLabel=ctk.CTkLabel(master=DataManipulationFrame,text="Product ID: ",font=ctk.CTkFont('Microsoft YaHei UI Bold',26),text_color=PASTEL_LABEL)
    ProductIDLabel.place(relx=0.3,rely=0.075)
    ProductIDEntry=ctk.CTkEntry(master=DataManipulationFrame,placeholder_text="Product ID",width=300,height=45,font=ctk.CTkFont('Microsoft YaHei UI Bold',20),placeholder_text_color=PASTEL_ENTRY_TXT,text_color=PASTEL_ENTRY_TXT,fg_color=PASTEL_ENTRY,border_color=PASTEL_BORDER,border_width=2)
    ProductIDEntry.place(relx=0.45,rely=0.075)



    def DeleteProduct2():
        ProductID=ProductIDEntry.get()

        if ProductID=="":
            CTkMessagebox(title='Error',message='Please enter the ID of product you want to delete',icon='cancel')
            return
        if not (ProductID.isdigit()):
            CTkMessagebox(title='Error',message="Please enter a valid product ID",icon='cancel')
            return
        
        display_product_before_delete="SELECT * FROM productdetails WHERE ProductID=%s"
        ProductTree=ttk.Treeview(master=DataManipulationFrame,height=1,columns=('ProductID','ProductName','Quantity','PurchaseRate','SalesRate','Profit','SupplierID'),show='headings')
        ProductTree.place(relx=0.2,rely=0.275)

        ProductTree.heading("#1",text="Product ID")
        ProductTree.heading("#2",text="Product Name")
        ProductTree.heading("#3",text="Quantity")
        ProductTree.heading("#4",text="Purchase Rate")
        ProductTree.heading("#5",text="Sales Rate")
        ProductTree.heading("#6",text="Profit")
        ProductTree.heading("#7",text="Supplier ID")

        ProductTree.column("#1",width=100)
        ProductTree.column("#2",width=100)
        ProductTree.column("#3",width=100)
        ProductTree.column("#4",width=100)
        ProductTree.column("#5",width=100)
        ProductTree.column("#6",width=100)
        ProductTree.column("#7",width=100)

        try:
            cursor.execute(display_product_before_delete,(ProductID,))
            db.commit()
            result=cursor.fetchall()
            for row in result:
                ProductTree.insert('','end',values=row)
        except Exception as e:
            db.rollback()
            return


        confirmation=CTkMessagebox(title="Confirmation!!",message="Are you sure you want to remove the product",icon="warning",option_1='Yes',option_2='No')
        if confirmation.get()=="No":
            return
        else:
            try:
                DeleteProductQuery="DELETE FROM productdetails WHERE ProductID=%s"
                cursor.execute(DeleteProductQuery,(ProductID,))
                db.commit()
                CTkMessagebox(title='Success',message="PRODUCT DELETED FROM THE INVENTORY",icon='check')
            except Exception as e:
                CTkMessagebox(title='Error',message=str(e),icon='warning')
                db.rollback()
            
    DeleteProductButton2=ctk.CTkButton(master=DataManipulationFrame,text="DELETE PRODUCT",font=ctk.CTkFont('Microsoft YaHei UI Bold',26),fg_color=PASTEL_ACCENT,hover_color=PASTEL_ACCENT_HV,text_color='white',height=50,width=400,command=DeleteProduct2)
    DeleteProductButton2.place(relx=0.32,rely=0.175)

DeleteProductButton=ctk.CTkButton(master=OptionsFrame,text='Delete Product',font=ctk.CTkFont('Microsoft YaHei UI Bold',20),fg_color=PASTEL_ACCENT,hover_color=PASTEL_ACCENT_HV,text_color='white',cursor='hand2',width=200,height=38,command=DeleteProduct)
DeleteProductButton.pack(side='left',padx=10,pady=8,expand=True)


#Function that will show the billing area of the program 

def BillingArea():
    clear_display_frame()
    SearchBillFrame=ctk.CTkFrame(master=DataManipulationFrame,fg_color=PASTEL_FRAME2,height=60,width=1280)
    SearchBillFrame.place(relx=0,rely=0.02)

    BillNoSearchLabel=ctk.CTkLabel(master=SearchBillFrame,text="Bill Number: ",text_color=PASTEL_LABEL,font=ctk.CTkFont('Microsoft YaHei UI Bold',26))
    BillNoSearchLabel.place(relx=0.35,rely=0.15)
    BillNoSearchEntry=ctk.CTkEntry(master=SearchBillFrame,placeholder_text="Bill No",height=40,width=250,font=ctk.CTkFont('Microsoft YaHei UI Bold',18),text_color=PASTEL_ENTRY_TXT,placeholder_text_color=PASTEL_ENTRY_TXT,fg_color=PASTEL_ENTRY,border_color=PASTEL_BORDER,border_width=2)
    BillNoSearchEntry.place(relx=0.5,rely=0.15)

    #function that will display the registered bill
    def display_bill():
        BillNo=BillNoSearchEntry.get()
        if BillNo=="":
            CTkMessagebox(title="Error",message="Please enter the bill number",icon='warning')
            return

        if not (BillNo.isdigit()):
            CTkMessagebox(title='Error',message="Please enter a valid bill number",icon='warning')
            return

        displayBillPanel=ctk.CTkToplevel(root)
        root.withdraw()
        displayBillPanel.geometry("800x800+150+150")
        displayBillPanel.title("View Bill")

        displayBillMainFrame=ctk.CTkFrame(master=displayBillPanel,fg_color=PASTEL_BG,height=750,width=750)
        displayBillMainFrame.pack(padx=10,pady=10,expand=True)
        
        displayBilltextarea=ctk.CTkTextbox(master=displayBillMainFrame,height=500,width=500,scrollbar_button_color=PASTEL_ACCENT,scrollbar_button_hover_color=PASTEL_ACCENT_HV,font=ctk.CTkFont('Microsoft YaHei UI Bold',14),text_color=PASTEL_LABEL)
        displayBilltextarea.place(relx=0.17,rely=0.1)

        try:
            cursor.execute("SELECT CustomerName,CustomerNumber,DateOfPurchase,TotalAmount,PaymentMethod FROM bill where BillID=%s",(BillNo,))
            db.commit()
            result=cursor.fetchone()
            if result:
                CustomerName, CustomerNumber, DateOfPurchase, TotalAmount, PaymentMethod=result
                displayBilltextarea.insert('end','\t\t       WELCOME CUSTOMER')
                displayBilltextarea.insert('end',f'\n\nBill No: {BillNo}')
                displayBilltextarea.insert('end',f'\nCustomer Name: {CustomerName}')
                displayBilltextarea.insert('end',f'\nCustomer Number: {CustomerNumber}')
                displayBilltextarea.insert('end',f'\nDate of Purchase: {DateOfPurchase}')
                displayBilltextarea.insert('end',f'\nPayment Method: {PaymentMethod}')
                displayBilltextarea.insert('end','\n===========================================')
                displayBilltextarea.insert('end','\nPRODUCTS\t\t\t QTY \t\t\tPrice')
                displayBilltextarea.insert('end','\n===========================================')

                #fetch products for the given bill
                cursor.execute("SELECT product_name,quantity,total_product_amount FROM bill_products WHERE bill_id=%s",(BillNo,))
                products=cursor.fetchall()
                for product in products:
                    product_name,quantity,total_product_amount=product
                    displayBilltextarea.insert('end',f'\n{product_name}\t\t\t  {quantity} \t\t              {total_product_amount}')
                displayBilltextarea.insert('end','\n===========================================')
                
                displayBilltextarea.insert('end', "\n\t\t\t\t\t            ======")
                displayBilltextarea.insert('end', f"\n\t\t\t\tTotal Amount:       {TotalAmount}")
                displayBilltextarea.insert('end', "\n\t\t\t\t\t            ======")
                displayBilltextarea.insert('end','\n-------------------------------------------------------------------------------')
                displayBilltextarea.insert('end','\n-------------------------------------------------------------------------------')
                displayBilltextarea.insert('end','\n-------------------------------------------------------------------------------')
                displayBilltextarea.insert('end','\t\t\t       IMPORTANT NOTE')
                displayBilltextarea.insert('end','\n1. Goods once purchased cannot be returned')   
                displayBilltextarea.insert('end','\n2. You can only exchange goods within 15 days of purchase.')  
                displayBilltextarea.insert('end',"\n3. If you modify the product, we won't exchange it.")
                displayBilltextarea.insert('end',"\n5. To exchange a product, please bring the receipt with you.")   
                displayBilltextarea.insert('end',"\n4. Prices are as steady as your grandma's knitting needles! So don't bargain")    
                displayBilltextarea.insert('end','\n-------------------------------------------------------------------------------')
                displayBilltextarea.insert('end','\n\t      THANK YOU FOR SHOPPING WITH US')
                displayBilltextarea.insert('end',"\n\t     Hope your day is as bright as your smile.")
            
            
            else:
                CTkMessagebox(title='Error',message="Bill Number not found",icon='warning')
                root.deiconify()
                displayBillPanel.destroy()
        except Exception as e:
            CTkMessagebox(title='Error',message=str(e),icon='cancel')
            root.deiconify()
            displayBillPanel.destroy()

        def goBackSearchBill():
            root.deiconify()
            displayBillPanel.destroy()


        goBackButton=ctk.CTkButton(master=displayBillMainFrame,text="Go Back",height=35,width=150,font=ctk.CTkFont('Microsoft YaHei UI Bold',14),fg_color=PASTEL_ACCENT,hover_color=PASTEL_ACCENT_HV,text_color='white',cursor='hand2',command=goBackSearchBill)
        goBackButton.place(relx=0.05,rely=0.9)

        def printBill():
            printmsg=CTkMessagebox(title='Confirmation',message="Are you sure you want to print the bill?",option_1='Yes',option_2='No',icon='question')

            if printmsg.get()=='Yes':
                CTkMessagebox(message="Printing Bill")
            else:
                return

        printBillButton=ctk.CTkButton(master=displayBillMainFrame,text="Print Bill",height=35,width=150,font=ctk.CTkFont('Microsoft YaHei UI Bold',14),fg_color=PASTEL_ACCENT,hover_color=PASTEL_ACCENT_HV,text_color='white',cursor='hand2',command=printBill)
        printBillButton.place(relx=0.75,rely=0.9)



        displayBillPanel.mainloop()




    SearchBillButton=ctk.CTkButton(master=DataManipulationFrame,text="Search Bill",height=42,width=280,font=ctk.CTkFont('Microsoft YaHei UI Bold',24),fg_color=PASTEL_ACCENT,hover_color=PASTEL_ACCENT_HV,text_color='white',cursor='hand2',command=display_bill)
    SearchBillButton.place(relx=0.4,rely=0.12)



    
    #Frame where the main bill will be generated
    MainBillAreaFrame=ctk.CTkFrame(master=DataManipulationFrame,fg_color=PASTEL_FRAME2,height=500,width=500,corner_radius=8)
    MainBillAreaFrame.place(relx=0,rely=0.2)

    ProductIDLabel=ctk.CTkLabel(master=MainBillAreaFrame,text="Product ID: ",text_color=PASTEL_LABEL,font=ctk.CTkFont('Microsoft YaHei UI Bold',26))
    ProductIDLabel.place(relx=0.05,rely=0.1)
    ProductIDEntry=ctk.CTkEntry(master=MainBillAreaFrame,placeholder_text="Product ID",height=42,width=280,font=ctk.CTkFont('Microsoft YaHei UI Bold',18),text_color=PASTEL_ENTRY_TXT,placeholder_text_color=PASTEL_ENTRY_TXT,fg_color=PASTEL_ENTRY,border_color=PASTEL_BORDER,border_width=2)
    ProductIDEntry.place(relx=0.4,rely=0.1)
    
    
    QuantityLabel=ctk.CTkLabel(master=MainBillAreaFrame,text="Quantity: ",text_color=PASTEL_LABEL,font=ctk.CTkFont('Microsoft YaHei UI Bold',26))
    QuantityLabel.place(relx=0.05,rely=0.3)
    QuantityEntry=ctk.CTkEntry(master=MainBillAreaFrame,placeholder_text="Quantity",height=42,width=280,font=ctk.CTkFont('Microsoft YaHei UI Bold',18),text_color=PASTEL_ENTRY_TXT,placeholder_text_color=PASTEL_ENTRY_TXT,fg_color=PASTEL_ENTRY,border_color=PASTEL_BORDER,border_width=2)
    QuantityEntry.place(relx=0.4,rely=0.3)

    #Defining dictionary to store initial quantities fetched from database
    initial_quantities = {}
    #function that will display The items added when bill is generated
    def AddedItems():
        ProductID=ProductIDEntry.get()
        Quantity=QuantityEntry.get()

        if ProductID=="" or Quantity=="":
            CTkMessagebox(title="Error",message="Please fill up the details",icon="cancel")
            return
        if not(ProductID.isdigit() or Quantity.isdigit()):
            CTkMessagebox(title='Error',message="Please Enter valid values",icon='cancel')
            return 

        try:
            cursor.execute("SELECT * FROM productdetails WHERE ProductID=%s",(ProductID,))
            db.commit()
            result=cursor.fetchone()
            if result:

                #fetch initial quantities
                initial_quantities=result[2]

                #check if entered quantity exceeds available quantity
                if int(Quantity)>initial_quantities:
                    CTkMessagebox(title='Error',message="Quantity Entered Exceeds Available Quantity",icon='warning')
                    return
                AddProductTree.insert('', 'end', values=(result[0], result[1], result[2], result[3], result[4], result[5], result[6], Quantity))
            else:
                CTkMessagebox(title='Error',message="Product ID not found",icon='warning')
        except Exception as e:
            db.rollback()
            return
        ProductIDEntry.delete(0, 'end')
        QuantityEntry.delete(0, 'end')
    AddProductTree=ttk.Treeview(master=DataManipulationFrame,columns=('ProductID','ProductName','Quantity','PurchaseRate','SalesRate','Profit','SupplierID','Quantity Required'),show='headings')
    AddProductTree.place(relx=0.39,rely=0.2)
        
    AddProductTree.heading("#1",text="Product ID")
    AddProductTree.heading("#2",text="Product Name")
    AddProductTree.heading("#3",text="Quantity Available")
    AddProductTree.heading("#4",text="Purchase Rate")
    AddProductTree.heading("#5",text="Sales Rate")
    AddProductTree.heading("#6",text="Profit")
    AddProductTree.heading("#7",text="Supplier ID")
    AddProductTree.heading("#8",text="Quantity Required")

    AddProductTree.column("#1",width=100)
    AddProductTree.column("#2",width=100)
    AddProductTree.column("#3",width=100)
    AddProductTree.column("#4",width=100)
    AddProductTree.column("#5",width=100)
    AddProductTree.column("#6",width=100)
    AddProductTree.column("#7",width=100)
    AddProductTree.column("#8",width=75)

    AddMoreButton=ctk.CTkButton(master=MainBillAreaFrame,text="Add More",height=42,width=280,font=ctk.CTkFont('Microsoft YaHei UI Bold',24),fg_color=PASTEL_ACCENT,hover_color=PASTEL_ACCENT_HV,text_color='white',cursor='hand2',command=AddedItems)
    AddMoreButton.place(relx=0.2,rely=0.5)

    #Function that will delete the Item from ProductTree
    def delete_selected_item():
        selected_item=AddProductTree.selection()
        if selected_item:
            AddProductTree.delete(selected_item)
        else:
            CTkMessagebox(title='error',message='Please select an item to delete',icon='warning')

    #Button That will delete the product once selected
    DeleteSelectedProductButton=ctk.CTkButton(master=DataManipulationFrame,text="DELETE PURCHASED ITEM",height=30,width=300,font=ctk.CTkFont('Microsoft YaHei UI Bold',18),fg_color=PASTEL_ACCENT,hover_color=PASTEL_ACCENT_HV,text_color='white',cursor='hand2',command=delete_selected_item)
    DeleteSelectedProductButton.place(relx=0.58,rely=0.53)

    def goods_return():
        quantiy_to_return=QuantityEntry.get()
        product_id_to_return=ProductIDEntry.get()


        if quantiy_to_return=="" or product_id_to_return=="":
            CTkMessagebox(title='Error',message="Please fill up the details",icon='warning')
            return

        if not(quantiy_to_return.isdigit() or product_id_to_return.isdigit()):
            CTkMessagebox(title='Error',message="Please Enter valid details",icon='warning')
            return
        
        try:
            cursor.execute("SELECT * FROM productdetails WHERE ProductID=%s",(product_id_to_return,))
            db.commit()
            result=cursor.fetchone()
            if result:
                ReturnProductTree.insert('','end',values=(result[0], result[1], result[2], result[3], result[4], result[5], result[6],quantiy_to_return))
            else:
                CTkMessagebox(title='Error',message="No such Product ID",icon='cancel')
                return
        except Exception as e:
            CTkMessagebox(title='Error',message=str(e),icon='warning')
        ProductIDEntry.delete(0,'end')
        QuantityEntry.delete(0,'end')
    
    
    ReturnProductTree=ttk.Treeview(master=DataManipulationFrame,columns=('ProductID','ProductName','Quantity','PurchaseRate','SalesRate','Profit','SupplierID','Quantity Returned'),show='headings',height=5)
    ReturnProductTree.place(relx=0.39,rely=0.7)

    ReturnProductTree.heading("#1",text="Product ID")
    ReturnProductTree.heading("#2",text="Product Name")
    ReturnProductTree.heading("#3",text="Quantity Available")
    ReturnProductTree.heading("#4",text="Purchase Rate")
    ReturnProductTree.heading("#5",text="Sales Rate")
    ReturnProductTree.heading("#6",text="Profit")
    ReturnProductTree.heading("#7",text="Supplier ID")
    ReturnProductTree.heading("#8",text="Quantity to Return")
    
    ReturnProductTree.column("#1",width=100)
    ReturnProductTree.column("#2",width=100)
    ReturnProductTree.column("#3",width=100)
    ReturnProductTree.column("#4",width=100)
    ReturnProductTree.column("#5",width=100)
    ReturnProductTree.column("#6",width=100)
    ReturnProductTree.column("#7",width=100)
    ReturnProductTree.column("#8",width=75)


    ReturnGoodsLabel=ctk.CTkLabel(master=DataManipulationFrame,text="Return Goods",text_color=PASTEL_LABEL,font=ctk.CTkFont('Microsoft YaHei UI Bold',26))
    ReturnGoodsLabel.place(relx=0.61,rely=0.63)

    def delete_selected_goods_return_item():
        selected_item=ReturnProductTree.selection()
        if selected_item:
            ReturnProductTree.delete(selected_item)
        else:
            CTkMessagebox(title='error',message='Please select an item to delete',icon='warning')


    DeleteSelectedReturnGoodButton=ctk.CTkButton(master=DataManipulationFrame,text="REMOVE RETURNED ITEM",height=30,width=300,font=ctk.CTkFont('Microsoft YaHei UI Bold',18),fg_color=PASTEL_ACCENT,hover_color=PASTEL_ACCENT_HV,text_color='white',cursor='hand2',command=delete_selected_goods_return_item)
    DeleteSelectedReturnGoodButton.place(relx=0.58,rely=0.9)

    GoodsReturnButton=ctk.CTkButton(master=MainBillAreaFrame,text="GR",height=42,width=280,font=ctk.CTkFont('Microsoft YaHei UI Bold',24),fg_color=PASTEL_ACCENT,hover_color=PASTEL_ACCENT_HV,text_color='white',cursor='hand2',command=goods_return)
    GoodsReturnButton.place(relx=0.2,rely=0.7)

    #Creating a function that will generate the bill of Products added
    def GenerateBill():
        #Creation of Billing Panel
        BillPanel=ctk.CTkToplevel(root)
        BillPanel.geometry("1280x720+150+150")
        root.withdraw()

        BillFrame=ctk.CTkFrame(master=BillPanel,width=1100,height=600,fg_color=PASTEL_BG,corner_radius=8)
        BillFrame.pack(padx=10,pady=10,expand=True,fill='both')



        #creating a Tree View for displaying the Tree 
        BillTree=ttk.Treeview(master=BillFrame,columns=('ProductID','ProductName','Quantity','Price','Total Product Amount'),show='headings')
        BillTree.pack(padx=10,pady=10,fill='x')

        BillTree.heading("#1", text="Product ID")
        BillTree.heading("#2", text="Product Name")
        BillTree.heading("#3", text="Quantity")
        BillTree.heading("#4", text="Price")
        BillTree.heading("#5", text="Total Product Amount")

        BillTree.column("#1", width=100)
        BillTree.column("#2", width=200)
        BillTree.column("#3", width=100)
        BillTree.column("#4", width=100)
        BillTree.column("#5", width=100)

        total_amount=0

        
        CustomerDetailsFrame=ctk.CTkFrame(master=BillFrame,height=75,fg_color=PASTEL_FRAME2)
        CustomerDetailsFrame.pack(pady=10,padx=10,fill='x')
        
        CustomerNameLabel=ctk.CTkLabel(master=CustomerDetailsFrame,text="Customer Name: ",text_color=PASTEL_LABEL,font=ctk.CTkFont('Microsoft YaHei UI Bold',24))
        CustomerNameLabel.pack(side='left',padx=5,pady=10,expand=True)
        CustomerNameEntry=ctk.CTkEntry(master=CustomerDetailsFrame,placeholder_text="Name of Customer",height=42,width=250,font=ctk.CTkFont('Microsoft YaHei UI Bold',18),text_color=PASTEL_ENTRY_TXT,placeholder_text_color=PASTEL_ENTRY_TXT,fg_color=PASTEL_ENTRY,border_color=PASTEL_BORDER,border_width=2)
        CustomerNameEntry.pack(side='left',padx=5,pady=10,expand=True)


        CustomerNoLabel=ctk.CTkLabel(master=CustomerDetailsFrame,text="Customer Number: ",text_color=PASTEL_LABEL,font=ctk.CTkFont('Microsoft YaHei UI Bold',24))
        CustomerNoLabel.pack(side='left',padx=5,pady=10,expand=True)
        CustomerNoEntry=ctk.CTkEntry(master=CustomerDetailsFrame,placeholder_text="Customer Number",height=42,width=250,font=ctk.CTkFont('Microsoft YaHei UI Bold',18),text_color=PASTEL_ENTRY_TXT,placeholder_text_color=PASTEL_ENTRY_TXT,fg_color=PASTEL_ENTRY,border_color=PASTEL_BORDER,border_width=2)
        CustomerNoEntry.pack(side='left',padx=5,pady=10,expand=True)
        # Iterate through the items in AddProductTree and calculate total amount
        for item in AddProductTree.get_children():
            values=AddProductTree.item(item,'values')
            product_id=values[0]
            product_name=values[1]
            quantity_required=int(values[7])
            price=int(values[4])

            #calculate the total Product Amount
            total_product_amount=quantity_required*price
            total_amount+=total_product_amount


            #insert Product Details into the Bill Tree View 
            BillTree.insert('','end',values=(product_id,product_name,quantity_required,price,total_product_amount))
        

        #Iterate through the items in ReturnProductTree and calculate the total amount
        for item in ReturnProductTree.get_children():
            values=ReturnProductTree.item(item,'values')
            product_id=values[0]
            product_name=values[1]
            quantity_returned=int(values[7])
            price=int(values[4])

            #calculate the total product amount finalized
            total_product_amount=quantity_returned*price
            total_amount-=total_product_amount


            #Insert return product details into the bill tree 
            BillTree.insert('','end',values=(product_id, product_name, -quantity_returned, price, -total_product_amount))


        #displaying total amount in bill
        BillTree.insert('', 'end', values=("", "", "Total Amount:", total_amount))

        #clear the AddProductTree and ReturnProductTree so that previous data isnt maintained
        AddProductTree.delete(*AddProductTree.get_children())
        ReturnProductTree.delete(*ReturnProductTree.get_children())



        #function that will bring back the MainFrame
        def GoBack():
            msg=CTkMessagebox(title="Confirmation?",message="Are you sure you want to go back! Your bill will be removed if you choose to do so",icon='warning',option_1='Yes',option_2='No')
            if msg.get()=="Yes":
                root.deiconify()
                BillPanel.destroy()
            else:
                return

        GoBackButton=ctk.CTkButton(master=BillFrame,text="Go Back",height=42,width=280,font=ctk.CTkFont('Microsoft YaHei UI Bold',24),fg_color=PASTEL_ACCENT,hover_color=PASTEL_ACCENT_HV,text_color='white',cursor='hand2',command=GoBack)
        GoBackButton.pack(side='left',padx=10)

        #function that will generate the bill for customer
        def generateBill():
            if not CustomerNameEntry.get():
                CTkMessagebox(title='Error',message="Please enter the name of the customer",icon='warning')
                return

            billRoot=ctk.CTkToplevel(BillPanel)
            billRoot.geometry("800x800+150+150")
            billRoot.title("Final Bill")
            billRoot.resizable(False,False)
            BillPanel.withdraw()
            
            global global_bill_number
            global_bill_number+=1

            customerName=CustomerNameEntry.get()
            customerNumber=CustomerNoEntry.get()

            finalBillMainFrame=ctk.CTkFrame(master=billRoot,fg_color=PASTEL_BG,height=750,width=750)
            finalBillMainFrame.pack(padx=10,pady=10,expand=True)

            #defining the text area where the bill would be displayed
            textarea=ctk.CTkTextbox(master=finalBillMainFrame,height=500,width=500,scrollbar_button_color=PASTEL_ACCENT,scrollbar_button_hover_color=PASTEL_ACCENT_HV,font=ctk.CTkFont('Microsoft YaHei UI Bold',14),text_color=PASTEL_LABEL)
            textarea.place(relx=0.17,rely=0.1)
            


            textarea.insert('end','\t\t       WELCOME CUSTOMER')
            textarea.insert('end',f'\n\nBill No: {global_bill_number}')
            textarea.insert('end',f'\nCustomers Name: {customerName}')
            textarea.insert('end',f'\nNumber: {customerNumber}')
            textarea.insert('end',f'\nDate of Purchase: {formatted_date}')
            textarea.insert('end',f'\nTime of Purchase: {formatted_time}')
            textarea.insert('end','\n===========================================')
            textarea.insert('end','\nPRODUCTS\t\t\t QTY \t\t\tPrice')
            textarea.insert('end','\n===========================================')


            #iterate through finallized items in bill tree 
            total_price=0
            for item in BillTree.get_children():
                values=BillTree.item(item,'values')

                if len(values)==5: #makes sure there are enough elements in the tuple
                    product_id = values[0]
                    product_name = values[1]
                    quantity_required = int(values[2])
                    price = int(values[3])
                    total_product_amount = int(values[4])
                    total_price+=total_product_amount
                    
                    # Insert product details into the text area
                    textarea.insert('end', f"\n{product_name}\t\t\t {quantity_required} \t\t\t{total_product_amount}")
            textarea.insert('end', "\n\t\t\t\t\t           ======")
            textarea.insert('end', f"\n\t\t\t\tTotal Amount:          {total_price}")
            textarea.insert('end', "\n\t\t\t\t\t           ======")
            textarea.insert('end','\n-------------------------------------------------------------------------------')
            textarea.insert('end','\n-------------------------------------------------------------------------------')
            textarea.insert('end','\n-------------------------------------------------------------------------------')
            textarea.insert('end','\t\t\t       IMPORTANT NOTE')
            textarea.insert('end','\n1. Goods once purchased cannot be returned')   
            textarea.insert('end','\n2. You can only exchange goods within 15 days of purchase.')  
            textarea.insert('end',"\n3. If you modify the product, we won't exchange it.")
            textarea.insert('end',"\n5. To exchange a product, please bring the receipt with you.")   
            textarea.insert('end',"\n4. Prices are as steady as your grandma's knitting needles! So don't bargain")    
            textarea.insert('end','\n-------------------------------------------------------------------------------')
            textarea.insert('end','\n\t      THANK YOU FOR SHOPPING WITH US')
            textarea.insert('end',"\n\t     Hope your day is as bright as your smile.")
            

            PaymentMethodLabel=ctk.CTkLabel(master=finalBillMainFrame,text="Payment Method",font=ctk.CTkFont('Microsoft YaHei UI Bold',22),text_color=PASTEL_LABEL)
            PaymentMethodLabel.place(relx=0.2,rely=0.81)
            PaymentMethodListBox=CTkListbox(master=finalBillMainFrame,text_color=PASTEL_ENTRY_TXT,fg_color=PASTEL_ENTRY,height=30,width=200,hover_color=PASTEL_DROP_HV,highlight_color=PASTEL_ACCENT,font=ctk.CTkFont('Microsoft YaHei UI Bold',18))
            PaymentMethodListBox.place(relx=0.5,rely=0.8)
            #inserting default payment methods
            PaymentMethodListBox.insert(0,'Cash')
            PaymentMethodListBox.insert(1,'Card')
            PaymentMethodListBox.insert(2,'UPI')

            def back_to_root():
                msg=CTkMessagebox(title="Confirmation?",message="Are you sure you want to go back! Your bill will be removed if you choose to do so",icon='warning',option_1='Yes',option_2='No')
                if msg.get()=="Yes":
                    global global_bill_number
                    global_bill_number-=1
                    root.deiconify()
                    billRoot.destroy()
                else:
                    return

            GoBackButton1=ctk.CTkButton(master=finalBillMainFrame,text="Go Back",height=35,width=150,font=ctk.CTkFont('Microsoft YaHei UI Bold',14),fg_color=PASTEL_ACCENT,hover_color=PASTEL_ACCENT_HV,text_color='white',cursor='hand2',command=back_to_root)
            GoBackButton1.place(relx=0.05,rely=0.9)

            #function that will save the bill to the database
            def save_bill():
                global global_bill_number
                payment_method=PaymentMethodListBox.get(PaymentMethodListBox.curselection())
                save_bill_number(global_bill_number)
                try:
                    #begin a transanction
                    db.begin()
                    for item in BillTree.get_children():
                        values=BillTree.item(item,'values')
                        if len(values)==5:
                            product_id=values[0]
                            quantity_required=int(values[2]) 

                            #updating the quantity in the database
                            update_quantity_query="UPDATE productdetails SET Quantity=Quantity-%s WHERE ProductID=%s"
                            cursor.execute(update_quantity_query,(quantity_required,product_id))
                    
                    for item in ReturnProductTree.get_children():
                        values=ReturnProductTree.item(item,'values')
                        if len(values)==8:
                            product_id=values[0]
                            quantity_returned=int(values[7])


                            update_quantity_query = "UPDATE productdetails SET Quantity=Quantity+%s WHERE ProductID=%s"
                            cursor.execute(update_quantity_query, (quantity_returned, product_id))

                    bill_save_query='INSERT INTO bill(CustomerName,CustomerNumber,DateOfPurchase,TotalAmount,PaymentMethod) values(%s,%s,%s,%s,%s)'
                    cursor.execute(bill_save_query,(customerName,customerNumber,formatted_date,total_price,payment_method))
                    
                    #get the auto_generated bill ID 
                    bill_id=cursor.lastrowid
                    
                    #insert a row for each product in the bill
                    for item in BillTree.get_children():
                        values=BillTree.item(item,'values')
                        if len(values)==5:
                            product_id=values[0]
                            product_name = values[1]
                            quantity_required = int(values[2])
                            item_price = int(values[3])
                            total_product_amount = int(values[4])

                            #save the product details along with obtained bill id 
                            product_save_query="INSERT INTO bill_products(bill_id,product_id,product_name,quantity,item_price,total_product_amount) VALUES(%s,%s,%s,%s,%s,%s)"
                            cursor.execute(product_save_query,(bill_id,product_id,product_name,quantity_required,item_price,total_product_amount))

                    db.commit()
                    CTkMessagebox(title="Success",message="Bill Saved Successfully",icon='info')
                    billRoot.withdraw()
                    root.deiconify()
                except Exception as e:
                    db.rollback()
                    global_bill_number-=1
                    save_bill_number(global_bill_number)
                    billRoot.withdraw()
                    root.deiconify()
                    CTkMessagebox(title='Error',message=str(e),icon="warning")



            SaveBillButton=ctk.CTkButton(master=finalBillMainFrame,text="Save Bill",height=35,width=150,font=ctk.CTkFont('Microsoft YaHei UI Bold',14),fg_color=PASTEL_ACCENT,hover_color=PASTEL_ACCENT_HV,text_color='white',cursor='hand2',command=save_bill)
            SaveBillButton.place(relx=0.75,rely=0.9)
            billRoot.mainloop()


        FinalBillGenerate=ctk.CTkButton(master=BillFrame,text="Generate Bill",height=42,width=280,font=ctk.CTkFont('Microsoft YaHei UI Bold',24),fg_color=PASTEL_ACCENT,hover_color=PASTEL_ACCENT_HV,text_color='white',cursor='hand2',command=generateBill)
        FinalBillGenerate.pack(side='right',padx=10)



        BillPanel.mainloop()
        
    ViewBillButton=ctk.CTkButton(master=MainBillAreaFrame,text="View Bill",height=42,width=280,font=ctk.CTkFont('Microsoft YaHei UI Bold',24),fg_color=PASTEL_ACCENT,hover_color=PASTEL_ACCENT_HV,text_color='white',cursor='hand2',command=GenerateBill)
    ViewBillButton.place(relx=0.2,rely=0.9)



    
BillingAreaButton=ctk.CTkButton(master=OptionsFrame,text='Billing Area',font=ctk.CTkFont('Microsoft YaHei UI Bold',20),fg_color=PASTEL_ACCENT,hover_color=PASTEL_ACCENT_HV,text_color='white',cursor='hand2',width=200,height=38,command=BillingArea)
BillingAreaButton.pack(side='left',padx=10,pady=8,expand=True)




root.mainloop()
db.close()