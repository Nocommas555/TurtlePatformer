from tkinter import *

root = Tk()
root.resizable(False, False)
root.title("Fee Fie Foe Fum")

frame=Frame(root, width=1600, height=800)
frame.pack()

button1 = Button(frame, text="Mercy!")
button1.place(relx=0.5, rely=0.1, anchor=CENTER, height=30, width=100)

button2 = Button(frame, text="Justice!")
button2.place(relx=0.5, rely=0.2, anchor=CENTER, height=30, width=100)

text1 = Label(text="Verdict:")
text1.place(relx=0.5, rely=0.3, anchor=CENTER)

tbox1 = Text(frame)
tbox1.place(relx=0.5, rely=0.4, anchor=CENTER, height=30, width=200)

root.mainloop()