import tkinter.messagebox
from tkinter import *
import random
import json

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
           'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
           'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

PASSWORD_LENGTH = 8
SYMBOLS_COUNT = 2
NUMERIC_COUNT = 2


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    password_entry.delete(0, "end")
    # letters
    password = []
    for letter in range(1, PASSWORD_LENGTH - SYMBOLS_COUNT - NUMERIC_COUNT + 1):
        password.append(random.choice(letters))

    # symbols
    for symbol in range(1, SYMBOLS_COUNT + 1):
        password.append(random.choice(symbols))

    # numbers
    for number in range(1, NUMERIC_COUNT + 1):
        password.append(random.choice(numbers))

    random.shuffle(password)

    shuffled_password = ""

    for char in password:
        shuffled_password += char

    password_entry.insert(0, shuffled_password)
    password_entry.clipboard_clear()
    password_entry.clipboard_append(shuffled_password)


# ---------------------------- TXT FILE DATABASE ------------------------------- #
# def save_password():
#     existing_detail = check_existing()
#     if len(existing_detail) == 1:
#         email = email_entry.get()
#         website = website_entry.get()
#         password = password_entry.get()
#
#
#         with open("data.txt", mode="a") as file:
#             file.write(f"{website} | {email} | {password}\n")
#     else:
#         password_entry.delete(0, "end")
#         password_entry.insert(0, "Already in database")
#
#
#
def get_password():
    website = website_entry.get()
    existing_detail = check_existing(website)

    if type(existing_detail) is list:

        if len(existing_detail) == 1:
            email_entry.delete(0, "end")
            email_entry.insert(0, existing_detail[0][website]["email"])

            password_entry.delete(0, "end")
            password_entry.insert(0, existing_detail[0][website]["password"])
        else:
            email_entry.delete(0, "end")
            email_entry.insert(0, "NOT FOUND")


#
#
#
# def check_existing():
#     with open("data.txt", mode="r") as file:
#         data = file.readlines()
#     password_dict = []
#     for items in data:
#         data[data.index(items)] = items.strip()
#         content = items.split(" | ")
#         password_dict.append({"website": content[0],
#                               "email": content[1],
#                               "password": content[2],
#                               })
#
#     website = website_entry.get()
#     for items in password_dict:
#         if items["website"] == website:
#             return [items["email"], items["password"]]
#     return [0]

# ---------------------------- JSON file database ------------------------------- #
def check_existing(website):
    try:
        with open("data.json", mode="r") as file:
            json_data = json.load(file)
            if website in json_data:
                return [json_data]
            else:
                return [False, json_data]
    except:
        return False


def save_password():
    email = email_entry.get()
    website = website_entry.get()
    password = password_entry.get()
    json_model = {website: {"email": email,
                            "password": password}}
    alert_message_boc = None

    existing_data = check_existing(website)

    # if no json file found or any other issue in checking existing file. create new file
    if existing_data is False:
        with open("data.json", mode="w") as file:
            json.dump(fp=file, obj=json_model)
            return

    elif len(existing_data) == 1:
        website_details = existing_data[0][website]
        existing_email = website_details["email"]
        existing_password = website_details["password"]
        alert_message_boc = tkinter.messagebox.askokcancel(title=f"Data already exist for website{website}",
                                                           message=f"Username: {existing_email}\nPassword: {existing_password}\n\nDo you want to update with new details? ")

    if len(existing_data) > 1 or (alert_message_boc is True):
        with (open("data.json", mode="w") as file):
            if alert_message_boc is True:
                new_data = existing_data[0]
                new_data.update(json_model)
                print(new_data)
            else:
                new_data = existing_data[1]
                new_data.update(json_model)

            json.dump(fp=file, obj=new_data)

    # with open("data.json", mode="r") as file:
    #
    #
    # password_entry.delete(0, "end")
    # # password_entry.insert(0, "Already in database")

    # if len(existing_detail) == 1:
    #
    #
    #
    #     with open("data.txt", mode="a") as file:
    #         file.write(f"{website} | {email} | {password}\n")
    # else:
    #     password_entry.delete(0, "end")
    #     password_entry.insert(0, "Already in database")


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(pady=50, padx=50)

lock_image = PhotoImage(file="logo.png")

canvas = Canvas()
canvas.config(width=200, height=200)
canvas.create_image(100, 100, image=lock_image)
canvas.grid(column=1, row=0)

website_label = Label()
website_label.config(text="Website")
website_label.grid(column=0, row=1)

website_entry = Entry(width=35)
website_entry.grid(column=1, row=1)
website_entry.focus()

website_check = Button()
website_check.config(text="Retrieve details", command=get_password)
website_check.grid(column=2, row=1)

email_label = Label()
email_label.config(text="Email/Username")
email_label.grid(column=0, row=2)

email_entry = Entry(width=35)
email_entry.grid(column=1, row=2)
email_entry.insert(0, "yaitsmethiyagu@gmail.com")

password_label = Label()
password_label.config(text="Password")
password_label.grid(column=0, row=3)

password_entry = Entry(width=22)
password_entry.grid(column=1, row=3)

generate = Button()
generate.config(text="Generate Password", command=generate_password)
generate.grid(column=2, row=3)

add_button = Button()
add_button.config(text="Add", width=36, command=save_password)
add_button.grid(column=1, row=4, columnspan=3)

window.mainloop()
