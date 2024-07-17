from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import re
import mysql.connector
from mysql.connector import Error
import pyttsx3

class Register:
    def __init__(self, root):
        self.root = root
        self.root.title("Register Page")
        self.root.geometry("1350x790+0+0")
        self.root.configure(bg='white')
        
        # # text to speech
        # self.engine = pyttsx3.init(driverName='espeak')
        # self.voices = self.engine.getProperty('voices')
        # self.engine.setProperty('voice', self.voices[1].id)

        # Variables
        self.name_var = StringVar()
        self.email_var = StringVar()
        self.contact_var = StringVar()
        self.gender_var = StringVar()
        self.country_var = StringVar()
        self.id_var = StringVar()  # For ID type
        self.id_number_var = StringVar()  # For ID number
        self.password = StringVar()
        self.confirm_pass = StringVar()
        self.check_var = IntVar()

        # Background Image
        self.bg = ImageTk.PhotoImage(file="/Users/abhijeetkumar/Desktop/Registration/Bg.png")
        bg_lbl = Label(self.root, image=self.bg, bd=2, relief=RAISED)
        bg_lbl.place(x=0, y=0, relwidth=1, relheight=1)

        # Logo
        logo_img = Image.open("/Users/abhijeetkumar/Desktop/Registration/Logo.png")
        logo_img = logo_img.resize((60, 60), Image.LANCZOS)
        self.photo_logo = ImageTk.PhotoImage(logo_img)

        # Title Frame
        title_frame = Frame(self.root, bd=1, relief=RIDGE)
        title_frame.place(x=450, y=28, width=550, height=80)

        title_lbl = Label(title_frame, image=self.photo_logo, compound=LEFT, text="USER REGISTRATION FORM", font=('times new roman', 30, 'bold'), fg='darkblue')
        title_lbl.place(x=10, y=10)

        # Information Frame
        main_frame = Frame(self.root, bd=1, relief=RIDGE)
        main_frame.place(x=450, y=110, width=550, height=620)

        # Username
        user_name = Label(main_frame, text='Username', font=('times new roman', 16, 'bold'))
        user_name.grid(row=0, column=0, padx=10, pady=10, sticky=W)

        user_entry = ttk.Entry(main_frame, textvariable=self.name_var, font=('times new roman', 15, 'bold'), width=25)
        user_entry.grid(row=0, column=1, padx=10, pady=10, sticky=W)

        # Bind and validations
        validate_name = self.root.register(self.checkname)
        user_entry.config(validate='key', validatecommand=(validate_name, '%P'))

        # Email
        email_lbl = Label(main_frame, text='Email ID', font=('times new roman', 16, 'bold'))
        email_lbl.grid(row=1, column=0, padx=10, pady=10, sticky=W)

        txt_email = ttk.Entry(main_frame, textvariable=self.email_var, font=('times new roman', 15, 'bold'), width=25)
        txt_email.grid(row=1, column=1, padx=10, pady=10, sticky=W)

        # Contact Number
        contactNo = Label(main_frame, text='Contact Number', font=('times new roman', 16, 'bold'))
        contactNo.grid(row=2, column=0, padx=10, pady=10, sticky=W)

        entry_contact = ttk.Entry(main_frame, textvariable=self.contact_var, font=('times new roman', 15, 'bold'), width=25)
        entry_contact.grid(row=2, column=1, padx=10, pady=10, sticky=W)

        # Bind and validations
        validate_contact = self.root.register(self.checkcontact)
        entry_contact.config(validate='key', validatecommand=(validate_contact, '%P'))

        # Gender
        gender_lbl = Label(main_frame, text='Select Gender', font=('times new roman', 16, 'bold'))
        gender_lbl.grid(row=3, column=0, padx=10, pady=10, sticky=W)

        gender_frame = Frame(main_frame, bd=2, relief=RIDGE)
        gender_frame.place(x=200, y=160, width=280, height=35)

        radio_male = Radiobutton(gender_frame, variable=self.gender_var, value='Male', text='Male', font=('times new roman', 15))
        radio_male.grid(row=0, column=0, padx=10, pady=0, sticky=W)
        self.gender_var.set('Male')

        radio_female = Radiobutton(gender_frame, variable=self.gender_var, value='Female', text='Female', font=('times new roman', 15))
        radio_female.grid(row=0, column=1, padx=10, pady=0, sticky=W)

        # Country
        select_country = Label(main_frame, text="Select Country:", font=('times new roman', 16, 'bold'))
        select_country.grid(row=4, column=0, padx=10, pady=10, sticky=W)

        list_of_countries = ['India', 'UK', 'Nepal', 'Afghanistan', 'Pakistan']
        droplist = OptionMenu(main_frame, self.country_var, *list_of_countries)
        droplist.config(width=21, font=("times new roman", 15), bg='white')
        self.country_var.set('Select your country')
        droplist.grid(row=4, column=1, padx=10, pady=10, sticky=W)

        # ID Type
        id_type = Label(main_frame, text="Select ID Type:", font=('times new roman', 16, 'bold'))
        id_type.grid(row=5, column=0, padx=10, pady=10, sticky=W)

        self.combo_id_type = ttk.Combobox(main_frame, textvariable=self.id_var, font=('times new roman', 16), justify='center', state="readonly", width=23)
        self.combo_id_type["values"] = ("Select Your Id", "Aadhar Card", "Passport", "Driving Licence")
        self.combo_id_type.grid(row=5, column=1, padx=10, pady=10)

        # ID Number
        id_no = Label(main_frame, text="ID Number:", font=('times new roman', 16, 'bold'))
        id_no.grid(row=6, column=0, padx=10, pady=10, sticky=W)

        entry_id_no = ttk.Entry(main_frame, textvariable=self.id_number_var, font=('times new roman', 16, 'bold'), width=25)
        entry_id_no.grid(row=6, column=1, padx=10, pady=10, sticky=W)

        # Password
        s_password = Label(main_frame, text="Password:", font=('times new roman', 16, 'bold'))
        s_password.grid(row=7, column=0, padx=10, pady=10, sticky=W)

        entry_pass = ttk.Entry(main_frame, textvariable=self.password, font=('times new roman', 16, 'bold'), width=25, show='*')
        entry_pass.grid(row=7, column=1, padx=10, pady=10, sticky=W)

        # Confirm Password
        c_password = Label(main_frame, text="Confirm Password:", font=('times new roman', 16, 'bold'))
        c_password.grid(row=8, column=0, padx=10, pady=10, sticky=W)

        entry_confirm = ttk.Entry(main_frame, textvariable=self.confirm_pass, font=('times new roman', 16, 'bold'), width=25, show='*')
        entry_confirm.grid(row=8, column=1, padx=10, pady=10, sticky=W)

        # Check Frame
        check_frame = Frame(main_frame)
        check_frame.place(x=130, y=460, width=400, height=70)

        check_btn = Checkbutton(check_frame, text='Agree to our Terms and Conditions', variable=self.check_var, font=('times new roman', 16), onvalue=1, offvalue=0)
        check_btn.grid(row=0, column=0, padx=10, sticky=W)

        self.check_lbl = Label(check_frame, font=("arial", 16), fg='red')
        self.check_lbl.grid(row=1, column=0, padx=10, sticky=W)

        # Button Frame
        btn_frame = Frame(main_frame)
        btn_frame.place(x=30, y=530, width=450, height=60)

        register = Button(btn_frame, text='Register', command=self.validation, font=('times new roman', 16, 'bold'), width=12, cursor='hand2', bg='blue', fg='white')
        register.grid(row=0, column=0, padx=1, sticky=W)

        verify_data = Button(btn_frame,text='Verify Data', command=self.verify_data, font=('times new roman', 16, 'bold'), width=12, cursor='hand2', bg='blue', fg='white')
        verify_data.grid(row=0, column=1, padx=1, sticky=W)

        clear_data = Button(btn_frame, text='Clear Data', command=self.clear_data, font=('times new roman', 16, 'bold'), width=12, cursor='hand2', bg='blue', fg='white')
        clear_data.grid(row=0, column=2, padx=1, sticky=W)

    def checkname(self, name):
        if name.isalnum():
            return True
        if name == '':
            return True
        else:
            messagebox.showerror('Invalid', 'Not Allowed: ' + name[-1])
            return False

    def checkcontact(self, contact):
        if contact.isdigit():
            return True
        if len(str(contact)) == 0:
            return True
        else:
            messagebox.showerror("Invalid", 'Invalid Entry')
            return False

    def checkpassword(self, password):
        if len(password) <= 21:
            if re.match(r"^(?=.*[0-9])(?=.*[A-Z])(?=.*[^a-zA-Z0-9]).{8,}$", password):
                return True
            else:
                messagebox.showinfo('Invalid', 'Enter a valid password (Example: Abhijeet@15)')
                return False
        else:
            messagebox.showerror('Invalid', 'Password length exceeds 21 characters')
            return False

    def checkemail(self, email):
        if len(email) > 7:
            if re.match(r"^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$", email):
                return True
            else:
                messagebox.showwarning('Alert', 'Invalid email. Enter a valid user email (example: aviabhijeet7@gmail.com)')
                return False
        else:
            messagebox.showinfo('Invalid', 'Email length is too short')
            return False

    def validation(self):
        if self.name_var.get() == '':
            self.engine.say('Please enter your name')
            self.engine.runAndWait()
            messagebox.showerror('Error', 'Please enter your name', parent=self.root)
        elif not self.checkemail(self.email_var.get()):
            messagebox.showerror('Error', 'Invalid email', parent=self.root)
        elif not self.checkcontact(self.contact_var.get()):
            messagebox.showerror('Error', 'Invalid contact number', parent=self.root)
        elif self.country_var.get() == 'Select your country':
            messagebox.showerror('Error', 'Please select your country', parent=self.root)
        elif self.combo_id_type.get() == 'Select Your Id':
            messagebox.showerror('Error', 'Please select your ID type', parent=self.root)
        elif self.id_number_var.get() == '':
            messagebox.showerror('Error', 'Please enter your ID number', parent=self.root)
        elif not self.checkpassword(self.password.get()):
            return
        elif self.password.get() != self.confirm_pass.get():
            messagebox.showerror('Error', 'Passwords do not match', parent=self.root)
        elif self.check_var.get() == 0:
            messagebox.showerror('Error', 'Please agree to the terms and conditions', parent=self.root)
        else:
            messagebox.showinfo('Success', 'Registration Successful', parent=self.root)

        if self.email_var.get() and self.password.get():
            if self.checkemail(self.email_var.get()) and self.checkpassword(self.password.get()):
                if self.check_var.get() == 1:
                    self.check_lbl.config(text='Checked', fg='green')
                    try:
                        conn = mysql.connector.connect(host='localhost', username='root', password='', database='Register')
                        my_cursor = conn.cursor()
                        my_cursor.execute('insert into Data values(%s,%s,%s,%s,%s,%s,%s,%s)', (
                            self.name_var.get(),
                            self.email_var.get(),
                            self.contact_var.get(),
                            self.gender_var.get(),
                            self.country_var.get(),
                            self.id_var.get(),
                            self.id_number_var.get(),
                            self.password.get()
                        ))
                        conn.commit()
                        conn.close()
                        messagebox.showinfo('Success', f'Your registration is successfully completed.\nUsername: {self.name_var.get()}\nPassword: {self.password.get()}')
                    except Exception as es:
                        messagebox.showerror('Error', f'Due to: {str(es)}', parent=self.root)
                else:
                    self.check_lbl.config(text='Agree to our Terms and Conditions', fg='red')

    def verify_data(self):
        # Method to verify data
        data= f'Name:{self.name_var.get()}\nEmail:{self.email_var.get()}\nContact:{self.contact_var.get()}\nGender:{self.gender_var.get()}\nCountry_Name:{self.country_var.get()}\nId:{self.id_var.get}\nid Number:{self.id_number_var.get()}\nPassword:{self.password.get()}'
        messagebox.showinfo('Details',data)
        pass

    def clear_data(self):
        self.name_var.set('')
        self.email_var.set('')
        self.contact_var.set('')
        self.gender_var.set('Male')
        self.country_var.set('Select your country')
        self.id_var.set('Select Your Id')
        self.id_number_var.set('')
        self.password.set('')
        self.confirm_pass.set('')
        self.check_var.set(0)

if __name__ == "__main__":
    root = Tk()
    app = Register(root)
    root.mainloop()
