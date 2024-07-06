from tkinter import *
from tkinter.messagebox import *
from tkinter.scrolledtext import *
from sqlite3 import *

root = Tk()
root.title("Order Management system by Shruti")
root.geometry("1200x800+50+50")
root.iconbitmap("oms.ico")
root.configure(bg="lightyellow")
f = ("Arial", 15, "bold")

lab_header = Label(root, text="Welcome to Cafe Coffee Day!!", font=("Impact", 20, "bold"), fg="Green")
lab_header.place(x=450, y=10)

def adminlogin():
    loginwindow = Toplevel()
    loginwindow.title("Admin Login")
    loginwindow.geometry("1200x800+50+50")
    loginwindow.iconbitmap("oms.ico")
    loginwindow.configure(bg="lightyellow")
    f = ("Arial", 15, "bold")

    lab_header = Label(loginwindow, text="Admin Login", fg="Green", bg="White", font=("Impact", 20, "bold"))
    lab_header.pack(pady=10)

    lab_username = Label(loginwindow, text="Username:", font=f)
    lab_username.pack(pady=10)
    ent_username = Entry(loginwindow, font=f)
    ent_username.pack(pady=10)

    lab_password = Label(loginwindow, text="Password:", font=f)
    lab_password.pack(pady=10)
    ent_password = Entry(loginwindow, show="*",font=f)
    ent_password.pack(pady=10)

    def validate_login():
        admin_username = "shruti"
        admin_password = "shruti@123"
        entered_username = ent_username.get()
        entered_password = ent_password.get()

        if entered_username == admin_username and entered_password == admin_password:
            loginwindow.destroy()
            open_adminwindow()
        else:
            showerror("Login Failed", "Invalid username or password")

    login_button = Button(loginwindow, text="Login", command=validate_login, font=f, bg="Green", fg="Black")
    login_button.pack(pady=10)


def open_adminwindow():
    aw = Toplevel()
    aw.title("Admin Panel")
    aw.geometry("1200x800+50+50")
    aw.iconbitmap("oms.ico")
    aw.configure(bg="lightyellow")
    f = ("Arial", 15, "bold")

    orders_text = ScrolledText(aw, font=f, width=60, height=15)
    orders_text.pack(pady=10)

    def display_orders():
        con = None
        try:
            con = connect("cafe.db")
            cursor = con.cursor()
            sql = "SELECT * FROM customers"
            cursor.execute(sql)
            data = cursor.fetchall()

            orders_text.delete(1.0, END)
            if not data:
                orders_text.insert(END, "No orders yet.")
            else:
                for order in data:
                    orders_text.insert(END, f"Name: {order[0]}\nContact: {order[1]}\nEmail: {order[2]}\nAddress: {order[3]}\nMenu: {order[4]}\n\n")

        except Exception as e:
            showerror("Error", e)
        finally:
            if con is not None:
                con.close()

    def cancel_order():
        selected_order = orders_text.get(SEL_FIRST, SEL_LAST).strip()

        if selected_order:
            con = None
            try:
                con = connect("cafe.db")
                cursor = con.cursor()

                name = selected_order.split("\n")[0].split(":")[1].strip()

                sql = f"DELETE FROM customers WHERE name = '{name}'"
                cursor.execute(sql)
                con.commit()

                showinfo("Success", "Order canceled successfully!")
                display_orders()

            except Exception as e:
                showerror("Error", e)
            finally:
                if con is not None:
                    con.close()
        else:
            showerror("No Order Selected", "Please select an order to cancel.")

    display_orders_btn = Button(aw, text="Display Orders", command=display_orders, font=f, bg="Green")
    display_orders_btn.pack(pady=10)

    cancel_order_btn = Button(aw, text="Cancel Selected Order", command=cancel_order, font=f, bg="Green")
    cancel_order_btn.pack(pady=10)


btn_admin = Button(root, text="Admin Login", font=f, fg="white", bg="orange", command=adminlogin)
btn_admin.place(x=1000, y=10)

lab_headline = Label(root, text="⦾ Kindly, Fill your details for placing the order", font=f, bg="lightyellow", fg="Black")
lab_headline.place(x=5, y=60)

lab_name = Label(root, text="Name", font=f, bg="lightyellow", fg="Red")
lab_name.place(x=5, y=100)

ent_name = Entry(root, font=f)
ent_name.place(x=190, y=100)

lab_contact = Label(root, text="Contact no.", font=f, bg="lightyellow", fg="Red")
lab_contact.place(x=5, y=150)

ent_contact = Entry(root, font=f)
ent_contact.place(x=190, y=150)

lab_emailaddress = Label(root, text="Email Address", font=f, bg="lightyellow", fg="Red")
lab_emailaddress.place(x=5, y=200)

ent_emailaddress = Entry(root, font=f)
ent_emailaddress.place(x=190, y=200)

lab_address = Label(root, text="Delivery Address", font=f, bg="lightyellow", fg="Red")
lab_address.place(x=5, y=250)

ent_address = ScrolledText(root, font=f, width=30, height=3)
ent_address.place(x=190, y=250)

tea, coffee, juice, soda, milkshake = IntVar(), IntVar(), IntVar(), IntVar(), IntVar()

lab_menu = Label(root, text="Select Menu", font=f, bg="lightyellow", fg="Red")
lab_menu.place(x=5, y=350)

cb_tea = Checkbutton(root, text="Tea", font=f, fg="Red", bg="lightyellow", variable=tea)
cb_coffee = Checkbutton(root, text="Coffee", font=f, fg="Red", bg="lightyellow", variable=coffee)
cb_juice = Checkbutton(root, text="Juice", font=f, fg="Red", bg="lightyellow", variable=juice)
cb_soda = Checkbutton(root, text="Soda", font=f, fg="Red", bg="lightyellow", variable=soda)
cb_milkshake = Checkbutton(root, text="MilkShake", font=f, fg="Red", bg="lightyellow", variable=milkshake)

cb_tea.place(x=200, y=350)
cb_coffee.place(x=400, y=350)
cb_juice.place(x=200, y=400)
cb_soda.place(x=400, y=400)
cb_milkshake.place(x=290, y=450)


def save():
    try:
        name = ent_name.get()
        if len(name.strip()) < 2 or not name.isalpha():
            showerror("Issues", "Invalid Name")
            return False
        phone = ent_contact.get()
        if not phone.isdigit() or len(phone) != 10:
            showerror("Issues", "Please enter valid 10 digit contact no.")
            return False
        email = ent_emailaddress.get()
        if not email or "@" not in email or "." not in email:
            showerror("Issues", "Please enter valid Email address")
            return False
        address = ent_address.get(1.0, END)
        if not address.strip():
            showerror("Issues", "Please enter address")
            return False

        menu = ""
        if tea.get() == 1:
            menu = menu + " Tea "
        if coffee.get() == 1:
            menu = menu + " Coffee "
        if juice.get() == 1:
            menu = menu + " Juice "
        if soda.get() == 1:
            menu = menu + " Soda "
        if milkshake.get() == 1:
            menu = menu + " MilkShake "
        con = None
        try:
            con = connect("cafe.db")
            cursor = con.cursor()
            sql = "insert into customers values('%s','%s','%s','%s','%s')"
            cursor.execute(sql % (name, phone, email, address, menu))
            con.commit()
            showinfo("Success", "Thank you for Placing order")
            ent_name.delete(0, END)
            ent_contact.delete(0, END)
            ent_emailaddress.delete(0, END)
            ent_address.delete(1.0, END)
            tea.set(0)
            coffee.set(0)
            juice.set(0)
            soda.set(0)
            milkshake.set(0)
            ent_name.focus()
        except Exception as e:
            con.rollback()
            showerror("Issues", e)
        finally:
            if con is not None:
                con.close()
    except Exception as e:
        showerror("Issues", e)


btn_order = Button(root, text="Place Order", font=f, bg="Orange", fg="Black", command=save)
btn_order.place(x=290, y=500)


def on_closing():
    if askyesno("Quit", "Do u really want to Quit ?"):
        root.destroy()


root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()