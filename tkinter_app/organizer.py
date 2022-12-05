from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import requests
import json


def album_details():
    root = Toplevel(organizer)
    root.title('album details')
    root.geometry('800x600')

def main_screen():

    global organizer

    organizer = Tk()

    URL = 'http://127.0.0.1:8000/'

    def get_list():
        album_list.delete(0, END)
        if token:
            headers = {
                'Authorization': f'Token {token}'
            }
            r = requests.get(URL+'albums/', headers=headers)
            req_data = json.loads(r.text)
            data = []
            for i in req_data:
                res = i.values()
                data.append(list(res))
            for d in data:
                album_list.insert(END, d)
                print(get_list)


    def login():
        global token
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
                messagebox.showerror('Invalid Username or Password!')
            get_list()



    def clear():
        album_entry.delete(0, END)
        albumdesc_entry.delete(0, END)



    username_text = StringVar()
    username_label = Label(organizer, text='Username', fg="red", font=('bold', 10), padx=20)
    username_label.grid(row=0, column=8)
    username_entry = Entry(organizer, textvariable=username_text)
    username_entry.grid(row=0, column=9)

    password_text = StringVar()
    password_label = Label(organizer, text='Password', fg="red", font=('bold', 10), padx=20)
    password_label.grid(row=1, column=8)
    password_entry = Entry(organizer, show="*", textvariable=password_text)
    password_entry.grid(row=1, column=9)

    album_text = StringVar()
    album_label = Label(organizer, text='Album name', font=('bold', 14), pady=20)
    album_label.grid(row=0, column=0)

    album_entry = Entry(organizer, textvariable=album_text)
    album_entry.grid(row=0, column=1)

    albumdesc_text = StringVar()
    albumdesc_label = Label(organizer, text='Album description', font=('bold', 14))
    albumdesc_label.grid(row=1, column=0)

    albumdesc_entry = Entry(organizer, textvariable=albumdesc_text)
    albumdesc_entry.grid(row=1, column=1, padx=10, pady=10, ipadx=50, ipady=50)

    album_list = Listbox(organizer, height=15, width=45, border=1)
    album_list.grid(row=3, column=0, columnspan=3, rowspan=9, pady=20, padx=20, sticky=NSEW)

    scrollbar = Scrollbar(organizer, orient=VERTICAL)
    scrollbar.grid(row=4, column=2, sticky=NS)

    album_list.configure(yscrollcommand=scrollbar.set)
    scrollbar.configure(command=album_list.yview)

    album_list.bind('<<ListboxSelect>>')

    login_button = Button(organizer, text='Login', fg='red', width=15, command=login)
    addalbum_button = Button(organizer, text='Add album', width=15)
    deletealbum_button = Button(organizer, text='Delete album', width=15)
    updatealbum_button = Button(organizer, text='Update album', width=15)
    clear_button = Button(organizer, text='Clear', width=15, command=clear)
    album_details_button = Button(organizer, text='View album', width=15)

    login_button.grid(row=2, column=9, pady=20)
    addalbum_button.grid(row=3, column=9, pady=20)
    deletealbum_button.grid(row=4, column=9, pady=20)
    updatealbum_button.grid(row=5, column=9, pady=20)
    clear_button.grid(row=6, column=9, pady=20)
    album_details_button.grid(row=7, column=9, pady=20)

    organizer.title('band_api')
    organizer.geometry('800x600')

    organizer.mainloop()
main_screen()