from tkinter import *
from tkinter import messagebox
import mysql.connector
from tkinter.ttk import Treeview


mydb = mysql.connector.connect(
    host="localhost",
    user="Ahmad",
    password="6090",
    database="db_project")
my_cursor = mydb.cursor()

root = Tk()
root.geometry("900x600")
root.title("Hotel Management")
root.config(bg="#fef6e4")


def clear_frame():
    for widget in root.winfo_children():
        if widget.winfo_class() != "Menu":
            widget.destroy()


def styled_button1(root, text, command):
    btn = Button(root, text=text, bg="Tan", fg="white", height=2, width=18, font=("Arial", 12, "bold"),
                 relief=RAISED, bd=5, command=command, cursor="hand2")
    btn.bind("<Enter>", lambda e: btn.config(bg="#f5deb3"))
    btn.bind("<Leave>", lambda e: btn.config(bg="Tan"))
    btn.pack(side=LEFT, padx=10, pady=10)
    return btn


def styled_button2(root, text, command):
    btn = Button(root, text=text, bg="#1ABC9C", fg="White", height=2, width=18, font=("Arial", 12, "bold"),
                 relief=RAISED, bd=5, command=command, cursor="hand2")
    btn.bind("<Enter>", lambda e: btn.config(bg="aquamarine"))
    btn.bind("<Leave>", lambda e: btn.config(bg="#1ABC9C"))
    btn.pack(padx=10, pady=10)
    return btn


def show_hotel_details():
    clear_frame()
    Label(root, text="🏨 Hotel Details", bg="#fef6e4", font=("Garamond", 24, "bold"), pady=10).pack()
    form_frame = Frame(root, bg="#fef6e4", padx=20, pady=20)
    form_frame.pack()
    my_cursor.execute("SELECT hotel_name, location, contact_number FROM hotels WHERE hotel_code = 'HTL001'")
    result = my_cursor.fetchone()

    if result:
        fields = {
            "Hotel Name": result[0],
            "Location": result[1],
            "Contact": result[2]
        }
    else:
        messagebox.showerror("Error", "No hotel found with hotel_code 'HTL001'")
        return

    entry_widgets = {}

    for idx, (label_text, default_val) in enumerate(fields.items()):
        Label(form_frame, text=label_text, font=("Arial", 12, "bold"), bg="#fef6e4").grid(row=idx, column=0,
                                                                                              sticky="w", pady=5)
        entry = Entry(form_frame, font=("Arial", 12), width=30)
        entry.grid(row=idx, column=1, pady=5)
        entry.insert(0, default_val)
        entry_widgets[label_text] = entry

        # Update and Back Buttons
    btn_frame = Frame(root, bg="#fef6e4")
    btn_frame.pack(pady=20)

    def update_details():
        updated_info = {label: entry.get() for label, entry in entry_widgets.items()}

        hotel_name = updated_info["Hotel Name"]
        location = updated_info["Location"]
        contact = updated_info["Contact"]

        sql = """UPDATE hotels SET hotel_name = %s, location = %s, contact_number = %s WHERE hotel_code = 'HTL001'"""
        values = (hotel_name, location, contact)
        my_cursor.execute(sql, values)
        mydb.commit()
        messagebox.showinfo("Updated",
                            f"Hotel details updated:\n\n" + "\n".join(f"{k}: {v}" for k, v in updated_info.items()))
    styled_button2(btn_frame, "Update Details", update_details)

    btn = Button(root, text="Back to Main", bg="#8b5e3c", fg="White", height=2, width=18, font=("Arial", 12, "bold"),
                 relief=RAISED, bd=5, command=main, cursor="hand2")
    btn.pack(padx=10, pady=10)


def show_room_details():
    clear_frame()


    def deluxe():
        clear_frame()
        my_cursor.execute("SELECT * FROM rooms WHERE id = 1 and hotel='HTL001'")
        result = my_cursor.fetchone()

        if not result:
            print("No Deluxe rooms found.")
            return

        container = Frame(root, bg="#ecf0f1", bd=10, relief="ridge")
        container.pack(padx=30, pady=30, expand=True)

        Label(container, text="Room Information", font=("Helvetica", 24, "bold"),
              fg="#34495e", bg="#ecf0f1").pack(pady=(0, 20))

        form_frame = Frame(container, bg="#ecf0f1")
        form_frame.pack()

        # Hotel ID (read-only)
        Label(form_frame, text="Hotel ID", font=("Calibri", 16, "bold"),
              fg="#2980b9", bg="#ecf0f1").grid(row=1, column=0, padx=15, pady=12, sticky="w")
        hotel_id_var = StringVar(value=result[1])
        Entry(form_frame, textvariable=hotel_id_var, font=("Calibri", 16), width=30,
              state='readonly', relief="groove", bd=3,
              highlightthickness=2, highlightbackground="#bdc3c7").grid(row=1, column=1, padx=15, pady=12)

        # Editable fields
        def add_field(label_text, row, var):
            Label(form_frame, text=label_text, font=("Calibri", 16, "bold"),
                  fg="#2980b9", bg="#ecf0f1").grid(row=row, column=0, padx=15, pady=12, sticky="w")
            Entry(form_frame, textvariable=var, font=("Calibri", 16), width=30,
                  relief="groove", bd=3,
                  highlightthickness=2, highlightbackground="#bdc3c7").grid(row=row, column=1, padx=15, pady=12)

        room_type_var = StringVar(value=result[2])
        person_var = StringVar(value=result[4])
        bed_var = StringVar(value=result[5])
        facility_var = StringVar(value=result[6])
        price_var = StringVar(value=result[7])

        add_field("Room Type", 2, room_type_var)
        add_field("Person", 3, person_var)
        add_field("Bed", 4, bed_var)
        add_field("Facility", 5, facility_var)
        add_field("Price per day", 6, price_var)

        # Update Function
        def update_room_data():
            try:
                sql = """UPDATE rooms SET room_type = %s, person = %s,
                 bed = %s, facilities = %s, price = %s WHERE id = 1"""
                value = [room_type_var.get(), person_var.get(), bed_var.get(), facility_var.get(),
                          price_var.get()]
                my_cursor.execute(sql, value)
                mydb.commit()

                messagebox.showinfo("Success", "Room details updated successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update room details: {e}")

        # Update Button
        Button(root, text="Update", command=update_room_data,
               bg="#27ae60", fg="white", font=("Arial", 12, "bold"),
               height=2, width=18, relief=RAISED, bd=5, cursor="hand2").pack(pady=10)

        # Back Button
        Button(root, text="Back", bg="#8b5e3c", fg="White", height=2, width=18,
               font=("Arial", 12, "bold"),
               relief=RAISED, bd=5, command=show_room_details, cursor="hand2").pack(padx=10, pady=10)

    def executive():
        clear_frame()
        my_cursor.execute("SELECT * FROM rooms WHERE id = 2 and hotel='HTL001'")
        result = my_cursor.fetchone()

        if not result:
            print("No Deluxe rooms found.")
            return

        container = Frame(root, bg="#ecf0f1", bd=10, relief="ridge")
        container.pack(padx=30, pady=30, expand=True)

        Label(container, text="Room Information", font=("Helvetica", 24, "bold"),
              fg="#34495e", bg="#ecf0f1").pack(pady=(0, 20))

        form_frame = Frame(container, bg="#ecf0f1")
        form_frame.pack()

        # Hotel ID (read-only)
        Label(form_frame, text="Hotel ID", font=("Calibri", 16, "bold"),
              fg="#2980b9", bg="#ecf0f1").grid(row=1, column=0, padx=15, pady=12, sticky="w")
        hotel_id_var = StringVar(value=result[1])
        Entry(form_frame, textvariable=hotel_id_var, font=("Calibri", 16), width=30,
              state='readonly', relief="groove", bd=3,
              highlightthickness=2, highlightbackground="#bdc3c7").grid(row=1, column=1, padx=15, pady=12)

        # Editable fields
        def add_field(label_text, row, var):
            Label(form_frame, text=label_text, font=("Calibri", 16, "bold"),
                  fg="#2980b9", bg="#ecf0f1").grid(row=row, column=0, padx=15, pady=12, sticky="w")
            Entry(form_frame, textvariable=var, font=("Calibri", 16), width=30,
                  relief="groove", bd=3,
                  highlightthickness=2, highlightbackground="#bdc3c7").grid(row=row, column=1, padx=15, pady=12)

        room_type_var = StringVar(value=result[2])
        person_var = StringVar(value=result[4])
        bed_var = StringVar(value=result[5])
        facility_var = StringVar(value=result[6])
        price_var = StringVar(value=result[7])

        add_field("Room Type", 2, room_type_var)
        add_field("Person", 3, person_var)
        add_field("Bed", 4, bed_var)
        add_field("Facility", 5, facility_var)
        add_field("Price per day", 6, price_var)

        def update_room_data():
            try:
                sql = """UPDATE rooms SET room_type = %s, person = %s,
                 bed = %s, facilities = %s, price = %s WHERE id = 2"""
                value = [room_type_var.get(), person_var.get(), bed_var.get(), facility_var.get(),
                          price_var.get()]
                my_cursor.execute(sql, value)
                mydb.commit()

                messagebox.showinfo("Success", "Room details updated successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update room details: {e}")

        styled_button2(root, "Update", update_room_data)
        btn = Button(root, text="Back", bg="#8b5e3c", fg="White", height=2, width=18,
                     font=("Arial", 12, "bold"),
                     relief=RAISED, bd=5, command=show_room_details, cursor="hand2")
        btn.pack(padx=10, pady=10)

    def standard():
        clear_frame()
        my_cursor.execute("SELECT * FROM rooms WHERE id = 3 and hotel='HTL001'")
        result = my_cursor.fetchone()

        if not result:
            print("No Deluxe rooms found.")
            return

        container = Frame(root, bg="#ecf0f1", bd=10, relief="ridge")
        container.pack(padx=30, pady=30, expand=True)

        Label(container, text="Room Information", font=("Helvetica", 24, "bold"),
              fg="#34495e", bg="#ecf0f1").pack(pady=(0, 20))

        form_frame = Frame(container, bg="#ecf0f1")
        form_frame.pack()

        # Hotel ID (read-only)
        Label(form_frame, text="Hotel ID", font=("Calibri", 16, "bold"),
              fg="#2980b9", bg="#ecf0f1").grid(row=1, column=0, padx=15, pady=12, sticky="w")
        hotel_id_var = StringVar(value=result[1])
        Entry(form_frame, textvariable=hotel_id_var, font=("Calibri", 16), width=30,
              state='readonly', relief="groove", bd=3,
              highlightthickness=2, highlightbackground="#bdc3c7").grid(row=1, column=1, padx=15, pady=12)

        # Editable fields
        def add_field(label_text, row, var):
            Label(form_frame, text=label_text, font=("Calibri", 16, "bold"),
                  fg="#2980b9", bg="#ecf0f1").grid(row=row, column=0, padx=15, pady=12, sticky="w")
            Entry(form_frame, textvariable=var, font=("Calibri", 16), width=30,
                  relief="groove", bd=3,
                  highlightthickness=2, highlightbackground="#bdc3c7").grid(row=row, column=1, padx=15, pady=12)

        room_type_var = StringVar(value=result[2])
        person_var = StringVar(value=result[4])
        bed_var = StringVar(value=result[5])
        facility_var = StringVar(value=result[6])
        price_var = StringVar(value=result[7])

        add_field("Room Type", 2, room_type_var)
        add_field("Person", 3, person_var)
        add_field("Bed", 4, bed_var)
        add_field("Facility", 5, facility_var)
        add_field("Price per day", 6, price_var)

        def update_room_data():
            try:
                sql = """UPDATE rooms SET room_type = %s, person = %s,
                 bed = %s, facilities = %s, price = %s WHERE id = 3"""
                value = [room_type_var.get(), person_var.get(), bed_var.get(), facility_var.get(),
                          price_var.get()]
                my_cursor.execute(sql, value)
                mydb.commit()

                messagebox.showinfo("Success", "Room details updated successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update room details: {e}")

        styled_button2(root, "Update", update_room_data)
        btn = Button(root, text="Back", bg="#8b5e3c", fg="White", height=2, width=18,
                     font=("Arial", 12, "bold"),
                     relief=RAISED, bd=5, command=show_room_details, cursor="hand2")
        btn.pack(padx=10, pady=10)

    def family():
        clear_frame()
        my_cursor.execute("SELECT * FROM rooms WHERE id = 4 and hotel='HTL001'")
        result = my_cursor.fetchone()

        if not result:
            print("No Deluxe rooms found.")
            return

        container = Frame(root, bg="#ecf0f1", bd=10, relief="ridge")
        container.pack(padx=30, pady=30, expand=True)

        Label(container, text="Room Information", font=("Helvetica", 24, "bold"),
              fg="#34495e", bg="#ecf0f1").pack(pady=(0, 20))

        form_frame = Frame(container, bg="#ecf0f1")
        form_frame.pack()

        Label(form_frame, text="Hotel ID", font=("Calibri", 16, "bold"),
              fg="#2980b9", bg="#ecf0f1").grid(row=1, column=0, padx=15, pady=12, sticky="w")
        hotel_id_var = StringVar(value=result[1])
        Entry(form_frame, textvariable=hotel_id_var, font=("Calibri", 16), width=30,
              state='readonly', relief="groove", bd=3,
              highlightthickness=2, highlightbackground="#bdc3c7").grid(row=1, column=1, padx=15, pady=12)

        def add_field(label_text, row, var):
            Label(form_frame, text=label_text, font=("Calibri", 16, "bold"),
                  fg="#2980b9", bg="#ecf0f1").grid(row=row, column=0, padx=15, pady=12, sticky="w")
            Entry(form_frame, textvariable=var, font=("Calibri", 16), width=30,
                  relief="groove", bd=3,
                  highlightthickness=2, highlightbackground="#bdc3c7").grid(row=row, column=1, padx=15, pady=12)

        room_type_var = StringVar(value=result[2])
        person_var = StringVar(value=result[4])
        bed_var = StringVar(value=result[5])
        facility_var = StringVar(value=result[6])
        price_var = StringVar(value=result[7])

        add_field("Room Type", 2, room_type_var)
        add_field("Person", 3, person_var)
        add_field("Bed", 4, bed_var)
        add_field("Facility", 5, facility_var)
        add_field("Price per day", 6, price_var)

        def update_room_data():
            try:
                sql = """UPDATE rooms SET room_type = %s, person = %s,
                 bed = %s, facilities = %s, price = %s WHERE id = 4"""
                value = [room_type_var.get(), person_var.get(), bed_var.get(), facility_var.get(),
                          price_var.get()]
                my_cursor.execute(sql, value)
                mydb.commit()

                messagebox.showinfo("Success", "Room details updated successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update room details: {e}")

        styled_button2(root, "Update", update_room_data)
        btn = Button(root, text="Back", bg="#8b5e3c", fg="White", height=2, width=18,
                     font=("Arial", 12, "bold"),
                     relief=RAISED, bd=5, command=show_room_details, cursor="hand2")
        btn.pack(padx=10, pady=10)

    Label(root, text="🛏️ Room Details", bg="#fef6e4", font=("Garamond", 24, "bold"), pady=10).pack()
    styled_button2(root, "Deluxe Suite", deluxe)
    styled_button2(root, "Executive Room", executive)
    styled_button2(root, "Standard Room", standard)
    styled_button2(root, "Family Room", family)
    btn = Button(root, text="Back to Main", bg="#8b5e3c", fg="White", height=2, width=18,
                 font=("Arial", 12, "bold"),
                 relief=RAISED, bd=5, command=main, cursor="hand2")
    btn.pack(padx=10, pady=10)


def show_booking_details():
    clear_frame()

    title_bar = Label(root, text="🏨 Bookings", font=("Arial", 24, "bold"),
                      bg="#deb887", fg="black", pady=10)
    title_bar.pack(fill=X)

    frame = Frame(root)
    frame.pack(padx=10, pady=10)

    h_scrollbar = Scrollbar(frame, orient=HORIZONTAL)
    h_scrollbar.pack(side=BOTTOM, fill=X)

    listbox = Listbox(frame, width=130, height=20, font=("Courier New", 10),
                      xscrollcommand=h_scrollbar.set)
    listbox.pack()

    h_scrollbar.config(command=listbox.xview)

    def fetch_bookings_from_db():
        my_cursor.execute("SELECT * FROM booking WHERE hotel_code='HTL001'")
        rows = my_cursor.fetchall()
        bookings = []
        for row in rows:
            bookings.append({'id': row[0], 'hotel_code': row[1], 'customer_name': row[2],
                             'date': row[3].strftime("%Y-%m-%d"), 'time': row[4],
                             'checkout_date': row[5].strftime("%Y-%m-%d"), 'checkout_time': row[6], 'room_type': row[7],
                             'num_rooms': row[8]})
        return bookings

    def update_list():
        listbox.delete(0, END)
        all_bookings = fetch_bookings_from_db()
        if not all_bookings:
            listbox.insert(END, "No bookings found.")
            return

        for booking in all_bookings:
            display_text = (f"Name: {booking['customer_name']:<20} | "
                            f"Check-in: {booking['date']} {booking['time']} | "
                            f"Check-out: {booking['checkout_date']} {booking['checkout_time']} | "
                            f"Room Type: {booking['room_type']:<10} | "
                            f"Rooms: {booking['num_rooms']}")
            listbox.insert(END, display_text)

    update_list()

    btn = Button(root, text="Back to Main", bg="#8b5e3c", fg="White", height=2, width=18,
                 font=("Arial", 12, "bold"),
                 relief=RAISED, bd=5, command=main, cursor="hand2")
    btn.pack(padx=10, pady=10)


def check_inn():
    clear_frame()

    def check():
        cust_id = var.get()
        query = """SELECT cus_name, room_type, no_of_rooms, additional_service,check_in_date, check_out_date, price
                FROM booking WHERE booking_id = %s AND hotel_code = 'HTL001'"""
        my_cursor.execute(query, (cust_id,))
        results = my_cursor.fetchall()

        # Clear previous output
        output_box.delete("1.0", END)

        if results:
            for row in results:
                name, room_type, no_of_rooms, services, check_in, check_out, bill = row
                output_box.insert(END, f"Customer Name : {name}\n")
                output_box.insert(END, f"Room Type     : {room_type}\n")
                output_box.insert(END, f"No. of Rooms  : {no_of_rooms}\n")
                output_box.insert(END, f"Services      : {services}\n")
                output_box.insert(END, f"Check-in Date : {check_in}\n")
                output_box.insert(END, f"Check-out Date: {check_out}\n")
                output_box.insert(END, f"Total bill    : {bill}\n")
                output_box.insert(END, "-" * 50 + "\n")
        else:
            output_box.insert(END, "No booking found for this ID.\n")

    # Container
    container = Frame(root, bg="#ecf0f1", bd=10, relief="ridge")
    container.pack(padx=30, pady=30, expand=True)

    header = Label(container, text="Check-INN", font=("Helvetica", 24, "bold"),
                   fg="#34495e", bg="#ecf0f1")
    header.pack(pady=(0, 20))

    form_frame = Frame(container, bg="#ecf0f1")
    form_frame.pack()

    lbl = Label(form_frame, text="Booking Id:", font=("Calibri", 16, "bold"),
                fg="#2980b9", bg="#ecf0f1")
    lbl.grid(row=1, column=0, padx=15, pady=12, sticky="w")

    var = StringVar()
    entry = Entry(form_frame, textvariable=var, font=("Calibri", 16), width=30,
                  relief="groove", bd=3, highlightthickness=2, highlightbackground="#bdc3c7")
    entry.grid(row=1, column=1, padx=15, pady=12)

    check_btn = Button(form_frame, text="Check", font=("Calibri", 14, "bold"),
                       bg="#27ae60", fg="white", relief="raised", bd=3,
                       padx=30, pady=5, command=check, cursor="hand2")
    check_btn.grid(row=3, column=0, columnspan=2, pady=20)

    # Output text box
    global output_box
    output_box = Text(container, height=10, width=60, font=("Courier New", 12), bd=2, relief="sunken")
    output_box.pack(pady=10)

    btn = Button(container, text="Back to Main", bg="#8b5e3c", fg="White", height=2, width=18,
                 font=("Arial", 12, "bold"),
                 relief=RAISED, bd=5, command=main, cursor="hand2")
    btn.pack(padx=10, pady=10)


def available_rooms():
    clear_frame()

    Label(root, text="📋 Available Rooms", bg="#fef6e4", font=("Garamond", 24, "bold"), pady=10).pack()

    form_frame = Frame(root, bg="#fef6e4", padx=20, pady=20)
    form_frame.pack()

    query = """SELECT room_type, SUM(available) AS total_available FROM rooms WHERE hotel = 'HTL001' GROUP BY
     room_type"""
    my_cursor.execute(query)
    results = my_cursor.fetchall()

    if not results:
        Label(form_frame, text="No data found for hotel 'HTL001'.", font=("Arial", 12, "bold"), bg="#fef6e4").pack()
        return

    entry_dict = {}

    for i, (room_type, total_available) in enumerate(results):
        Label(form_frame, text=f"{room_type}", font=("Arial", 12, "bold"), bg="#fef6e4").grid(row=i, column=0, sticky="w", padx=10, pady=5)
        entry = Entry(form_frame, font=("Arial", 12), width=10)
        entry.insert(0, str(total_available))
        entry.grid(row=i, column=1, pady=5)
        entry_dict[room_type] = entry

    def update_availability():
        for room_type, entry in entry_dict.items():
            try:
                new_available = int(entry.get())
                sql = """UPDATE rooms SET available = %s WHERE room_type = %s AND hotel = 'HTL001'"""
                my_cursor.execute(sql, (new_available, room_type))
            except ValueError:
                messagebox.showerror("Invalid Input", f"Please enter a valid number for {room_type}")
                return
        mydb.commit()
        messagebox.showinfo("Updated", "Availability updated successfully.")

    btn_frame = Frame(root, bg="#fef6e4")
    btn_frame.pack(pady=20)
    styled_button2(btn_frame, "Update Availability", update_availability)

    Button(root, text="Back to Main", bg="#8b5e3c", fg="White", height=2, width=18,
           font=("Arial", 12, "bold"), relief=RAISED, bd=5, command=main, cursor="hand2").pack(pady=10)


def employee_details():
    clear_frame()

    def add_employee_gui():
        clear_frame()
        Label(root, text="➕ Add New Employee", font=("Garamond", 22, "bold"),
              bg="#fef6e4", fg="#2C3E50").pack(pady=20)

        form = Frame(root, bg="#fef6e4")
        form.pack(pady=10)

        Label(form, text="Name:", font=("Arial", 12, "bold"), bg="#fef6e4", fg="#2C3E50").grid(row=0, column=0,
                                                                                    sticky="w", padx=10, pady=5)
        name_entry = Entry(form, font=("Arial", 12), bg="#ffffff", width=30)
        name_entry.grid(row=0, column=1, pady=5)

        Label(form, text="Department:", font=("Arial", 12, "bold"), bg="#fef6e4", fg="#2C3E50").grid(row=1, column=0,
                                                                                    sticky="w", padx=10, pady=5)
        department_var = StringVar(value="Department")
        dept_menu = OptionMenu(form, department_var, "Department", "Security", "Housekeeping", "Reception", "Finance")
        dept_menu.config(font=("Arial", 11), bg="#ffffff", width=30)
        dept_menu.grid(row=1, column=1, pady=5)

        Label(form, text="Designation:", font=("Arial", 12, "bold"), bg="#fef6e4", fg="#2C3E50").grid(row=2, column=0,
                                                                                     sticky="w", padx=10, pady=5)
        design_entry = Entry(form, font=("Arial", 12), bg="#ffffff", width=30)
        design_entry.grid(row=2, column=1, pady=5)

        Label(form, text="Salary:", font=("Arial", 12, "bold"), bg="#fef6e4", fg="#2C3E50").grid(row=3, column=0,
                                                                                    sticky="w", padx=10, pady=5)
        salary_entry = Entry(form, font=("Arial", 12), bg="#ffffff", width=30)
        salary_entry.grid(row=3, column=1, pady=5)

        def add_employee():
            name = name_entry.get().strip()
            dept = department_var.get().strip()
            design = design_entry.get().strip()
            salary = salary_entry.get().strip()
            if not all([name, dept, design, salary]):
                messagebox.showerror("Error", "All fields are required.")
                return
            if not salary.isdigit():
                messagebox.showerror("Error", "Salary must be numeric.")
                return
            try:
                my_cursor.execute(
                    "INSERT INTO emp(name, department, job_rank, salary) VALUES (%s, %s, %s, %s)",
                    (name, dept, design, salary))
                mydb.commit()
                messagebox.showinfo("Success", "Employee added successfully!")
                name_entry.delete(0, END)
                design_entry.delete(0, END)
                salary_entry.delete(0, END)
            except Exception as e:
                messagebox.showerror("Error", f"Error: {e}")

        btn_frame = Frame(root, bg="#fef6e4")
        btn_frame.pack(pady=20)
        styled_button2(btn_frame, "Submit", add_employee)
        Button(root, text="Back", bg="#8b5e3c", fg="White", height=2, width=18,
               font=("Arial", 12, "bold"), relief=RAISED, bd=5, command=employee_details, cursor="hand2").pack(pady=10)

    def remove_employee_gui():
        clear_frame()
        Label(root, text="❌ Remove Employee", font=("Garamond", 22, "bold"),
              bg="#fef6e4", fg="#2C3E50").pack(pady=20)

        Label(root, text="Enter Employee ID:", font=("Arial", 12, "bold"), bg="#fef6e4", fg="#2C3E50").pack()
        emp_id_entry = Entry(root, font=("Arial", 12), bg="#ffffff", width=30)
        emp_id_entry.pack()

        def remove():
            emp_id = emp_id_entry.get()
            if emp_id.isdigit():
                try:
                    my_cursor.execute("DELETE FROM emp WHERE emp_id = %s", (emp_id,))
                    mydb.commit()
                    if my_cursor.rowcount > 0:
                        messagebox.showinfo("Success", f"Employee ID {emp_id} removed.")
                    else:
                        messagebox.showwarning("Not Found", "No such employee.")
                except Exception as e:
                    messagebox.showerror("Error", str(e))
            else:
                messagebox.showwarning("Invalid", "ID must be numeric.")

        btn_frame = Frame(root, bg="#fef6e4")
        btn_frame.pack(pady=20)
        styled_button2(btn_frame, "Remove", remove)
        Button(root, text="Back", bg="#8b5e3c", fg="White", height=2, width=18,
               font=("Arial", 12, "bold"), relief=RAISED, bd=5, command=employee_details, cursor="hand2").pack(pady=10)

    def search():
        clear_frame()
        Label(root, text="🔍 Search Employee", font=("Garamond", 22, "bold"),
              bg="#fef6e4", fg="#2C3E50").pack(pady=20)

        Label(root, text="Enter Employee ID:", font=("Arial", 12, "bold"), bg="#fef6e4", fg="#2C3E50").pack()
        search_entry = Entry(root, font=("Arial", 12), bg="#ffffff", width=30)
        search_entry.pack()

        result_text = StringVar()
        Label(root, textvariable=result_text, bg="#fef6e4", font=("Arial", 12)).pack(pady=10)

        def search_emp():
            query = search_entry.get().strip()
            if not query.isdigit():
                messagebox.showwarning("Invalid Input", "Enter a numeric ID.")
                return
            my_cursor.execute("SELECT * FROM emp WHERE emp_id = %s", (query,))
            result = my_cursor.fetchone()
            if result:
                result_text.set(
                    f"ID: {result[0]}\nName: {result[1]}\nDepartment: {result[2]}\nDesignation: {result[3]}\nSalary: {result[4]}")
            else:
                result_text.set("No employee found.")

        btn_frame = Frame(root, bg="#fef6e4")
        btn_frame.pack(pady=20)
        styled_button2(btn_frame, "Search", search_emp)
        Button(root, text="Back", bg="#8b5e3c", fg="White", height=2, width=18,
               font=("Arial", 12, "bold"), relief=RAISED, bd=5, command=employee_details, cursor="hand2").pack(pady=10)

    def create_dashboard():
        clear_frame()
        Label(root, text="📊 Employee Dashboard", font=("Garamond", 22, "bold"), bg="#fef6e4", fg="#2C3E50").pack(
            pady=20)

        # Fetch employee details with ID
        my_cursor.execute("SELECT emp_id, name, department, job_rank, salary FROM emp ORDER BY department, name")
        employees = my_cursor.fetchall()

        my_cursor.execute("SELECT department, AVG(salary) FROM emp GROUP BY department")
        avg_salaries = dict(my_cursor.fetchall())

        frame = Frame(root)
        frame.pack(fill=BOTH, expand=True, padx=10)

        tree = Treeview(frame, columns=("ID", "Name", "Department", "Position", "Salary"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Name", text="Name")
        tree.heading("Department", text="Department")
        tree.heading("Position", text="Position")
        tree.heading("Salary", text="Salary")

        tree.column("ID", anchor=CENTER, width=50)
        tree.column("Name", anchor=W, width=150)
        tree.column("Department", anchor=W, width=120)
        tree.column("Position", anchor=W, width=150)
        tree.column("Salary", anchor=E, width=100)

        tree.pack(fill=BOTH, expand=True)

        for emp in employees:
            tree.insert("", END, values=emp)

        tree.insert("", END, values=("", "", "", "", ""))
        tree.insert("", END, values=("📌 Average Salary by Department", "", "", "", ""))

        for dept, avg in avg_salaries.items():
            tree.insert("", END, values=(f"Dept: {dept}", f"Avg: {avg:.2f}", "", "", ""))

        Button(root, text="Back", bg="#8b5e3c", fg="White", height=2, width=18,
               font=("Arial", 12, "bold"), relief=RAISED, bd=5, command=employee_details, cursor="hand2").pack(pady=10)

    Label(root, text=" Employees Management", bg="#fef6e4", font=("Garamond", 24, "bold"), pady=10).pack()
    btn_frame = Frame(root, bg="#fef6e4")
    btn_frame.pack(pady=10)
    styled_button2(btn_frame, "➕ Add Employee", add_employee_gui)
    styled_button2(btn_frame, "❌ Remove Employee", remove_employee_gui)
    btn_frame1 = Frame(root, bg="#fef6e4")
    btn_frame1.pack(pady=10)
    styled_button2(btn_frame1, "🔍 Search Employee", search)
    styled_button2(btn_frame1, "📊 Employee Dashboard", create_dashboard)
    Button(root, text="Back to Main", bg="#8b5e3c", fg="White", height=2, width=18,
           font=("Arial", 12, "bold"), relief=RAISED, bd=5, command=main, cursor="hand2").pack(pady=10)


def main():
    clear_frame()
    title_bar = Label(root, text="🏨 Hotel Management System", font=("Garamond", 24, "bold"),
                      bg="BurlyWood", anchor="center")
    title_bar.pack(fill=X, pady=15)
    Label(root, text="PC Hotel", bg="#fef6e4", font=("Garamond", 24, "bold"), pady=10).pack()
    frame1 = Frame(root, bg="#fef6e4")
    photo = PhotoImage(file=r"C:\Users\Ahmad\Downloads\a.png", height=250, width=350)
    pic = Label(frame1, image=photo, bg="#fef6e4")
    pic.image = photo
    pic.pack()
    frame1.pack()
    f1 = Frame(root, bg="#fef6e4")
    f1.pack()
    styled_button1(f1, "Hotel Details", show_hotel_details)
    styled_button1(f1, "Available Rooms", available_rooms)
    styled_button1(f1, "Room Details", show_room_details)
    f2 = Frame(root, bg="#fef6e4")
    f2.pack()
    styled_button1(f2, "Check - Inn", check_inn)
    styled_button1(f2, "Booking Details", show_booking_details)
    styled_button1(f2, "Employees", employee_details)
    Button(root, text="Exit", bg="red", fg="white", height=2, width=10, font="Arial 12 bold", command=root.quit,
           relief="raised", bd=4, cursor="hand2").pack(pady=10)


main()
root.mainloop()
