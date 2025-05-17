from tkinter import *
from tkinter import ttk, messagebox
import datetime

class PharmacyInventorySystem:
    def __init__(self, root):
        self.root = root
        self.root.geometry("800x600")
        self.root.title("SalbaFirS: A FIFO-based Pharmaceutical Inventory System")
        self.root.config(bg="white")

        # =======Title=======
        title = Label(self.root, text="SalbaFirS Pharmaceutical Inventory System", font=("Arial", 24, "bold"), bg="#722F37", fg="white")
        title.pack(fill=X)

        self.inventory = []

        # =======Search Frame=======
        self.var_search = StringVar()
        search_frame = Frame(self.root, bg="white")
        search_frame.pack(pady=10, fill=X)

        lbl_search = Label(search_frame, text="Search Product:", font=("Arial", 12), bg="white")
        lbl_search.pack(side=LEFT, padx=10)

        txt_search = Entry(search_frame, textvariable=self.var_search, font=("Arial", 12), bg="#FAEDEA")
        txt_search.pack(side=LEFT, padx=5)

        btn_search = Button(search_frame, text="Search", command=self.search, font=("Arial", 12), bg="#722F37", fg="white")
        btn_search.pack(side=LEFT)

        btn_show_all = Button(search_frame, text="Show All", command=self.show_all, font=("Arial", 12), bg="#722F37", fg="white")
        btn_show_all.pack(side=LEFT)

        btn_sort = Button(search_frame, text="Sort by Expiry Date", command=self.sort_by_expiry, font=("Arial", 12), bg="#722F37", fg="white")
        btn_sort.pack(side=LEFT)

        #=======Product Table Frame=======
        self.product_table_frame = Frame(self.root)
        self.product_table_frame.pack(pady=10, fill=BOTH, expand=1)

        self.product_table = ttk.Treeview(self.product_table_frame, columns=("pid", "itemname", "price", "qty", "expiry_date", "date"), show="headings")
        self.product_table.pack(side=LEFT, fill=BOTH, expand=1)

        for col in ("pid", "itemname", "price", "qty", "expiry_date", "date"):
            self.product_table.heading(col, text=col.capitalize())

        self.product_table.bind("<ButtonRelease-1>", self.get_data)

        #=======Action Frame=======
        self.action_frame = Frame(self.root, bd=4, relief=RIDGE, bg="white")
        self.action_frame.pack(pady=10, fill=X)

        self.var_pid = StringVar()
        self.var_pname = StringVar()
        self.var_price = StringVar()
        self.var_qty = StringVar()
        self.var_expiry_date = StringVar()

        #=======Labels and Entries=======
        fields = [
            ("PID:", self.var_pid, 'readonly'),
            ("Item Name:", self.var_pname),
            ("Price:", self.var_price),
            ("Quantity:", self.var_qty),
            ("Expiry Date (YYYY-MM-DD):", self.var_expiry_date),
        ]

        for idx, (label, var, *state) in enumerate(fields):
            lbl = Label(self.action_frame, text=label, bg="white")
            lbl.grid(row=idx, column=0, padx=10, pady=10, sticky="e")
            entry = Entry(self.action_frame, textvariable=var, state=state[0] if state else 'normal')
            entry.grid(row=idx, column=1, padx=10, pady=10, sticky="w")

        #=======Action Buttons=======
        button_frame = Frame(self.action_frame, bg="white")
        button_frame.grid(row=0, column=2, rowspan=5, padx=10, pady=10, sticky="w")

        Button(button_frame, text="Add", command=self.add_product, bg="#722F37", fg="white", font=("Arial", 12)).grid(row=0, column=0, pady=10)
        Button(button_frame, text="Update", command=self.update_product, bg="#722F37", fg="white", font=("Arial", 12)).grid(row=1, column=0, pady=10)
        Button(button_frame, text="Clear", command=self.clear_fields, bg="#722F37", fg="white", font=("Arial", 12)).grid(row=2, column=0, pady=10)
        Button(button_frame, text="Dispense", command=self.delete_product, bg="#722F37", fg="white", font=("Arial", 12)).grid(row=3, column=0, pady=10)

        self.action_frame.grid_columnconfigure(0, weight=1)
        self.action_frame.grid_columnconfigure(1, weight=3)
        self.action_frame.grid_columnconfigure(2, weight=1)

        self.show_all()

    def show_all(self):
        self.product_table.delete(*self.product_table.get_children())
        for row in self.inventory:
            self.product_table.insert('', END, values=(row['pid'], row['itemname'], row['price'], row['qty'], row['expiry_date'], row['date']))

    def search(self):
        search_term = self.var_search.get().lower()
        filtered_inventory = [row for row in self.inventory if search_term in row['itemname'].lower()]
        self.product_table.delete(*self.product_table.get_children())
        for row in filtered_inventory:
            self.product_table.insert('', END, values=(row['pid'], row['itemname'], row['price'], row['qty'], row['expiry_date'], row['date']))

    def sort_by_expiry(self):
        self.inventory.sort(key=lambda x: x['expiry_date'])
        self.show_all()

    def get_data(self, event):
        selected_item = self.product_table.focus()
        item_data = self.product_table.item(selected_item)
        row = item_data['values']
        if row:
            self.var_pid.set(row[0])
            self.var_pname.set(row[1])
            self.var_price.set(row[2])
            self.var_qty.set(row[3])
            self.var_expiry_date.set(row[4])

    def validate_inputs(self):
        itemname = self.var_pname.get().strip()
        quantity = self.var_qty.get().strip()
        expiry_date = self.var_expiry_date.get().strip()

        if not itemname:
            messagebox.showerror("Input Error", "❌ Medicine name cannot be empty.")
            return False
        if itemname.isdigit():
            messagebox.showerror("Input Error", "❌ Medicine name should not be only numbers.")
            return False

        if not quantity.isdigit() or int(quantity) <= 0:
            messagebox.showerror("Input Error", "❌ Quantity must be a positive integer.")
            return False

        try:
            expiry_date_obj = datetime.datetime.strptime(expiry_date, "%Y-%m-%d").date()
            if expiry_date_obj < datetime.date.today():
                messagebox.showerror("Input Error", "❌ Expiry date cannot be in the past.")
                return False
        except ValueError:
            messagebox.showerror("Input Error", "❌ Invalid date format. Please use YYYY-MM-DD.")
            return False

        return True

    def add_product(self):
        if not self.validate_inputs():
            return

        pid = len(self.inventory) + 1  
        itemname = self.var_pname.get()
        price = self.var_price.get()
        qty = self.var_qty.get()
        expiry_date = self.var_expiry_date.get()
        date = self.get_current_date()

        self.inventory.append({'pid': pid, 'itemname': itemname, 'price': price, 'qty': qty, 'expiry_date': expiry_date, 'date': date})

        self.show_all()
        self.clear_fields()

    def update_product(self):
        if not self.validate_inputs():
            return

        pid = int(self.var_pid.get())
        for row in self.inventory:
            if row['pid'] == pid:
                row['itemname'] = self.var_pname.get()
                row['price'] = self.var_price.get()
                row['qty'] = self.var_qty.get()
                row['expiry_date'] = self.var_expiry_date.get()
                row['date'] = self.get_current_date()
                break
        self.show_all()
        self.clear_fields()

    def delete_product(self):
        pid = int(self.var_pid.get())
        self.inventory = [row for row in self.inventory if row['pid'] != pid]
        self.show_all()
        self.clear_fields()

    def get_current_date(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def clear_fields(self):
        self.var_pid.set('')
        self.var_pname.set('')
        self.var_price.set('')
        self.var_qty.set('')
        self.var_expiry_date.set('')
        self.var_search.set('')

if __name__ == "__main__":
    root = Tk()
    app = PharmacyInventorySystem(root)
    root.mainloop()
