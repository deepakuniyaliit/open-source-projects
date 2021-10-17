from tkinter import *

bmi=Tk()

# Title
bmi.title("BMI Calculator")
#geometry
bmi.geometry("300x300")
bmi.minsize(300,300)
bmi.maxsize(300,300)
#photo
photo = PhotoImage(file="1.png")
varun_label = Label(image=photo)
varun_label.pack()
#heading
heading = Label(text="ENTER WIEGHT AND HEIGHT")
heading.pack()


bmi.mainloop()

