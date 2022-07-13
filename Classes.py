import tkinter as tk


root = tk.Tk()
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)
timer1 = 0
timer2 = 0
frame1 = tk.Frame(root)
frame2 = tk.Frame(root)
frame2.grid(row=0, column=0, sticky='nsew')
frame1.grid(row=0, column=0, sticky='nsew')
frame1.tkraise()

current_active_frame = frame1

lbl1 = tk.Label(frame1, text='Active Counter at: 0')
lbl2 = tk.Label(frame2, text='Active Counter at: 0')
lbl1.grid(row=0, column=0, sticky='nsew')
lbl2.grid(row=0, column=0, sticky='nsew')
tk.Button(frame1, text='Switch to frame 2', command=lambda: raise_frame(frame2)).grid(row=1, column=0, sticky='nsew')
tk.Button(frame2, text='Switch to frame 1', command=lambda: raise_frame(frame1)).grid(row=1, column=0, sticky='nsew')


def raise_frame(frame):
    global current_active_frame
    frame.tkraise()
    current_active_frame = frame


def update_while_active():
    global timer1, timer2
    if current_active_frame == frame1:
        print('frame1')
        timer1 += 1
        lbl1.config(text='Active Counter at: {}'.format(timer1))
    if current_active_frame == frame2:
        print('frame2')
        timer2 += 1
        lbl2.config(text='Active Counter at: {}'.format(timer2))
    root.after(1000, update_while_active)

update_while_active()
root.mainloop()