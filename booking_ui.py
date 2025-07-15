from tkinter import *
import datetime
from tkinter import messagebox
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="Ahmad",
    password="6090",
    database="db_project")
my_cursor = mydb.cursor()

root = Tk()
root.geometry("550x500")
root.title("Hotel Management")
root.config(bg="#f6f1eb")


def clear_frame():
    for widget in root.winfo_children():
        if widget.winfo_class() != "Menu":
            widget.destroy()


def styled_button1(root, text, command):
    btn = Button(root, text=text, bg="#8b5e3c", fg="white", height=2, width=18, font=("Arial", 12, "bold"),
                 relief=RAISED, bd=5, command=command, cursor="hand2")
    btn.bind("<Enter>", lambda e: btn.config(bg="Tan"))
    btn.bind("<Leave>", lambda e: btn.config(bg="#8b5e3c"))
    btn.pack(side=LEFT, padx=10, pady=10)
    return btn


def styled_button2(root, text, command):
    btn = Button(root, text=text, bg="#1ABC9C", fg="White", height=2, width=18, font=("Arial", 12, "bold"),
                 relief=RAISED, bd=5, command=command, cursor="hand2")
    btn.bind("<Enter>", lambda e: btn.config(bg="aquamarine"))
    btn.bind("<Leave>", lambda e: btn.config(bg="#1ABC9C"))
    btn.pack(padx=10, pady=10)
    return btn


def h_d():
    clear_frame()

    title_bar = Label(root, text="🏨 Explore Our Hotel Types", font=("Garamond", 26, "bold"),
                      bg="#deb887", fg="black", anchor="center", pady=10)
    title_bar.pack(fill=X)

    canvas = Canvas(root, bg="#f6f1eb", highlightthickness=0)
    scrollbar = Scrollbar(root, orient=VERTICAL, command=canvas.yview)
    scroll_frame = Frame(canvas, bg="#f6f1eb")

    scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side=LEFT, fill=BOTH, expand=True)
    scrollbar.pack(side=RIGHT, fill=Y)

    my_cursor.execute("SELECT * FROM hotels")
    hotel_list = []

    type_icons = {
        "5-Star": "🌟",
        "3-Star": "🏙️",
        "Resort": "🏖️",
        "Budget": "💰",
        "4-Star": "⛰️",
        "Eco": "🏕️",
        "Theme": "🎡"
    }

    type_descriptions = {
        "5-Star": "Luxury hotel.",
        "3-Star": "Affordable city-center hotel with basic amenities.",
        "Resort": "Relaxing resort with sea view and water sports.",
        "Budget": "Low-cost option with free Wi-Fi and breakfast.",
        "4-Star": "Scenic lodge with hiking trails and mountain views.",
        "Eco": "Environmentally friendly hotel in the forest.",
        "Theme": "Located next to a theme park with kid-friendly services."
    }

    for row in my_cursor:
        code, name_type, city, contact = row
        if "(" in name_type and ")" in name_type:
            name = name_type.split(" (")[0]
            htype = name_type.split(" (")[1].rstrip(")")
        else:
            name = name_type
            htype = "Unknown"

        icon = type_icons.get(htype, "🏨")
        desc = type_descriptions.get(htype, f"A nice hotel located in {city}.")

        hotel_list.append({
            "code": code,
            "icon": icon,
            "name": name,
            "type": htype,
            "desc": desc,
            "city": city,
            "contact": contact
        })

    for hotel in hotel_list:
        card = Frame(scroll_frame, bg="#fff8f0", bd=2, relief=GROOVE)
        card.pack(padx=20, pady=10, fill=X)

        l1 = Label(card, text=f"{hotel['icon']} {hotel['name']} ({hotel['type']})",
                   font=("Helvetica", 16, "bold"), bg="#fff8f0", fg="#5a3d2b")
        l1.pack(anchor="center", padx=10, pady=5)

        l2 = Label(card, text=f"Hotel Code: {hotel['code']}", font=("Arial", 12, "italic"),
                   bg="#fff8f0", fg="#333")
        l2.pack(anchor="center", padx=10)

        l3 = Label(card, text=hotel['desc'], font=("Arial", 12), bg="#fff8f0", anchor="w",
                   wraplength=450, justify=LEFT)
        l3.pack(anchor="center", padx=10, pady=5)

        l4 = Label(card, text=f"City: {hotel['city']} | Contact: {hotel['contact']}", font=("Arial", 12),
                   bg="#fff8f0", fg="#333")
        l4.pack(anchor="center", padx=10, pady=(0, 5))

        # Hover effect functions
        def on_enter(e, c=card, a=l1, b=l2, d=l3, e_=l4):
            for widget in (c, a, b, d, e_):
                widget.config(bg="#f0e6d6")

        def on_leave(e, c=card, a=l1, b=l2, d=l3, e_=l4):
            for widget in (c, a, b, d, e_):
                widget.config(bg="#fff8f0")

        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)

    f = Frame(scroll_frame, bg="#f6f1eb")
    f.pack(fill="x")
    Button(f, text="⏪ Back", bg="#8b5e3c", fg="white", font=("Arial", 12, "bold"), command=main, height=2, width=13,
           relief=RAISED, bd=4, cursor="hand2").pack(pady=15, anchor="center")


def r_b():
    clear_frame()
    canvas = Canvas(root, bg="#f6f1eb", highlightthickness=0)
    scrollbar = Scrollbar(root, orient=VERTICAL, command=canvas.yview)
    scroll_frame = Frame(canvas, bg="#f6f1eb")

    scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side=LEFT, fill=BOTH, expand=True)
    scrollbar.pack(side=RIGHT, fill=Y)

    room_data = {}
    my_cursor.execute("SELECT hotel, room_type, person, bed, facilities, price FROM rooms")
    for row in my_cursor:
        hotel, room_type, person, beds, facilities, price = row
        if hotel not in room_data:
            room_data[hotel] = {"rooms": {}}
        room_data[hotel]["rooms"][room_type] = {
            "capacity": person,
            "beds": beds,
            "features": facilities,
            "price": price
        }

    services = {
        "Breakfast": 500,
        "WiFi": 500,
        "AC": 2000
    }

    Label(scroll_frame, text="📖 Room Booking", font=("Garamond", 24, "bold"), bg="#deb887", fg="black", pady=10).pack(fill=X)

    frame = Frame(scroll_frame, bg="#f6f1eb", padx=20, pady=20)
    frame.pack(pady=10)

    Label(frame, text="Select Hotel Code:", font=("Arial", 12), bg="#f6f1eb").grid(row=0, column=0, sticky=W)
    selected_code = StringVar()
    code_menu = OptionMenu(frame, selected_code, *room_data.keys())
    code_menu.grid(row=0, column=1, pady=5, sticky=W)

    Label(frame, text="Customer Name:", font=("Arial", 12), bg="#f6f1eb").grid(row=1, column=0, sticky=W)
    customer_name = Entry(frame, font=("Arial", 12))
    customer_name.grid(row=1, column=1, pady=5, sticky=W)

    Label(frame, text="Check-In Date (YYYY-MM-DD):", font=("Arial", 12), bg="#f6f1eb").grid(row=2, column=0, sticky=W)
    date_entry = Entry(frame, font=("Arial", 12))
    date_entry.insert(0, datetime.datetime.now().strftime("%Y-%m-%d"))
    date_entry.grid(row=2, column=1, pady=5, sticky=W)

    Label(frame, text="Check-In Time (HH:MM):", font=("Arial", 12), bg="#f6f1eb").grid(row=3, column=0, sticky=W)
    time_entry = Entry(frame, font=("Arial", 12))
    time_entry.insert(0, datetime.datetime.now().strftime("%I:%M"))
    time_entry.grid(row=3, column=1, pady=5, sticky=W)

    am_pm = StringVar(value="AM")
    ampm_menu = OptionMenu(frame, am_pm, "AM", "PM")
    ampm_menu.grid(row=3, column=2, pady=5, sticky=W)

    Label(frame, text="Check-Out Date (YYYY-MM-DD):", font=("Arial", 12), bg="#f6f1eb").grid(row=4, column=0, sticky=W)
    check_out_date_entry = Entry(frame, font=("Arial", 12))
    check_out_date_entry.insert(0, datetime.datetime.now().strftime("%Y-%m-%d"))
    check_out_date_entry.grid(row=4, column=1, pady=5, sticky=W)

    Label(frame, text="Check-Out Time (HH:MM):", font=("Arial", 12), bg="#f6f1eb").grid(row=5, column=0, sticky=W)
    check_out_time_entry = Entry(frame, font=("Arial", 12))
    check_out_time_entry.insert(0, "12:00")
    check_out_time_entry.grid(row=5, column=1, pady=5, sticky=W)

    check_out_am_pm = StringVar(value="PM")
    check_out_ampm_menu = OptionMenu(frame, check_out_am_pm, "AM", "PM")
    check_out_ampm_menu.grid(row=5, column=2, pady=5, sticky=W)

    Label(frame, text="Room Type:", font=("Arial", 12), bg="#f6f1eb").grid(row=6, column=0, sticky=W)
    selected_room = StringVar(value="-- Select Room --")
    room_menu = OptionMenu(frame, selected_room, "-- Select Room --")
    room_menu.grid(row=6, column=1, pady=5, sticky=W)

    Label(frame, text="No. of Rooms:", font=("Arial", 12), bg="#f6f1eb").grid(row=7, column=0, sticky=W)
    num_rooms = Entry(frame, font=("Arial", 12))
    num_rooms.grid(row=7, column=1, pady=5, sticky=W)

    Label(frame, text="Additional Services:", font=("Arial", 12, "bold"), bg="#f6f1eb").grid(row=8, column=0, sticky=W, pady=(10, 2))
    service_vars = {}
    for i, (srv, price) in enumerate(services.items()):
        var = IntVar()
        chk = Checkbutton(frame, text=f"{srv} (+Rs {price})", variable=var, bg="#f6f1eb", font=("Arial", 11))
        chk.grid(row=9 + i, column=0, columnspan=2, sticky=W)
        service_vars[srv] = var

    room_details = Label(frame, text="", font=("Arial", 11), bg="#f6f1eb", fg="blue", justify=LEFT)
    room_details.grid(row=12, column=0, columnspan=3, sticky=W)

    price_label = Label(frame, text="Total Price: Rs 0", font=("Arial", 12, "bold"), bg="#f6f1eb", fg="darkgreen")
    price_label.grid(row=13, column=0, columnspan=3, pady=(10, 5), sticky=W)

    result_label = Label(frame, text="", font=("Arial", 12, "bold"), fg="green", bg="#f6f1eb")
    result_label.grid(row=14, column=0, columnspan=3, pady=10, sticky=W)

    def calculate_price():
        code = selected_code.get()
        room = selected_room.get()
        try:
            count = int(num_rooms.get())
        except:
            count = 0
        if code and room in room_data.get(code, {}).get("rooms", {}):
            price = room_data[code]["rooms"][room]["price"] * count
            for srv, var in service_vars.items():
                if var.get():
                    price += services[srv] * count
            price_label.config(text=f"Total Price: Rs {price}")
        else:
            price_label.config(text="Total Price: Rs 0")

    def set_room_selection(room_type):
        selected_room.set(room_type)
        update_room_details()
        calculate_price()

    def update_rooms(*args):
        code = selected_code.get()
        room_menu['menu'].delete(0, 'end')
        if code in room_data:
            rooms = list(room_data[code]["rooms"].keys())
            if rooms:
                for room in rooms:
                    room_menu['menu'].add_command(label=room, command=lambda r=room: set_room_selection(r))
                set_room_selection(rooms[0])
            else:
                selected_room.set("-- Select Room --")
                room_details.config(text="")
        else:
            selected_room.set("-- Select Room --")
            room_details.config(text="")

    def update_room_details(*args):
        code = selected_code.get()
        room = selected_room.get()
        if code and room in room_data[code]["rooms"]:
            info = room_data[code]["rooms"][room]
            details = (f"👥 Capacity: {info['capacity']}\n"
                       f"🛏️ Beds: {info['beds']}\n"
                       f"🛎️ Features: {info['features']}\n"
                       f"💰 Price per Room: Rs {info['price']}")
            room_details.config(text=details)
        else:
            room_details.config(text="")

    def confirm_booking():
        code = selected_code.get()
        name = customer_name.get().strip()
        check_in_date = date_entry.get().strip()
        check_in_time = time_entry.get().strip()
        check_in_meridian = am_pm.get()
        check_out_date = check_out_date_entry.get().strip()
        check_out_time = check_out_time_entry.get().strip()
        check_out_meridian = check_out_am_pm.get()
        room = selected_room.get()
        try:
            count = int(num_rooms.get())
        except:
            messagebox.showerror("Invalid Input", "Number of rooms must be a valid integer.")
            return

        if not all([code, name, check_in_date, check_in_time, check_out_date, check_out_time, room]) or count <= 0:
            messagebox.showerror("Missing Info", "Please complete all fields with valid data.")
            return

        try:
            check_in_dt = datetime.datetime.strptime(f"{check_in_date} {check_in_time} {check_in_meridian}", "%Y-%m-%d %I:%M %p")
            check_out_dt = datetime.datetime.strptime(f"{check_out_date} {check_out_time} {check_out_meridian}", "%Y-%m-%d %I:%M %p")

            if check_in_dt < datetime.datetime.now():
                messagebox.showerror("Invalid Time", "Check-in cannot be in the past.")
                return
            if check_out_dt <= check_in_dt:
                messagebox.showerror("Invalid Time", "Check-out must be after check-in.")
                return
        except Exception:
            messagebox.showerror("Invalid Format", "Please check date/time format.")
            return

        room_price = room_data[code]["rooms"][room]["price"]
        total = room_price * count

        selected_services = []
        for srv, var in service_vars.items():
            if var.get():
                total += services[srv] * count
                selected_services.append(srv)
        additional_services = ", ".join(selected_services) if selected_services else "None"

        try:
            insert_sql = ("INSERT INTO booking (hotel_code, cus_name, check_in_date, check_in_time, check_out_date,"
                          " check_out_time, room_type, no_of_rooms, additional_service, price) "
                          "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
            my_cursor.execute(insert_sql, (code, name,check_in_date, f"{check_in_time} {check_in_meridian}",
                                           check_out_date, f"{check_out_time} {check_out_meridian}",
                                           room, count, additional_services, total))
            mydb.commit()
            result_label.config(text=f"Booking confirmed! Total price: Rs {total}")
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to insert booking: {e}")

    # Traces and Events
    selected_code.trace('w', update_rooms)
    selected_room.trace('w', update_room_details)
    num_rooms.bind("<KeyRelease>", lambda e: calculate_price())
    for var in service_vars.values():
        var.trace("w", lambda *args: calculate_price())

    f2 = Frame(scroll_frame, bg="#f6f1eb")
    f2.pack()
    Button(f2, text="Confirm Booking", font=("Arial", 14, "bold"), bg="green", fg="white",
           command=confirm_booking).grid(row=15, column=0)
    Button(f2, text="⏪ Back", font=("Arial", 14, "bold"), bg="#8b5e3c", fg="white", command=main).grid(row=16, column=0, pady=15)


def show_bookings():
    clear_frame()
    title_bar = Label(root, text="🏨 Bookings", font=("Arial", 24, "bold"),
                      bg="#deb887", fg="black", pady=10)
    title_bar.pack(fill=X)

    filter_var = StringVar(value="all")
    frame_filter = Frame(root)
    frame_filter.pack()

    Radiobutton(frame_filter, text="Previous Bookings", variable=filter_var, value="previous").pack(side=LEFT, padx=5)
    Radiobutton(frame_filter, text="Today's Bookings", variable=filter_var, value="today").pack(side=LEFT, padx=5)
    Radiobutton(frame_filter, text="Future Bookings", variable=filter_var, value="future").pack(side=LEFT, padx=5)
    Radiobutton(frame_filter, text="All Bookings", variable=filter_var, value="all").pack(side=LEFT, padx=5)

    listbox_frame = Frame(root)
    listbox_frame.pack(pady=10)

    v_scroll_right = Scrollbar(listbox_frame, orient=VERTICAL)
    v_scroll_right.pack(side=RIGHT, fill=Y)

    h_scroll_bottom = Scrollbar(listbox_frame, orient=HORIZONTAL)
    h_scroll_bottom.pack(side=BOTTOM, fill=X)

    listbox = Listbox(listbox_frame, width=60, height=17, font=("Courier New", 10),
                      yscrollcommand=lambda *args:[v_scroll_right.set(*args)],
                      xscrollcommand=lambda *args: [h_scroll_bottom.set(*args)], xscroll=True)

    listbox.pack(side=LEFT, fill=BOTH, expand=True)
    v_scroll_right.config(command=listbox.yview)
    h_scroll_bottom.config(command=listbox.xview)

    def fetch_bookings_from_db():
        my_cursor.execute("SELECT * FROM booking")
        rows = my_cursor.fetchall()
        bookings = []
        for row in rows:
            bookings.append({
                'id': row[0],
                'hotel_code': row[1],
                'customer_name': row[2],
                'date': row[3].strftime("%Y-%m-%d"),
                'time': row[4],
                'checkout_date': row[5].strftime("%Y-%m-%d"),
                'checkout_time': row[6],
                'room_type': row[7],
                'num_rooms': row[8],
                'services': [s.strip() for s in row[9].split(",")] if row[9] else [],
                'price': row[10]
            })
        return bookings

    def update_list():
        listbox.delete(0, END)
        today = datetime.date.today()
        all_bookings = fetch_bookings_from_db()

        filtered = []
        for b in all_bookings:
            b_date = datetime.datetime.strptime(b['date'], "%Y-%m-%d").date()
            if filter_var.get() == "previous" and b_date < today:
                filtered.append(b)
            elif filter_var.get() == "today" and b_date == today:
                filtered.append(b)
            elif filter_var.get() == "future" and b_date > today:
                filtered.append(b)
            elif filter_var.get() == "all":
                filtered.append(b)

        if not filtered:
            listbox.insert(END, "No bookings found for this filter.")
            return

        listbox.insert(END,
                       f"  {'ID':<4} {'Customer':<18} {'Hotel':<10}  {'Room Type':<12}        {'Check-in':<12} {'Time':<6}     {'Rooms':<6}      {'Services'}")
        listbox.insert(END, "-" * 200)

        for b in filtered:
            services_str = ", ".join(b['services']) if b['services'] else "None"
            listbox.insert(END,
                           f"  {b['id']:<4} {b['customer_name']:<18} {b['hotel_code']:<10}   {b['room_type']:<12}      {b['date']:<12}  {b['time']:<6}      {b['num_rooms']:<6}    {services_str}")

    filter_var.trace("w", lambda *args: update_list())
    update_list()

    f2 = Frame(root, bg="#f6f1eb")
    f2.pack()
    Button(f2, text="⏪ Back", bg="#8b5e3c", fg="white", font=("Arial", 12, "bold"), height=2, width=13,
           command=main, relief=RAISED, bd=4, cursor="hand2").pack(pady=10)


def delete_booking():
    clear_frame()
    title_bar = Label(root, text="🗑️ Delete Booking", font=("Arial", 24, "bold"),
                      bg="#deb887", fg="black", pady=10)
    title_bar.pack(fill=X)

    # Frame to hold Listbox and Scrollbars
    listbox_frame = Frame(root)
    listbox_frame.pack(pady=10)

    # Scrollbars
    y_scroll = Scrollbar(listbox_frame, orient=VERTICAL)
    x_scroll = Scrollbar(listbox_frame, orient=HORIZONTAL)

    listbox = Listbox(listbox_frame, width=100, height=15, font=("Courier New", 10),
                      yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)

    # Configure scrollbars
    y_scroll.config(command=listbox.yview)
    x_scroll.config(command=listbox.xview)

    # Grid layout for proper alignment
    listbox.grid(row=0, column=0, sticky="nsew")
    y_scroll.grid(row=0, column=1, sticky="ns")
    x_scroll.grid(row=1, column=0, sticky="ew")

    # Allow Listbox to expand
    listbox_frame.grid_rowconfigure(0, weight=1)
    listbox_frame.grid_columnconfigure(0, weight=1)

    def load_bookings():
        listbox.delete(0, END)
        my_cursor.execute("SELECT * FROM booking")
        rows = my_cursor.fetchall()
        global current_bookings
        current_bookings = rows

        if not rows:
            listbox.insert(END, "No bookings available.")
            return

        listbox.insert(END,
                       f"  {'Index':<6} {'BookingID':<10}   {'Customer':<18} {'Hotel':<12} {'Room Type':<12} {'Date':<12}")
        listbox.insert(END, "-" * 120)  # Adjusted length for horizontal scroll

        for i, row in enumerate(rows):
            listbox.insert(END,
                           f"   {i:<6}  {row[0]:<10}{row[2]:<18} {row[1]:<12} {row[7]:<12} {row[3].strftime('%Y-%m-%d'):<12}")

    def delete_selected():
        selected = listbox.curselection()
        if not selected or selected[0] < 2:
            messagebox.showerror("Error", "Please select a valid booking to delete.")
            return

        idx = selected[0] - 2
        if idx >= len(current_bookings):
            messagebox.showerror("Error", "Selected booking does not exist.")
            return

        booking_id = current_bookings[idx][0]
        customer = current_bookings[idx][2]

        confirm = messagebox.askyesno("Confirm Delete", f"Delete booking ID {booking_id} for {customer}?")

        if confirm:
            try:
                my_cursor.execute("DELETE FROM booking WHERE booking_id = %s", (booking_id,))
                mydb.commit()
                messagebox.showinfo("Deleted", f"Booking ID {booking_id} deleted.")
                load_bookings()
            except Exception as e:
                messagebox.showerror("Database Error", f"An error occurred:\n{str(e)}")

    load_bookings()

    Button(root, text="Delete Selected Booking", bg="green", fg="white", font=("Arial", 12, "bold"), height=2,
           relief="raised", command=delete_selected, bd=4, cursor="hand2").pack(pady=10)

    Button(root, text="⏪ Back", bg="#8b5e3c", fg="white", font=("Arial", 12, "bold"), height=2, width=13,
           command=main, relief=RAISED, bd=4, cursor="hand2").pack(pady=10)


def search_hotel():
    clear_frame()

    def search_action():
        code = code_entry.get().strip().upper()
        if not code:
            messagebox.showwarning("Input Error", "Please enter a hotel code.")
            return

        try:
            my_cursor.execute("SELECT * FROM hotels WHERE hotel_code = %s", (code,))
            hotel = my_cursor.fetchone()

            clear_frame()

            if hotel:
                Label(root, text="Hotel Details", font=("Helvetica", 13, "bold"), bg="#f6f1eb").pack(pady=5)

                details = f"Hotel Code: {hotel[0]}\nHotel Name: {hotel[1]}\nLocation: {hotel[2]}\nContact: {hotel[3]}"
                Label(root, text=details, bg="#f6f1eb", font=("Arial", 11), justify=LEFT, anchor="w").pack()

                my_cursor.execute("""
                    SELECT r.room_type, r.person, r.bed, r.facilities, r.price
                    FROM hotels h
                    JOIN rooms r ON h.hotel_code = r.hotel
                    WHERE h.hotel_code = %s
                """, (code,))
                rooms = my_cursor.fetchall()

                Label(root, text="\nRoom Types Available", font=("Helvetica", 12, "bold"), bg="#f6f1eb").pack(pady=5)

                list_frame = Frame(root, bg="#fef6e4")
                list_frame.pack(pady=5)
                h_scrollbar = Scrollbar(list_frame, orient=HORIZONTAL)
                scrollbar = Scrollbar(list_frame, orient=VERTICAL)
                room_listbox = Listbox(list_frame, yscrollcommand=scrollbar.set, xscrollcommand=h_scrollbar.set,
                                       width=70, height=10, font=("Courier", 9))
                scrollbar.config(command=room_listbox.yview)
                h_scrollbar.config(command=room_listbox.xview)
                scrollbar.pack(side=RIGHT, fill=Y)
                h_scrollbar.pack(side=BOTTOM, fill=X)
                room_listbox.pack(side=LEFT, fill=BOTH, expand=True)
                Button(root, text="Back", bg="red", fg="white", height=2, width=15,
                       font="Arial 12 bold", command=main, relief=RAISED, cursor="hand2", bd=3).pack(pady=15)

                if rooms:
                    for idx, room in enumerate(rooms, start=1):
                        info = (f"{idx}. Type: {room[0]}  |  Person: {room[1]}  |  Bed: {room[2]}  |  "
                                f"Facilities: {room[3]}  |  Price: {room[4]} PKR")
                        room_listbox.insert(END, info)
                else:
                    room_listbox.insert(END, "No rooms found for this hotel.")
            else:
                Label(root, text="No hotel found with this code.", fg="red", bg="#fef6e4").pack()

        except Exception as e:
            messagebox.showerror("Database Error", f"Error: {e}")

    title_bar = Label(root, text="🏨 Search Hotel Details", font=("Arial", 24, "bold"),
                      bg="#deb887", fg="black", pady=10)
    title_bar.pack(fill=X)

    search_frame = Frame(root, bg="#f6f1eb")
    search_frame.pack(pady=20)
    Label(search_frame, text="Enter Hotel Code:", font=("Arial", 11), bg="#f6f1eb").grid(row=2, column=0, padx=5, pady=5)
    code_entry = Entry(search_frame, font=("Arial", 11))
    code_entry.grid(row=2, column=1, padx=5, pady=5)
    Button(search_frame, text="Search", font=("Arial", 15), bg="#8b5e3c", fg="white", command=search_action,
           relief=RAISED, cursor="hand2", bd=3, height=1).grid(row=2, column=2, padx=10)
    Button(root, text="Back", bg="red", fg="white", height=2, width=15,
           font="Arial 12 bold", command=main, relief=RAISED, cursor="hand2", bd=3).pack(pady=15)


def main():
    clear_frame()
    title_bar = Label(root, text="🏨 Hotel Booking System", font=("Garamond", 24, "bold"),
                      bg="BurlyWood", anchor="center")
    title_bar.pack(fill=X, pady=15)
    f1 = Frame(root, bg="#f6f1eb")
    f1.pack()
    styled_button1(f1, "Hotel Details", h_d)
    styled_button1(f1, "Search Hotels", search_hotel)
    f2 = Frame(root, bg="#f6f1eb")
    f2.pack()
    styled_button1(f2, "Delete Booking", delete_booking)
    styled_button1(f2, "Show Booking", show_bookings)
    f3 = Frame(root, bg="#f6f1eb")
    f3.pack()
    styled_button1(f3, "Room Booking", r_b)
    Button(root, text="Exit", bg="red", fg="white", height=2, width=18, font="Arial 12 bold", command=root.quit,
           relief=RAISED, cursor="hand2", bd=3).pack(padx=10, pady=10)


main()
root.mainloop()
