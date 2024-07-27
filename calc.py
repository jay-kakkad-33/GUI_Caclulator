import sqlite3
import psutil
import tkinter as tk
from tkinter import RIGHT, messagebox
from tkinter.constants import ANCHOR, INSIDE, NO
from tkinter.font import BOLD

con=sqlite3.connect("calc.db")
c=con.cursor()
con.execute("CREATE TABLE IF NOT EXISTS expressions (EXP TEXT)")
calculator=tk.Tk()
calculator.iconbitmap("calculator.ico")
window_location="+450+100"
calculator.title("Calculator")
calculator.config(bg="#2f2f2f")
calculator.geometry(f"325x270{window_location}")
calculator.resizable(0,0)
exp=tk.StringVar()
display=tk.Entry(calculator,width=21,bg="#c1c1ff",bd=5,font=("Arial",20),textvariable=exp,justify=RIGHT)
display.grid(row=0,column=0,columnspan=5)
calculator.bind("<Button-1>",lambda event=None:calculator.focus_set())
#-------------menu-----------------
def show_history(event=None):
    try:
        history=con.execute("SELECT * FROM expressions")
        history_window=tk.Toplevel()
        history_window.title("History")
        history_window.config(bg="#000")
        history_window.geometry(f"325x250{window_location}")
        history_window.resizable(0,0)
        history_window.focus_force()
        history_list=tk.Listbox(history_window,width=60,height=20,bd=0,bg="#000",fg="#fff")
        history_list.pack()

        for i in history.fetchall():
            history_list.insert(0,i)
        def show_exp(event=None):
            try:
                exp.set(history_list.selection_get())
                history_window.destroy()
            except:
                messagebox.showerror("No selection","Please select a history to show")
        history_window.bind("<Double-Button-1>",show_exp)
        history_window.bind("<Return>",show_exp)
        history_window.bind("<Escape>",lambda event=None:history_window.destroy())
    except:
        messagebox.showerror("No History","No History Found")
def clr_history():
    con.execute("DROP TABLE expressions")
    con.commit()
menu=tk.Menu(calculator)
history_menu=tk.Menu(menu,tearoff=0)
history_menu.add_command(label="Show History",command=show_history,accelerator="Ctrl+H")
history_menu.add_command(label="Clear History",command=clr_history)
menu.add_cascade(label="History",menu=history_menu)
calculator.config(menu=menu)
# ---------function_for_results-------------
def calc(event=None):
    temp=exp.get()
    try:
        if "Root" in exp.get():
            try:
                n=int(exp.get()[exp.get().index("(")+1:exp.get().index(")")])
            except ValueError:
                n=int(float(exp.get()[exp.get().index("(")+1:exp.get().index(")")]))
            r=int(exp.get()[exp.get().index(")")+1:])
            for i in range(int(n/2)+1):
                if i**r==n:
                    exp.set(i)
                    con.execute("CREATE TABLE IF NOT EXISTS expressions (EXP TEXT)")
                    con.execute(f"""INSERT INTO expressions (EXP) VALUES ('={i}')""")
                    con.execute(f"""INSERT INTO expressions (EXP) VALUES ('{temp}')""")
                    con.commit()
        else:
            answer=eval(f"{exp.get()}")
            exp.set(eval(f"{exp.get()}"))
            con.execute("CREATE TABLE IF NOT EXISTS expressions (EXP TEXT)")
            con.execute(f"""INSERT INTO expressions (EXP) VALUES ('={answer}')""")
            con.execute(f"""INSERT INTO expressions (EXP) VALUES ('{temp}')""")
            con.commit()
    except SyntaxError:
        messagebox.showerror("Wrong Imput","Please enter a valid value")
def  perc(event=None):
    try:
        int(exp.get())
        exp.set(f"{int(exp.get())*0.01}*")
    except ValueError:
        el=["*","+","-"]
        try:
            for i in el:
                if(i in exp.get()):
                    a1=int(float(exp.get().split(i)[0]))
                    a2=int(float(exp.get().split(i)[1]))
                    if (i=="*"):
                        exp.set(f"{a1*0.01*a2}")
                    elif (i=="-"):
                        exp.set(f"{a1-((a1*0.01*a2))}")
                    elif (i=="+"):
                        exp.set(f"{a1+((a1*0.01*a2))}")
        except:
            messagebox.showerror("Oops","Wrong Input")
        
def add_ope(a):
    if(len(exp.get())==0):
        pass
    elif(len(exp.get())>15):
        messagebox.showerror("Out of Length","You exceeded Value Length")
    else:
        el=["*","+","-",".","/"]
        try:
            if(exp.get()[-1] in el):
                pass
            else:
                exp.set(f"{exp.get()}{a}")
        except:
            messagebox.showerror("Oops","Wrong Input")

def add_value(value):
    if(value=="0" and len(exp.get())==0):
        pass
    elif(len(exp.get())>15):
        messagebox.showerror("Out of Length","You exceeded Value Length")
    else:
        exp.set(f"{exp.get()}{value}")
        
# ----------------first_raw----------------
btn_9=tk.Button(text="9",width=7,height=2,bg="#aaf",bd=0,font=("Arial",8,BOLD),command=lambda:exp.set(f"{exp.get()}9"))
btn_9.grid(row=1,column=0,padx=2,pady=5)
btn_8=tk.Button(text="8",width=7,height=2,bg="#aaf",bd=0,font=("Arial",8,BOLD),command=lambda:exp.set(f"{exp.get()}8"))
btn_8.grid(row=1,column=1,padx=2,pady=5)
btn_7=tk.Button(text="7",width=7,height=2,bg="#aaf",bd=0,font=("Arial",8,BOLD),command=lambda:exp.set(f"{exp.get()}7"))
btn_7.grid(row=1,column=2,padx=2,pady=5)
btn_clear=tk.Button(calculator,text="C",width=7,height=2,bg="#aaf",bd=0,font=("Arial",8,BOLD),command=lambda:exp.set(""))
btn_clear.grid(row=1,column=3,padx=2,pady=5)
root_clear=tk.Button(calculator,text="\u221A",width=7,height=2,bg="#aaf",bd=0,font=("Arial Black",8,BOLD),command=lambda:exp.set(f"Root({exp.get()})"))
root_clear.grid(row=1,column=4,padx=2,pady=5)
# ----------------second_raw----------------
btn_6=tk.Button(text="6",width=7,height=2,bg="#aaf",bd=0,font=("Arial",8,BOLD),command=lambda:exp.set(f"{exp.get()}6"))
btn_6.grid(row=2,column=0,padx=2,pady=5)
btn_5=tk.Button(text="5",width=7,height=2,bg="#aaf",bd=0,font=("Arial",8,BOLD),command=lambda:exp.set(f"{exp.get()}5"))
btn_5.grid(row=2,column=1,padx=2,pady=5)
btn_4=tk.Button(text="4",width=7,height=2,bg="#aaf",bd=0,font=("Arial",8,BOLD),command=lambda:exp.set(f"{exp.get()}4"))
btn_4.grid(row=2,column=2,padx=2,pady=5)
btn_plus=tk.Button(calculator,text="+",width=4,height=1,bg="#aaf",bd=0,font=("Arial",14),command=lambda:exp.set(f"{exp.get()}+"))
btn_plus.grid(row=2,column=3,padx=2,pady=5)
btn_minus=tk.Button(calculator,text="-",width=4,height=1,bg="#aaf",bd=0,font=("Arial",14,BOLD),command=lambda:exp.set(f"{exp.get()}-"))
btn_minus.grid(row=2,column=4,padx=2,pady=5)
# ----------------third_raw----------------
btn_3=tk.Button(text="3",width=7,height=2,bg="#aaf",bd=0,font=("Arial",8,BOLD),command=lambda:exp.set(f"{exp.get()}3"))
btn_3.grid(row=3,column=0,padx=2,pady=5)
btn_2=tk.Button(text="2",width=7,height=2,bg="#aaf",bd=0,font=("Arial",8,BOLD),command=lambda:exp.set(f"{exp.get()}2"))
btn_2.grid(row=3,column=1,padx=2,pady=5)
btn_1=tk.Button(text="1",width=7,height=2,bg="#aaf",bd=0,font=("Arial",8,BOLD),command=lambda:exp.set(f"{exp.get()}1"))
btn_1.grid(row=3,column=2,padx=2,pady=5)
btn_into=tk.Button(calculator,text="X",width=7,height=2,bg="#aaf",bd=0,font=("Arial",8,BOLD),command=lambda:exp.set(f"{exp.get()}*"))
btn_into.grid(row=3,column=3,padx=2,pady=5)
btn_by=tk.Button(calculator,text="/",width=4,height=1,bg="#aaf",bd=0,font=("Arial",14,BOLD),command=lambda:exp.set(f"{exp.get()}"))
btn_by.grid(row=3,column=4,padx=2,pady=5)
# ----------------fourth_raw----------------
btn_0=tk.Button(text="0",width=7,height=2,bg="#aaf",bd=0,font=("Arial",8,BOLD),command=lambda:exp.set(f"{exp.get()}0"))
btn_0.grid(row=4,column=0,padx=2,pady=5)
btn_00=tk.Button(text="00",width=7,height=2,bg="#aaf",bd=0,font=("Arial",8,BOLD),command=lambda:exp.set(f"{exp.get()}00"))
btn_00.grid(row=4,column=1,padx=2,pady=5)
btn_dot=tk.Button(text=".",width=7,height=2,bg="#aaf",bd=0,font=("Arial",8,BOLD),command=lambda:exp.set(f"{exp.get()}."))
btn_dot.grid(row=4,column=2,padx=2,pady=5)
btn_percentage=tk.Button(text="%",width=7,height=2,bg="#aaf",bd=0,font=("Arial",8,BOLD),command=perc)
btn_percentage.grid(row=4,column=3,padx=2,pady=5)
btn_result=tk.Button(calculator,text="=",width=7,height=2,bg="#aaf",bd=0,font=("Arial",8,BOLD),command=calc)
btn_result.grid(row=4,column=4,padx=2,pady=5)
battery=psutil.sensors_battery().percent
battery_label=tk.Label(calculator,text=f"Battery : {battery}",bg="#2f2f2f")
battery_label.grid(row=5,column=0)
if (battery<50):
    battery_label.config(fg="#f55")
elif(battery>50 and battery<75):
    battery_label.config(fg="yellow")
else:
    battery_label.config(fg="#54ff25")
# --------binding_keys---------------------
keys_to_bind = {
    "1":lambda event=None:add_value("1"),
    "2":lambda event=None:add_value("2"),
    "3":lambda event=None:add_value("3"),
    "4":lambda event=None:add_value("4"),
    "5":lambda event=None:add_value("5"),
    "6":lambda event=None:add_value("6"),
    "7":lambda event=None:add_value("7"),
    "8":lambda event=None:add_value("8"),
    "9":lambda event=None:add_value("9"),
    "0":lambda event=None:add_value("0"),
    "+":lambda event=None:add_ope("+"),
    "-":lambda event=None:add_ope("-"),
    "*":lambda event=None:add_ope("*"),
    "/":lambda event=None:add_ope("/"),
    ".":lambda event=None:add_ope("."),
    "<Escape>":lambda event=None:exp.set(""),
    "%":perc,
    "<R>":lambda evevn=None:exp.set(f"Root({exp.get()})"),
    "<r>":lambda evevn=None:exp.set(f"Root({exp.get()})"),
    "<BackSpace>":lambda event=None:exp.set(exp.get()[:-1]),
    "<Return>":calc,
    "<Control-h>":show_history,
    "<Control-H>":show_history,
    }

for key,event in keys_to_bind.items():
    calculator.bind(key,event)
calculator.mainloop()
