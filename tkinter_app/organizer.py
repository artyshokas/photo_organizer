from tkinter import *
from tkinter import messagebox, filedialog
from PIL import ImageTk, Image
import requests
import json


def album_details():
    root = Toplevel(organizer)
    root.title('album details')
    root.geometry('800x600')

    URL = 'http://127.0.0.1:8000/'

    def get_album_list():
        album_list.delete(0, END)
        pk = selected_item[0]
        r = requests.get(f"http://127.0.0.1:8000/album/{pk}/photos")
        req_data = json.loads(r.text)
        data = []
        for i in req_data:
            res = i.values()
            data.append(list(res))
        for d in data:
            album_list.insert(END, d)


    def select(event):
        try:
            global selected
            index = album_list.curselection()[0]
            selected = album_list.get(index)
            comment_entry.delete(0, END)
            comment_entry.insert(END, selected[1])
        except Exception as e:
            print(e)

    def view_photo():
        global photo
        selected_path = selected[2]
        selected_photo = selected_path[39:]
        photo = PhotoImage(file=f"C:\\Users\\Artiom\\python_ptu5\\photo_organizer\\ptu5_organizer\\media\\user_photos\\{selected_photo}")
        photo_field.image_create(END, image=photo)

    def upload_file():
        global filename, img
        f_types =[('Png files','*.png'),('Jpg Files', '*.jpg')]
        filename = filedialog.askopenfilename(filetypes=f_types)
        img = ImageTk.PhotoImage(file=filename)
        photo_field.image_create(END, image=img)

    def update():
        if token:
            if comment_text.get() == '' or photo_field.get("1.0", END) == '':
                messagebox.showerror('Please fill in all fields')
            else:
                # upd_photo = filename[29:]
                pk = selected[0]
                data = {
                    "comment": comment_text.get(),
                    # "photo": "http://127.0.0.1:8000/media/user_photos/acespades.png",
                    }
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f'Token {token}'
                }
                response = requests.put(f"http://127.0.0.1:8000/photo/{pk}/", json=data, headers=headers)
                get_album_list()



    photo_field = Text(root, width=40, height=10)
    photo_field.grid(row=3, column=5)

    comment_text = StringVar()
    comment_label = Label(root, text='Comment', font=('bold', 14), pady=20)
    comment_label.grid(row=0, column=0)

    comment_entry = Entry(root, textvariable=comment_text)
    comment_entry.grid(row=0, column=1)

    upload_button = Button(root, text='Upload photo', command=upload_file)
    upload_button.grid(row=8, column=9)

    add_photo_button = Button(root, text='Add photo', command=update)
    add_photo_button.grid(row=9, column=9)


    photo_button = Button(root, text='Photo', command=view_photo)
    photo_button.grid(row=1, column=0)



    album_list = Listbox(root, height=15, width=45, border=1)
    album_list.grid(row=3, column=0, columnspan=3, rowspan=9, pady=20, padx=20, sticky=NSEW)

    scrollbar = Scrollbar(root, orient=VERTICAL)
    scrollbar.grid(row=4, column=2, sticky=NS)

    album_list.configure(yscrollcommand=scrollbar.set)
    scrollbar.configure(command=album_list.yview)

    album_list.bind('<<ListboxSelect>>', select)

    album_details_button = Button(root, text='View details', width=15, command=get_album_list)
    album_details_button.grid(row=7, column=9, pady=20)

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
                messagebox.showerror('ERROR!')
            get_list()



    def add():
        try:
            if token:
                if album_text.get() == '' or albumdesc_text.get() == '':
                    messagebox.showerror('Please fill in all fields')
                else:
                    address = 'http://127.0.0.1:8000/albums/'
                    data = {
                        "name": album_text.get(),
                        "description": albumdesc_text.get()
                        }
                    headers = {
                        "Content-Type": "application/json",
                        "Authorization": f'Token {token}'
                    }
                    response = requests.post(address, json=data, headers=headers)
                    album_list.delete(0, END)
                    album_list.insert(END, (album_text.get(), albumdesc_text.get()))
                    clear()
                    get_list()
        except Exception as e:
            print(e)

    
    def update():
        try:
            if token:
                if album_text.get() == '' or albumdesc_text.get() == '':
                    messagebox.showerror('Please fill in all fields')
                else:
                    pk = selected_item[0]
                    data = {
                        "name": album_text.get(),
                        "description": albumdesc_text.get()
                        }
                    headers = {
                        "Content-Type": "application/json",
                        "Authorization": f'Token {token}'
                    }
                    response = requests.put(f"http://127.0.0.1:8000/album/{pk}/", json=data, headers=headers)
                    get_list()
        except Exception as e:
            print(e)


    def select(event):
        try:
            global selected_item
            index = album_list.curselection()[0]
            selected_item = album_list.get(index)
            album_entry.delete(0, END)
            album_entry.insert(END, selected_item[1])
            albumdesc_entry.delete(0, END)
            albumdesc_entry.insert(END, selected_item[2])
        except Exception as e:
            print(e)



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

    album_list.bind('<<ListboxSelect>>', select)

    login_button = Button(organizer, text='Login', fg='red', width=15, command=login)
    addalbum_button = Button(organizer, text='Add album', width=15, command=add)
    deletealbum_button = Button(organizer, text='Delete album', width=15)
    updatealbum_button = Button(organizer, text='Update album', width=15, command=update)
    clear_button = Button(organizer, text='Clear', width=15, command=clear)
    album_details_button = Button(organizer, text='View album', width=15, command=album_details)

    login_button.grid(row=2, column=9, pady=20)
    addalbum_button.grid(row=3, column=9, pady=20)
    deletealbum_button.grid(row=4, column=9, pady=20)
    updatealbum_button.grid(row=5, column=9, pady=20)
    clear_button.grid(row=6, column=9, pady=20)
    album_details_button.grid(row=7, column=9, pady=20)

    organizer.title('Photo Organizer')
    organizer.geometry('800x600')

    organizer.mainloop()
main_screen()