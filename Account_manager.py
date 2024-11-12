from tkinter import *
from tkinter import ttk
from tkmacosx import *
from PIL import ImageTk
from tkinter import messagebox
import sqlite3
from cryptography.fernet import Fernet
import random

# create cryptography
def generate_key():
    try:
        with open ('account_manager_key','rb') as file:
            return file.read()
    except FileNotFoundError:
        key = Fernet.generate_key()
        with open ('account_manager_key', 'wb') as file:
            file.write(key)
        return key

key = generate_key()
cipher_suite = Fernet(key)

def encrypt(password):
    encoded_password = password.encode() # let password become into bytes
    encrypted_password = cipher_suite.encrypt(encoded_password) #lock
    return encrypted_password

def decrypt(encrypted_password):
    decrypted_password = cipher_suite.decrypt(encrypted_password) #unlock
    decoded_password = decrypted_password.decode() # from bytes into password
    return decoded_password




# Create SQLite
conn = sqlite3.connect('Account_Storage.db')
cur = conn.cursor()
cur.execute(
    '''
    CREATE TABLE IF NOT EXISTS account_manager (
    Account_name TEXT PRIMARY KEY,
    Account TEXT,
    Password BLOB,
    Category TEXT,
    Tags TEXT
    )
    '''
)
conn.commit()
conn.close()

def click():
    username = username_entry.get()
    accountnum = accountnum_entry.get()
    password = password_entry.get()
    cate_choose = category_combobox.get()
    tag_choose = tag_combobox.get()

    encrypted_password = encrypt(password) #lock password

    conn = sqlite3.connect('Account_Storage.db')
    cur = conn.cursor()
    cur.execute('SELECT Account_name FROM account_manager')
    records = cur.fetchall() # get account_name like tuple in List
    conn.close()

    account_name_records = [record[0] for record in records]

    if username == '' or accountnum == '' or password == '' or cate_choose not in category_list or tag_choose not in tag_list:
        messagebox.showerror(title = 'Error', message= 'Please enter all information')
    elif username in account_name_records:
        messagebox.showerror(title = 'Error', message ='Account had already existed' )
    else:
        conn = sqlite3.connect('Account_Storage.db')
        cur = conn.cursor()
        cur.execute('INSERT INTO account_manager (Account_name, Account, Password, Category, Tags) VALUES (?,?,?,?,?)',
                    (username, accountnum, encrypted_password, cate_choose, tag_choose))
        conn.commit()
        conn.close()

        messagebox.showinfo(title='Successful', message = 'Success')



def search():
    username = username_entry.get()

    conn = sqlite3.connect('Account_Storage.db')
    cur = conn.cursor()
    cur.execute(
        'SELECT Account_name, Account, Password, Category, Tags from account_manager '
    )
    records = cur.fetchall()  # get account_name like tuple in List
    conn.close()

    account_name_records = [record[0] for record in records]
    account_records = [record[1] for record in records]
    password_records = [record[2] for record in records]
    category_records = [record[3] for record in records]
    tag_records = [record[4] for record in records]
    password_account = {}
    for account_name, account, encrypted_password, category, tag in zip(account_name_records, account_records, password_records,category_records, tag_records):
        decrypted_password = decrypt(encrypted_password) # unlock
        password_account[account_name] = {
            'Account': account,
            'Password': decrypted_password,
            'Category': category,
            'Tags': tag
        }

    if username in account_name_records:
        messagebox.showinfo(title='Information', message= f'Username: {username}\n'
        f'Account: {password_account[username]['Account']}\n'
        f'Password: {password_account[username]['Password']}\n'
        f'Category: {password_account[username]['Category']}\n'
        f'Tag: {password_account[username]['Tags']}'
        )

    else:
        messagebox.showerror(title='Error', message='No this account')

def gen_random_password():
    letters_upper = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
                     "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
                     "U", "V", "W", "X", "Y", "Z"]

    letters_lower = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
                     "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
                     "u", "v", "w", "x", "y", "z"]

    numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

    symbols = ["!", "@", "#", "$", "%", "^", "&", "*", "-", "+"]

    ran_password = ''
    ran_upper_num = random.randint(0, 7)
    for a in range(0, ran_upper_num):
        ran_password += letters_upper[random.randint(0, 25)]

    ran_lower_num = random.randint(0, 5)
    for a in range(0, ran_lower_num):
        ran_password += letters_lower[random.randint(0, 25)]

    ran_numbers_num = random.randint(0, 7)
    for a in range(0, ran_numbers_num):
        ran_password += numbers[random.randint(0, 9)]

    ran_symbols_num = random.randint(0, 5)
    for a in range(0, ran_symbols_num):
        ran_password += symbols[random.randint(0, 9)]

    password_list = list(ran_password)
    random.shuffle(password_list)
    new_password = ''
    for cha in password_list:
        new_password += cha

    password_entry.delete(0,END)
    password_entry.insert(0,new_password)


def search_cate():
    search_category = search_category_combobox.get()
    conn = sqlite3.connect('Account_Storage.db')
    cur = conn.cursor()
    cur.execute(
       'SELECT * FROM account_manager WHERE Category = ?',
        (search_category,))
    records = cur.fetchall()
    conn.close()

    if not records:
        messagebox.showerror(title='Error', message='No accounts found under this category')
        return

    results = []
    for record in records:
        account_name = record[0]
        account = record[1]
        encrypted_password = record[2]
        category = record[3]
        tag = record[4]
        decrypted_password = decrypt(encrypted_password)  # unlock

        results.append(
            f'Username: {account_name}\n'
            f'Account: {account}\n'
            f'Password: {decrypted_password}\n'
            f'Category: {category}\n'
            f'Tag: {tag}\n'
            '_________________________'
        )

    all_message = "\n\n".join(results) # merge all information
    messagebox.showinfo(title = 'Account Information', message = all_message)

def search_tag():
    search_tag = search_tag_combobox.get()
    conn = sqlite3.connect('Account_Storage.db')
    cur = conn.cursor()
    cur.execute(
        'SELECT * FROM account_manager WHERE Tags = ?',
        (search_tag,)
    )
    records = cur.fetchall()
    conn.close()

    if not records:
        messagebox.showerror(title='Error', message='No accounts found under this tag')
        return

    results = []
    for record in records:
        account_name = record[0]
        account = record[1]
        encrypted_password = record[2]
        category = record[3]
        tag = record[4]
        decrypted_password = decrypt(encrypted_password)  # unlock

        results.append(
            f'Username: {account_name}\n'
            f'Account: {account}\n'
            f'Password: {decrypted_password}\n'
            f'Category: {category}\n'
            f'Tag: {tag}\n'
            '_________________________'
        )
    all_message = "\n\n".join(results)  # merge all information
    messagebox.showinfo(title='Account Information', message=all_message)



window = Tk()
window. title('Password manager')
window.geometry('600x700')
window.resizable(False, False)
window.config(padx = 130, pady = 40, bg = 'white')

img = ImageTk.PhotoImage(file = 'lock.png')
canvas = Canvas(width = 224, height = 225, bg = 'white', highlightthickness = 0)
canvas.create_image(112, 112, image = img)
canvas.grid(row = 0, column = 0, columnspan = 2)
# window.iconphoto(True, img)


first_label = Label(text = 'User name', bg = 'white', fg = 'black')
first_label.grid(row = 1, column = 0, pady = 3)
username_entry = Entry(width = 25, bg = 'white', highlightthickness = 0, fg = 'black')
username_entry.grid(row = 1, column = 1, pady = 3)



second_label = Label(text = 'account number', bg = 'white', fg = 'black')
second_label.grid(row = 2, column = 0, pady = 3)
accountnum_entry = Entry(width = 25, bg = 'white', highlightthickness = 0, fg = 'black')
accountnum_entry.grid(row = 2, column = 1, pady = 3)

third_label = Label(text = 'password', bg = 'white', fg = 'black')
third_label.grid(row = 3, column = 0, pady = 3)
password_entry = Entry(width = 25, bg = 'white', highlightthickness = 0, fg = 'black')
password_entry.grid(row = 3, column = 1, pady = 3)


add_button = Button(text = 'add', width = 350, bg = '#0066cc', highlightthickness = 0, fg = 'white', command = click)
add_button.grid(row = 5, column = 0, columnspan = 2, pady = 5)


search_button = Button(text='search', width = 350, bg = '#8E8E8E', highlightthickness = 0, fg = 'white',command = search)
search_button.grid(row = 4, column=0, columnspan=2, pady = 10)

add_ran_password_button = Button(text = 'add random password', width = 350, bg = 'sky blue', highlightthickness = 0, fg = 'white', command = gen_random_password)
add_ran_password_button.grid(row = 6, column = 0, columnspan = 2, pady = 5)

# create Combobox-category
category_list = [
    'Social Media',
    'Finance & Payment',
    'Work & Business',
    'Entertainment & Streaming',
    'E-commerce & Shopping'
]
category_combobox = ttk.Combobox(width = 36, values = category_list)
category_combobox.set('Select the category')
category_combobox.grid(row = 7, column = 0,columnspan = 2, pady = 5)





# create Combobox-tag
tag_list = [
    'Important',
    'Family',
    'Travel',
    'Backup',
    'Education'
]
tag_combobox = ttk.Combobox(width = 36, values = tag_list)
tag_combobox.set('Select the tag')
tag_combobox.grid(row = 8, column = 0,columnspan = 2, pady = 5)


# Search system-category

search_category_combobox = ttk.Combobox(width = 36, values= category_list)
search_category_combobox.set('Search by category')
search_category_combobox.grid(row = 9, column = 0,columnspan = 2, pady = 1)

search_cate_button= Button(text = 'search', width = 80, bg = '#8E8E8E', highlightthickness = 0, fg = 'white',command = search_cate)
search_cate_button.grid(row = 9, column = 2, columnspan = 1, pady = 1)

# Search system-tag
search_tag_combobox = ttk.Combobox(width = 36, values= tag_list)
search_tag_combobox.set('Search by tag')
search_tag_combobox.grid(row = 10, column = 0,columnspan = 2, pady = 1)

search_tag_button= Button(text = 'search', width = 80, bg = '#8E8E8E', highlightthickness = 0, fg = 'white', command = search_tag)
search_tag_button.grid(row = 10, column = 2, columnspan = 1, pady = 1)



window. mainloop()