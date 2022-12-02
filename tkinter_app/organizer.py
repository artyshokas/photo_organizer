from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import requests
import json




app = Tk()

URL = 'http://127.0.0.1:8000/'


def login():
    username = username_entry.get()
    password = password_entry.get()
    print(username, password)
    if username == '' or password == '':
        messagebox.showerror('cannot be empty')
    else:
        data = {
            "username": username,
            "password": password,
        }
        try:
            response = requests.post(URL+'api-token-auth/', data=data)
            response_dict = json.loads(response.text)
            print(response_dict)
            token = response_dict['token']
            print(token)
        except Exception as e:
            messagebox.showerror('ERROR!')



def clear():
    album_entry.delete(0, END)
    albumdesc_entry.delete(0, END)



username_text = StringVar()
username_label = Label(app, text='Username', fg="red", font=('bold', 10), padx=20)
username_label.grid(row=0, column=8)
username_entry = Entry(app, textvariable=username_text)
username_entry.grid(row=0, column=9)

password_text = StringVar()
password_label = Label(app, text='Password', fg="red", font=('bold', 10), padx=20)
password_label.grid(row=1, column=8)
password_entry = Entry(app, show="*", textvariable=password_text)
password_entry.grid(row=1, column=9)

album_text = StringVar()
album_label = Label(app, text='Album name', font=('bold', 14), pady=20)
album_label.grid(row=0, column=0)

album_entry = Entry(app, textvariable=album_text)
album_entry.grid(row=0, column=1)

albumdesc_text = StringVar()
albumdesc_label = Label(app, text='Album description', font=('bold', 14))
albumdesc_label.grid(row=1, column=0)

albumdesc_entry = Entry(app, textvariable=albumdesc_text)
albumdesc_entry.grid(row=1, column=1, padx=10, pady=10, ipadx=50, ipady=50)

album_list = Listbox(app, height=15, width=45, border=1)
album_list.grid(row=3, column=0, columnspan=3, rowspan=9, pady=20, padx=20, sticky=NSEW)

scrollbar = Scrollbar(app, orient=VERTICAL)
scrollbar.grid(row=4, column=2, sticky=NS)

album_list.configure(yscrollcommand=scrollbar.set)
scrollbar.configure(command=album_list.yview)

album_list.bind('<<ListboxSelect>>')

login_button = Button(app, text='Login', fg='red', width=15, command=login)
addalbum_button = Button(app, text='Add album', width=15)
deletealbum_button = Button(app, text='Delete album', width=15)
updatealbum_button = Button(app, text='Update album', width=15)
clear_button = Button(app, text='Clear', width=15, command=clear)
album_details_button = Button(app, text='View album', width=15)

login_button.grid(row=2, column=9, pady=20)
addalbum_button.grid(row=3, column=9, pady=20)
deletealbum_button.grid(row=4, column=9, pady=20)
updatealbum_button.grid(row=5, column=9, pady=20)
clear_button.grid(row=6, column=9, pady=20)
album_details_button.grid(row=7, column=9, pady=20)

app.title('band_api')
app.geometry('800x600')

app.mainloop()