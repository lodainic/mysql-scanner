from tkinter import *
from tkinter import messagebox
import traceback
from app import DatabaseManip


def enter_db():
    try:
        global db
        db = DatabaseManip(ent1f1.get(), ent2f1.get(), ent3f1.get(), ent4f1.get())
        db.connect_db()
        f1.place_forget()
        f2.place(relx=0.5, rely=0.5, anchor="c")
    except:
        messagebox.showerror(title="ERROR", message="UNKNOWN")


def leave_db():
    db.disconnect_db()
    f2.place_forget()
    f1.place(relx=0.5, rely=0.5, anchor="c")


def norm_nullbt():
    f2.place_forget()
    f3.pack()

    global lbl
    lbl = "nullbt"

    gd, bd = db.norm_nullbt()

    gd_str = []
    for x in gd:
        gd_str.append(str(x[0]).upper())
    listbox1f3.delete(0, "end")
    gd_str = list(dict.fromkeys(gd_str))
    for i in range(len(gd_str)):
        listbox1f3.insert(i, gd_str[i])

    bd_str = []
    for x in bd:
        bd_str.append(str(x[0]).upper())
    listbox2f3.delete(0, "end")
    bd_str = list(dict.fromkeys(bd_str))
    for i in range(len(bd_str)):
        listbox2f3.insert(i, bd_str[i])

    bd_str = []
    for x in bd:
        bd_str.append(str(x[0]).upper() + "." + str(x[1]) + ", NULL:" + str(x[2]))
    listbox3f3.configure(state=NORMAL)
    listbox3f3.delete(0, "end")
    for i in range(len(bd_str)):
        listbox3f3.insert(i, bd_str[i])


def norm_prim_keys():
    f2.place_forget()
    f4.pack()

    global lbl
    lbl = "pk"

    pk_res, _ = db.norm_pr_key()

    pk_res_str0 = []
    pk_res_str1 = []
    pk_res_str2 = []
    for x in pk_res:
        if x[1] == 0:
            pk_res_str0.append(str(x[0]).upper())
        elif x[1] == 1:
            pk_res_str1.append(str(x[0]).upper())
        elif x[1] >= 2:
            pk_res_str2.append(str(x[0]).upper())
    listbox1f4.delete(0, "end")
    for i in range(len(pk_res_str0)):
        listbox1f4.insert(i, pk_res_str0[i])
    listbox1f4.select_set(0, END)

    listbox2f4.delete(0, "end")
    for i in range(len(pk_res_str1)):
        listbox2f4.insert(i, pk_res_str1[i])
    listbox2f4.select_set(0, END)

    listbox3f4.delete(0, "end")
    for i in range(len(pk_res_str2)):
        listbox3f4.insert(i, pk_res_str2[i])
    listbox3f4.select_set(0, END)


def norm_domain():
    f2.place_forget()
    f5.pack()

    global lbl
    lbl = "domain"

    db.drop_fk_constr(True)

    charr, numr, dater = db.norm_domain()

    charr_str = []
    for x in charr:
        charr_str.append(
            str(x[0]).upper()
            + "."
            + str(x[1])
            + ", "
            + str(x[2])
            + "->"
            + str(x[4])
            + ", max_len:"
            + str(x[3])
        )
    listbox1f5.delete(0, "end")
    for i in range(len(charr_str)):
        listbox1f5.insert(i, charr_str[i])

    dater_str = []
    for x in dater:
        dater_str.append(
            str(x[0]).upper()
            + "."
            + str(x[1])
            + " "
            + str(x[2])
            + " - "
            + str(x[3])
            + "->"
            + str(x[4])
            + " - "
            + str(x[5])
        )
    listbox2f5.delete(0, "end")
    for i in range(len(dater_str)):
        listbox2f5.insert(i, dater_str[i])

    numr_str = []
    for x in numr:
        numr_str.append(
            str(x[0]).upper()
            + "."
            + str(x[1])
            + ", "
            + str(x[4])
            + ", "
            + str(x[2])
            + "->"
            + str(x[3])
        )
    listbox3f5.delete(0, "end")
    for i in range(len(numr_str)):
        listbox3f5.insert(i, numr_str[i])


def save():
    if lbl == "nullbt":
        b_sel = listbox3f3.curselection()
        if listbox3f3.index(END) > 0 and len(b_sel) == 0:
            messagebox.showerror(title="ERROR", message="No selected items.")
        else:
            try:
                db.save_norm_nullbt(b_sel)
            except:
                traceback.print_exc()
                messagebox.showerror(title="ERROR", message="Could not apply changes.")
            else:
                messagebox.showinfo(title="SUCCES", message="Changes applied!")
                cancel()
    if lbl == "pk":
        try:
            db.save_norm_pr_key()
        except:
            traceback.print_exc()
            messagebox.showerror(title="ERROR", message="Could not apply changes.")
        else:
            messagebox.showinfo(title="SUCCES", message="Changes applied!")
            cancel()
    if lbl == "domain":
        try:
            db.save_norm_domain()
            db.drop_fk_constr(False)
        except:
            traceback.print_exc()
            messagebox.showerror(title="ERROR", message="Could not apply changes.")
        else:
            messagebox.showinfo(title="SUCCES", message="Changes applied")
            cancel()


def cancel():
    f3.pack_forget()
    f4.pack_forget()
    f5.pack_forget()
    f2.place(relx=0.5, rely=0.5, anchor="c")


if __name__ == "__main__":

    root = Tk()
    root.title("MySQL DB Scanner")
    root.geometry("800x900")
    root.resizable(0, 0)

    # connect frame
    f1 = Frame(root)
    f1.place(relx=0.5, rely=0.5, anchor="c")
    lbl1f1 = Label(f1, text="Enter Your Credentials", pady=10)
    lbl2f1 = Label(f1, text="Host: ", pady=5)
    lbl3f1 = Label(f1, text="User: ", pady=5)
    lbl4f1 = Label(f1, text="Password: ", pady=5)
    lbl5f1 = Label(f1, text="DB Name: ", pady=5)
    ent1f1 = Entry(f1)
    ent2f1 = Entry(f1)
    ent3f1 = Entry(f1, show="*")
    ent4f1 = Entry(f1)
    btn1f1 = Button(f1, text="Connect", command=enter_db, padx=20)

    lbl1f1.grid(row=0, column=1)
    lbl2f1.grid(row=1, column=0)
    lbl3f1.grid(row=2, column=0)
    lbl4f1.grid(row=3, column=0)
    lbl5f1.grid(row=4, column=0)
    ent1f1.grid(row=1, column=1)
    ent2f1.grid(row=2, column=1)
    ent3f1.grid(row=3, column=1)
    ent4f1.grid(row=4, column=1)
    btn1f1.grid(row=5, column=1)

    # home frame
    f2 = Frame(root)
    lbl1f2 = Label(
        f2, text="Normalization: ", font=("Helvetica", "18", "bold"), pady=30
    )
    btn1f2 = Button(
        f2, text="Nullability Constraint", command=norm_nullbt, pady=10, width=20
    )
    btn2f2 = Button(
        f2, text="Primary Key Constraints", command=norm_prim_keys, pady=10, width=20
    )
    btn3f2 = Button(
        f2, text="Domain Constraints", command=norm_domain, pady=10, width=20
    )
    btn4f2 = Button(f2, text="Disconnect", command=leave_db)

    lbl1f2.pack()
    btn1f2.pack()
    btn2f2.pack()
    btn3f2.pack()
    btn4f2.pack()

    # norm nullbt frame
    f3 = Frame(root)
    lbl1f3 = Label(
        f3,
        text="Nullability Constraint Normalization",
        font=("Helvetica", "18", "bold"),
        pady=10,
    )
    lbl2f3 = Label(f3, text="Good Tables")
    lbl3f3 = Label(f3, text="Bad Tables")
    lbl4f3 = Label(f3, text="Available changes")
    listbox1f3 = Listbox(
        f3,
        width=40,
        height=10,
        yscrollcommand=True,
        xscrollcommand=True,
        exportselection=False,
        selectbackground="white",
    )
    listbox2f3 = Listbox(
        f3,
        width=40,
        height=10,
        yscrollcommand=True,
        xscrollcommand=True,
        exportselection=False,
        selectbackground="white",
    )
    listbox3f3 = Listbox(
        f3,
        width=40,
        height=10,
        yscrollcommand=True,
        xscrollcommand=True,
        selectmode=MULTIPLE,
        exportselection=False,
        selectbackground="green",
    )
    btn1f3 = Button(f3, text="Make Changes", command=save, width=10)
    btn2f3 = Button(f3, text="Cancel", command=cancel, width=10)

    lbl1f3.pack()
    lbl2f3.pack()
    listbox1f3.pack()
    lbl3f3.pack()
    listbox2f3.pack()
    lbl4f3.pack()
    listbox3f3.pack()
    btn1f3.pack()
    btn2f3.pack()

    # norm PK frame
    f4 = Frame(root)
    lbl1f4 = Label(
        f4,
        text="Primary Key Constraint Normalization",
        font=("Helvetica", "18", "bold"),
        pady=10,
    )
    lbl2f4 = Label(f4, text="Tabels with no Primary Key:")
    lbl3f4 = Label(f4, text="Tables with non-numeric Primary Key:")
    lbl4f4 = Label(f4, text="Tables with multiple Primary Keys:")
    listbox1f4 = Listbox(
        f4,
        width=40,
        height=10,
        yscrollcommand=True,
        xscrollcommand=True,
        exportselection=False,
        selectbackground="white",
    )
    listbox2f4 = Listbox(
        f4,
        width=40,
        height=10,
        yscrollcommand=True,
        xscrollcommand=True,
        exportselection=False,
        selectbackground="white",
    )
    listbox3f4 = Listbox(
        f4,
        width=40,
        height=10,
        yscrollcommand=True,
        xscrollcommand=True,
        exportselection=False,
        selectbackground="white",
    )
    btn1f4 = Button(f4, text="Make Changes", command=save, width=10)
    btn2f4 = Button(f4, text="Cancel", command=cancel, width=10)

    lbl1f4.pack()
    lbl2f4.pack()
    listbox1f4.pack()
    lbl3f4.pack()
    listbox2f4.pack()
    lbl4f4.pack()
    listbox3f4.pack()
    btn1f4.pack()
    btn2f4.pack()

    # norm domain frame
    f5 = Frame(root)
    lbl1f5 = Label(
        f5,
        text="Domain Constraint Normalization",
        font=("Helvetica", "18", "bold"),
        pady=10,
    )
    lbl2f5 = Label(f5, text="CHAR")
    lbl3f5 = Label(f5, text="DATE")
    lbl4f5 = Label(f5, text="NUM")
    listbox1f5 = Listbox(
        f5,
        width=40,
        height=10,
        yscrollcommand=True,
        xscrollcommand=True,
        exportselection=False,
        selectbackground="white",
    )
    listbox2f5 = Listbox(
        f5,
        width=40,
        height=10,
        yscrollcommand=True,
        xscrollcommand=True,
        exportselection=False,
        selectbackground="white",
    )
    listbox3f5 = Listbox(
        f5,
        width=40,
        height=10,
        yscrollcommand=True,
        xscrollcommand=True,
        exportselection=False,
        selectbackground="white",
    )
    btn1f5 = Button(f5, text="Make Changes", command=save, width=10)
    btn2f5 = Button(f5, text="Cancel", command=cancel, width=10)

    lbl1f5.pack()
    lbl2f5.pack()
    listbox1f5.pack()
    lbl3f5.pack()
    listbox2f5.pack()
    lbl4f5.pack()
    listbox3f5.pack()
    btn1f5.pack()
    btn2f5.pack()

    root.mainloop()
