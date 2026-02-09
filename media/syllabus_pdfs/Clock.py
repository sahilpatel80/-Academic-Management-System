import time
from tkinter import Label,Tk

root = Tk()
root.title("Digital Clock")
root.geometry("400x200")
root.resizable(False,False)

Label = Label(root,font=("Arial",50),bg="black",fg="white")
Label.pack(pady=20)

def update_clock():
    current_time =time.strftime("%H:%M:%S")
    Label.config(text=current_time)
    Label.after(1000,update_clock)

update_clock()

root.mainloop()