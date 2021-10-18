# Python program to generate random
# password using Tkinter module
import random
import pyperclip
from tkinter import *
from tkinter.ttk import *

# Function for calculation of password
def low():
	entry.delete(0, END)

	# Get the length of password
	length = var1.get()

	lower = "abcdefghijklmnopqrstuvwxyz"
	upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
	digits = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 !@#$%^&*()"
	password = ""

	# if strength selected is low
	if var.get() == 1:
		for i in range(0, length):
			password = password + random.choice(lower)
		return password

	# if strength selected is medium
	elif var.get() == 0:
		for i in range(0, length):
			password = password + random.choice(upper)
		return password

	# if strength selected is strong
	elif var.get() == 3:
		for i in range(0, length):
			password = password + random.choice(digits)
		return password
	else:
		print("Please choose an option")


# Function for generation of password
def generate():
	password1 = low()
	entry.insert(10, password1)


# Function for copying password to clipboard
def copy1():
	random_password = entry.get()
	pyperclip.copy(random_password)


# Main Function

# create GUI window
root = Tk()
var = IntVar()
var1 = IntVar()

# Title of your GUI window
root.title("Random Password Generator")
root.geometry("190x320")
root.maxsize(320,190)
root.minsize(320,190)
root.config(bg="teal")

# create label and entry to show
# password generated

Random_password = Label(root, text="Password")
Random_password.grid(row=0)
entry = Entry(root)
entry.grid(row=0, column=1,padx=10,pady=10)

# create label for length of password
c_label = Label(root, text="Length")
c_label.grid(row=1,padx=10,pady=10)

# create Buttons Copy which will copy
copy_button = Button(root, text="Copy",command=copy1)
copy_button.grid(row=4, column=2, padx=10,pady=10)
# create Buttons will generate the password
generate_button = Button(root, text="Generate", command=generate)
generate_button.grid(row=4, column=1, padx=10,pady=10 )

# Radio Buttons for deciding the strength
radio_low = Radiobutton(root, text="Low", variable=var, value=1)
radio_low.grid(row=3, column=0, sticky='E',padx=10,pady=10)
radio_middle = Radiobutton(root, text="Medium", variable=var, value=0)
radio_middle.grid(row=3, column=1, sticky='E',padx=10,pady=10)
radio_strong = Radiobutton(root, text="Strong", variable=var, value=3)
radio_strong.grid(row=3, column=2, sticky='E',padx=10,pady=10)

# Combo Box for length of your password
lengthchoice = Combobox(root, textvariable=var1)
lengthchoice['values'] = (8, 9, 10, 11, 12, 13, 14, 15, 16,
				17, 18, 19, 20)
lengthchoice.current(0)
lengthchoice.bind('<<ComboboxSelected>>')
lengthchoice.grid(column=1, row=1)

# start the GUI
root.mainloop()
