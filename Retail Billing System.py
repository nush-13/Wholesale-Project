import customtkinter as ctk 
import tkinter as tk 
import pymysql 
from CTkListbox import *
from CTkMessagebox import *
from tkinter import messagebox
from PIL import Image,ImageTk
import time

ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('green')
db=pymysql.connect(host='localhost',user="root",password='',database="rbs")
cursor=db.cursor()


root=ctk.CTk()
root.geometry("1280x625")
root.title("Retail Billing System")
root.resizable(False,False)


TitleFrame=ctk.CTkFrame(master=root,height=50,fg_color="#89CFF0",corner_radius=1)
TitleFrame.pack(padx=10,pady=5,fill='x')
Title=ctk.CTkLabel(master=TitleFrame,text="RETAIL BILLING SYSTEM",font=ctk.CTkFont('Microsoft YaHei UI Bold',24,'bold'),text_color="#fdfff5",height=50,width=300)
Title.pack(pady=5,expand=True,fill='x')

UserSelect=CTkListbox(master=root,height=30,width=250,hover_color="#5dbea3",highlight_color="#E0115F",font=ctk.CTkFont('Microsoft YaHei UI Bold'))
UserSelect.insert(0,"Admin")
UserSelect.insert(1,"Employee")
UserSelect.place(relx=0.4,rely=0.135)

def Login():
    Username=UsernameEntry.get()
    Password=PasswordEntry.get()
    UserType=UserSelect.get(UserSelect.curselection())
    if UserType=="Admin":
        try:
            Login_query="SELECT * FROM admin_details where A_USERNAME=%s and A_PASSWORD=%s"
            cursor.execute(Login_query,(Username,Password))
            result=cursor.fetchone()
            if result:
                CTkMessagebox(title='SUCCESS',message="LOGGED IN SUCCESFULLY",icon='check')
            else:
                CTkMessagebox(title='Error',message="Please enter valid username and password",icon='warning')
        except Exception as e:
            CTkMessagebox(title='Error',message=str(e),icon='warning')
    elif UserType=="Employee":
        try:
            Login_query="SELECT * FROM employee_details where E_USERNAME=%s and E_PASSWORD=%s"
            cursor.execute(Login_query,(Username,Password))
            result=cursor.fetchone()
            if result:
                CTkMessagebox(title='SUCCESS',message="LOGGED IN SUCCESFULLY",icon='check')
            else:
                CTkMessagebox(title='Error',message="Please enter valid username and password",icon='warning')
        except Exception as e:
            CTkMessagebox(title='Error',message=str(e),icon='warning')
    else:
        CTkMessagebox(title='Error',message="Select Valid user type",icon='warning')


LoginFrame=ctk.CTkFrame(master=root,height=400,width=400,fg_color="#89CFF0")
LoginFrame.pack(expand=True)


#function that will display time
def display_time():
    current_time=time.strftime('%H:%M:%S')
    clockLabel.configure(text=current_time)
    root.after(1000,display_time) 


clockLabel=ctk.CTkLabel(master=LoginFrame,text="",fg_color="#89CFF0",font=ctk.CTkFont('Microsoft YaHei UI Bold',45,'bold'),text_color="#fdfff5")
clockLabel.place(relx=0.245,rely=0.075)
display_time()

UsernameLabel=ctk.CTkLabel(master=LoginFrame,text="Username: ",font=ctk.CTkFont('Microsoft YaHei UI Bold',26,'bold'),text_color="#fdfff5")
UsernameLabel.place(relx=0.05,rely=0.3)
UsernameEntry=ctk.CTkEntry(master=LoginFrame,placeholder_text="Your Username: ",placeholder_text_color="#36454f",font=ctk.CTkFont('Microsoft YaHei UI Bold'),height=40,width=200,text_color="#36454f",fg_color="#ECF3F9",border_color="#36454f",border_width=3)
UsernameEntry.place(relx=0.43,rely=0.3)


PasswordLabel=ctk.CTkLabel(master=LoginFrame,text="Password: ",font=ctk.CTkFont('Microsoft YaHei UI Bold',26,'bold'),text_color="#fdfff5")
PasswordLabel.place(relx=0.05,rely=0.5)
PasswordEntry=ctk.CTkEntry(master=LoginFrame,placeholder_text="Your Password: ",placeholder_text_color="#36454f",font=ctk.CTkFont('Microsoft YaHei UI Bold'),height=40,width=200,text_color="#36454f",fg_color="#ECF3F9",border_color="#36454f",border_width=3,show="*")
PasswordEntry.place(relx=0.43,rely=0.5)

LoginButton=ctk.CTkButton(master=LoginFrame,text="LOGIN",font=ctk.CTkFont('Microsoft YaHei UI Bold',26,'bold'),fg_color='transparent',height=50,width=300,border_color='#5dbea3',border_width=3,hover_color='#5dbea3',cursor='hand2',command=Login)
LoginButton.place(relx=0.125,rely=0.7)

root.mainloop()
db.close()