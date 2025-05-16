import json
import math
import random
import tkinter
from operator import length_hint
from tkinter import *
from tkinter import messagebox
import pyperclip

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
list_upper = []
list_lower = []
list_number = []
list_symbol = []

# Generate list of uppercase letters
for i in range(65, 91):
    list_upper.append(chr(i))

# Generate list of lowercase letters
for i in range(97, 123):
    list_lower.append(chr(i))

# Generate list of numbers
for i in range(48, 58):
    list_number.append(chr(i))

# Generate list of symbols
for i in range(33, 48):
    list_symbol.append(chr(i))
for i in range(58, 65):
    list_symbol.append(chr(i))
for i in range(91, 97):
    list_symbol.append(chr(i))
for i in range(123, 127):
    list_symbol.append(chr(i))


def open_generator():
    def get_value():
        return upper_scale.get()

    gen_pass_window = Tk()
    gen_pass_window.title("Password settings")
    gen_pass_window.geometry("+1100+200")
    gen_pass_window.minsize(width=150, height=150)
    gen_pass_window.config(padx=20, pady=20)

    # Scale for selecting the number of uppercase letters amount included in password
    upper_label = Label(gen_pass_window, text="How many uppercase letters?")
    upper_label.grid(row=0, column=0)

    upper_scale = Scale(gen_pass_window, orient="horizontal", length=100, from_=1, to=8)
    upper_scale.grid(row=1, column=0, pady=(0, 30))

    # Scale for selecting the number of lowercase letters included in password
    lower_label = Label(gen_pass_window, text="How many lowercase letters?")
    lower_label.grid(row=2, column=0)

    lower_scale = Scale(gen_pass_window, orient="horizontal", length=100, from_=1, to=8)
    lower_scale.grid(row=3, column=0, pady=(0, 30))

    # Scale for selecting the number of numbers included in password
    number_label = Label(gen_pass_window, text="How many numbers?")
    number_label.grid(row=4, column=0)

    number_scale = Scale(gen_pass_window, orient="horizontal", length=100, from_=1, to=5)
    number_scale.grid(row=5, column=0, pady=(0, 30))

    # Scale for selecting the number of symbols included in password
    symbol_label = Label(gen_pass_window, text="How many symbols?")
    symbol_label.grid(row=6, column=0)

    symbol_scale = Scale(gen_pass_window, orient="horizontal", length=100, from_=1, to=5)
    symbol_scale.grid(row=7, column=0, pady=(0, 30))

    def generate_password():
        password_input.delete(0, END)

        uppercase_count = math.floor(upper_scale.get())
        lowercase_count = math.floor(lower_scale.get())
        number_count = math.floor(number_scale.get())
        symbol_count = math.floor(symbol_scale.get())

        passw_upper_list = [random.choice(list_upper) for _ in range(uppercase_count)]
        passw_lower_list = [random.choice(list_lower) for _ in range(lowercase_count)]
        passw_num_list = [random.choice(list_number) for _ in range(number_count)]
        passw_symbol_list = [random.choice(list_symbol) for _ in range(symbol_count)]

        password_list = passw_symbol_list + passw_num_list + passw_lower_list + passw_upper_list
        random.shuffle(password_list)

        password = "".join(password_list)

        pyperclip.copy(password)

        password_input.insert(0, password)

    # Generate password button
    generate_button = Button(gen_pass_window, text="Generate", command=generate_password)
    generate_button.grid(row=8, column=0, padx=20, pady=20)

    gen_pass_window.mainloop()

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_input.get()
    username = username_input.get()
    password = password_input.get()

    new_data = {
        website: {
            "username": username,
            "password": password
        }
    }

    if len(website) * len(username) * len(password) == 0:
        messagebox.showinfo(title="Error", message="Please fill all of the brackets.")
        return

    is_ok = messagebox.askokcancel(title=website, message="These are the details entered:\n"
                                                  f"Username/E-mail: {username}\n"
                                                  f"Password: {password}\n"
                                                  f"Do you want to save?")

    if is_ok:
        try:
            with open("passwords.json", "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            with open("passwords.json", "w") as file:
                json.dump(new_data, file, indent=4)
        else:
            data.update(new_data)
            with open("passwords.json", "w") as file:
                json.dump(data, file, indent=4)
        finally:
            website_input.delete(0, END)
            password_input.delete(0, END)

# ----------------------------- SEARCH -------------------------------- #
def search():
    searched_website = website_input.get()

    try:
        with open("passwords.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        messagebox.showinfo("Error", "No data file found.")
    else:
        try:
            print(data[searched_website])
        except KeyError:
            messagebox.showinfo("Error", "Website not found.")
        else:
            messagebox.showinfo(searched_website, f"Username: {data[searched_website]["username"]}\n"
                                                  f"Password: {data[searched_website]["password"]}")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.config(padx=40, pady=30)
window.geometry("+600+200")

canvas = Canvas(width=200, height=200)
logo = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo)
canvas.grid(row=0, column=0, columnspan=3)

website_label = Label(text="Website: ")
website_label.grid(row=1, column=0, sticky="e")

website_input = Entry(width=33)
website_input.grid(row=1, column=1)
website_input.focus()

username_label = Label(text="Username/E-mail: ")
username_label.grid(row=2, column=0, sticky="e")

username_input = Entry(width=52)
username_input.grid(row=2, column=1, columnspan=2)

password_label = Label(text="Password: ")
password_label.grid(row=3, column=0, sticky="e")

password_input = Entry(width=33)
password_input.grid(row=3, column=1)

gen_password_button = Button(text="Generate password", command=open_generator)
gen_password_button.grid(row=3, column=2)

add_button = Button(text="Add", width=44, command=save)
add_button.grid(row=4, column=1, columnspan=2)

search_button = Button(text="Search", width=15, command=search)
search_button.grid(row=1, column=2)

window.mainloop()