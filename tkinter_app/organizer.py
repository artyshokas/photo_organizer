from tkinter import *
from tkinter import filedialog
from tkinter import messagebox, filedialog
from PIL import ImageTk
import requests
import json


def album_details():
    root = Toplevel(organizer)
    root.title('album details')
    #root.geometry('800x650')

    URL = 'http://127.0.0.1:8000/'

    def select(event):
        global selected
        index = album_list.curselection()[0]
        selected = album_list.get(index)
        comment_text.delete(1.0, END)
        comment_text.insert(END, selected[1])
        view_photo()

    def view_photo():
        global photo
        selected_path = selected[2]
        selected_photo = selected_path[39:]
        photo = PhotoImage(file=f"C:\\Users\\Artiom\\python_ptu5\\photo_organizer\\ptu5_organizer\\media\\user_photos\\{selected_photo}")
        photo_field.image_create(END, image=photo)

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

    def upload_file():
        global filename, img
        f_types =[('Png files','*.png'),('Jpg Files', '*.jpg')]
        filename = filedialog.askopenfilename(filetypes=f_types)
        img = ImageTk.PhotoImage(file=filename)
        photo_upload_field.image_create(END, image=img)
        print(filename)

    def add():
        if comment_text.get(1.0, END) == '':
            messagebox.showerror('Please fill in all fields')
        else:
            pk = selected[0]
            post_files = {
                    "photo": open(filename, "rb")
                }
            data = {
                "comment": comment_text.get(1.0, END),
                }
            headers = {
                "Authorization": f'Token {token}'
                }
            response = requests.post(f"http://127.0.0.1:8000/album/{pk}/photos", data=data, files=post_files, headers=headers)
            print(response)
            get_album_list()

    def update_comment():
            if comment_text.get(1.0, END) == '':
                messagebox.showerror('Please fill in all fields')
            else:
                pk = selected[0]
                data = {
                    "comment": comment_text.get(1.0, END),
                    }
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f'Token {token}'
                }
                response = requests.put(f"http://127.0.0.1:8000/photo/{pk}/", json=data, headers=headers)
                get_album_list()

    def clear():
        comment_text.delete(1.0, END)
        photo_upload_field.delete(1.0, END)


    photo_field = Text(root, width=45, height=15)
    photo_field.grid(row=6, column=0, padx=(20,2))

    photo_upload_field = Text(root, width=45, height=15)
    photo_upload_field.grid(row=6, column=5, padx=20)

    # comment_text = StringVar()
    comment_label = Label(root, text='Comment', font=('bold', 14))
    comment_label.grid(row=2, column=5)

    comment_text = Text(root, width=45, height=15)
    comment_text.grid(row=3, column=5, columnspan=2, sticky=W+E, padx=20)

    album_details_button = Button(root, text='View details', width=15, command=get_album_list)
    album_details_button.grid(row=10, column=0, pady=20)

    clear_button = Button(root, text='Clear', command=clear)
    clear_button.grid(row=5, column=5)

    upload_button = Button(root, text='Upload photo', command=upload_file)
    upload_button.grid(row=9, column=5)

    add_button = Button(root, text='add photo', command=add)
    add_button.grid(row=10, column=5)

    update_comment_button = Button(root, text='Update comment', command=update_comment)
    update_comment_button.grid(row=4, column=5)

    album_list = Listbox(root, height=15, width=40, border=1)
    album_list.grid(row=2, column=0, columnspan=3, rowspan=4, pady=20, padx=20, sticky=NSEW)

    scrollbar = Scrollbar(root, orient=VERTICAL)
    scrollbar.grid(row=4, column=2, sticky=NS)

    album_list.configure(yscrollcommand=scrollbar.set)
    scrollbar.configure(command=album_list.yview)

    album_list.bind('<<ListboxSelect>>', select)

def main_screen():

    global organizer

    organizer = Tk()
    organizer.title('Photo Organizer')

    URL = 'http://127.0.0.1:8000/'

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

    def select(event):
        global selected_item
        index = album_list.curselection()[0]
        selected_item = album_list.get(index)
        album_entry.delete(0, END)
        album_entry.insert(END, selected_item[1])
        albumdesc_entry.delete(0, END)
        albumdesc_entry.insert(END, selected_item[2])

    def clear():
        album_entry.delete(0, END)
        albumdesc_entry.delete(0, END)

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

    def add():
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

    
    def update():
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

    def delete():
        if album_text.get() == '' or albumdesc_text.get() == '':
            messagebox.showerror('Please fill in all fields')
        else:
            pk = selected_item[0]
            headers = {
                "Content-Type": "application/json",
                "Authorization": f'Token {token}'
            }
            response = requests.delete(f"http://127.0.0.1:8000/album/{pk}/", headers=headers)
            get_list()


    username_text = StringVar()
    username_label = Label(organizer, text='Username', fg="red", font=('bold', 10))
    username_label.grid(row=0, column=8, sticky=W+E)
    username_entry = Entry(organizer, textvariable=username_text)
    username_entry.grid(row=0, column=9, padx=10)

    password_text = StringVar()
    password_label = Label(organizer, text='Password', fg="red", font=('bold', 10))
    password_label.grid(row=1, column=8, sticky=W+E)
    password_entry = Entry(organizer, show="*", textvariable=password_text)
    password_entry.grid(row=1, column=9, padx=10)

    album_text = StringVar()
    album_label = Label(organizer, text='Album name', font=('bold', 10))
    album_label.grid(row=4, column=8, columnspan=2, sticky=W+E, pady=(50, 5))

    album_entry = Entry(organizer, textvariable=album_text)
    album_entry.grid(row=5, column=8, columnspan=2, sticky=W+E, padx=10)

    albumdesc_text = StringVar()
    albumdesc_label = Label(organizer, text='Album description', font=('bold', 10))
    albumdesc_label.grid(row=6, column=8, columnspan=2, sticky=W+E)

    albumdesc_entry = Entry(organizer, textvariable=albumdesc_text)
    albumdesc_entry.grid(row=7, column=8, columnspan=2, sticky=W+E, padx=10, pady=(5, 150))

    album_list = Listbox(organizer, width=50, border=1)
    album_list.grid(row=0, column=0, columnspan=3, rowspan=11, pady=20, padx=2, sticky=NSEW)

    scrollbar = Scrollbar(organizer, orient=VERTICAL)
    scrollbar.grid(row=5, column=3, rowspan=6, sticky=NS)

    album_list.configure(yscrollcommand=scrollbar.set)
    scrollbar.configure(command=album_list.yview)

    album_list.bind('<<ListboxSelect>>', select)

    login_button = Button(organizer, text='Login', fg='red', command=login)
    addalbum_button = Button(organizer, text='Add album', width=15, command=add)
    deletealbum_button = Button(organizer, text='Delete album', width=15, command=delete)
    updatealbum_button = Button(organizer, text='Update album', width=15, command=update)
    clear_button = Button(organizer, text='Clear', width=15, command=clear)
    album_details_button = Button(organizer, text='View album', width=15, command=album_details)

    login_button.grid(row=2, column=8, columnspan=2, sticky=W+E, padx=10)
    addalbum_button.grid(row=10, column=9)
    deletealbum_button.grid(row=11, column=9, pady=(2, 15))
    updatealbum_button.grid(row=10, column=8)
    clear_button.grid(row=11, column=8, pady=(2, 15))
    album_details_button.grid(row=11, column=0, columnspan=3, sticky=W+E, pady=(2, 15))


    organizer.mainloop()
main_screen()