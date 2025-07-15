                                        Hotel Table
my_cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
my_cursor.execute("DROP TABLE IF EXISTS hotels")
my_cursor.execute("""CREATE TABLE IF NOT EXISTS hotels (hotel_code VARCHAR(20) PRIMARY KEY,
hotel_name VARCHAR(100) NOT NULL,location VARCHAR(100),contact_number VARCHAR(20))""")
sql = "INSERT INTO hotels(hotel_code, hotel_name, location, contact_number) VALUES (%s, %s, %s, %s)"
values = [("HTL001", "PC (5-Star)", "Lahore", "03001234567"),
          ("HTL002", "City Comfort Inn (3-Star)", "Karachi", "03011234567"),
          ("HTL003", "Beachside Resort (Resort)", "Gwadar", "03021234567"),
          ("HTL004", "Budget Resort (Budget)", "Multan", "03031234567"),
          ("HTL005", "Mountain View Lodge (4-Star)", "Murree", "03041234567"),
          ("HTL006", "Nature Retreat (Eco)", "Hunza", "03051234567"),
          ("HTL007", "Amusement Inn (Theme)", "Islamabad", "03061234567")]
my_cursor.executemany(sql, values)
mydb.commit()
my_cursor.execute("SELECT * FROM hotels")
for x in my_cursor:
    print(x)


                                       Rooms Table
my_cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
my_cursor.execute("DROP TABLE IF EXISTS rooms")
my_cursor.execute("""CREATE TABLE IF NOT EXISTS rooms (id INT AUTO_INCREMENT PRIMARY KEY,hotel VARCHAR(20),
room_type VARCHAR(50),available INT,person VARCHAR(50),bed VARCHAR(50),facilities TEXT,price INT,
FOREIGN KEY (hotel) REFERENCES hotels(hotel_code))""")
sql = ("INSERT INTO rooms(hotel, room_type, available, person, bed, facilities, price)"
       " VALUES (%s, %s, %s, %s, %s, %s, %s)")
values = [("HTL001", "Deluxe", 5, "1-2", "1-King Bed", "Upgraded Decors,Better View,Minibar,Larger Bathroom", 20000),
    ("HTL001", "Executive", 5, "2-3", "2-Double Bed", "Work desk,Access of executed lounge,Toiletries", 15000),
    ("HTL001", "Standard", 5, "1-2", "1-Double Bed / 2-Single Bed", "Basic Amenities", 5000),
    ("HTL001", "Family", 5, "4-6", "1-Double + 2-Single Beds", "Extra space,Multiple Beds,Kid-friendly,Kitchenette", 10000),
    ("HTL002", "Standard", 5, "2", "1-Queen Bed", "TV, Mini Fridge", 5000),
    ("HTL002", "Business", 5, "2 Adults + 1 Child", "2-Double Bed", "TV, Mini Fridge, Work Desk", 7500),
    ("HTL003", "Ocean View", 5, "2 Adults", "1 King Bed", "TV, Ocean View Balcony, Breakfast", 12000),
    ("HTL003", "Cottage", 5, "4 Adults", "2 Queen Beds", "TV, Private Garden, Kitchenette, Lounge Area", 18000),
    ("HTL004", "Single", 5, "1 Adult", "1-Single Bed", "TV", 3000),
    ("HTL004", "Double", 5, "2 Adults", "1-Double Bed", "TV, Mini Fridge", 4500),
    ("HTL005", "Standard Lodge", 5, "2 Adults", "1-Queen Bed", "Heating, Balcony, Mountain View", 9500),
    ("HTL005", "Family Suite", 5, "4 Persons", "2-Queen Beds", "Heating, Fireplace, Kitchenette, Mountain View", 14500),
    ("HTL005", "Honeymoon Cabin", 5, "2 Adults", "1-King Bed", "Romantic Decor, Private Jacuzzi, Mountain View", 16500),
    ("HTL006", "Eco Family Suite", 5, "2 Adults + 2 Kids", "2-Double Beds",
     "Solar-powered lighting, Kitchenette, Forest view", 12000),
    ("HTL007", "Standard Room", 5, "2 Adults", "1-Queen Bed", "TV, Theme Park Access", 6000),
    ("HTL007", "Family Suite", 5, "4 Adults", "2-Double Beds", "TV, Kids Play Area, Kitchenette", 12000)]
my_cursor.executemany(sql, values)
mydb.commit()
my_cursor.execute("SELECT * FROM rooms")
for x in my_cursor:
    print(x)


                                        View hotel_room_details
my_cursor.execute("DROP VIEW IF EXISTS hotel_room_details")
mydb.commit()
my_cursor.execute("CREATE VIEW hotel_room_details AS SELECT h.hotel_code, h.hotel_name, h.location, h.contact_number,"
                  " r.room_type, r.person, r.bed, r.facilities, r.price "
                  "FROM hotels h JOIN rooms r ON h.hotel_code = r.hotel")
my_cursor.execute("SELECT * FROM hotel_room_details")
for x in my_cursor:
    print(x)


                                        Booking table
my_cursor.execute("DROP TABLE IF EXISTS booking")
my_cursor.execute("""CREATE TABLE booking (booking_id INT AUTO_INCREMENT PRIMARY KEY,hotel_code VARCHAR(100),
cus_name VARCHAR(255),check_in_date DATE,check_in_time VARCHAR(10),check_out_date DATE,check_out_time VARCHAR(10),
room_type VARCHAR(100),no_of_rooms INT,additional_service TEXT,price INT)""")

sql = ("INSERT INTO booking (hotel_code, cus_name, check_in_date, check_in_time, check_out_date, check_out_time, "
       "room_type, no_of_rooms, additional_service, price) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

values = [("HTL001", "John Doe", "2025-05-01", "01:00 AM", "2025-06-05", "11:00 PM", "Deluxe", 1, "Breakfast, WiFi", 500),
          ("HTL002", "Jane Smith", "2025-05-03", "05:00 PM", "2025-06-06", "10:00 PM", "Standard", 2, "WiFi", 450),
          ("HTL003", "Ali Khan", "2025-06-02", "03:00 PM", "2025-06-04", "12:00 PM", "Suite", 1, "Breakfast, Gym Access", 800),
          ("HTL004", "Emily Brown", "2025-06-05", "06:00 AM", "2025-06-07", "11:30 PM", "Economy", 3, "None", 300),
          ("HTL005", "Michael Jordan", "2025-06-01", "12:00 AM", "2025-06-03", "10:00 PM", "Deluxe", 1, "Breakfast", 550),
          ("HTL006", "Fatima Zahra", "2025-05-04", "11:00 AM", "2025-06-08", "09:00 PM", "Suite", 2, "Spa, WiFi", 950),
          ("HTL007", "Daniel Lee", "2025-05-27", "04:30 PM", "2025-06-10", "11:00 PM", "Standard", 1, "Parking, Breakfast", 400),
          ("HTL008", "Sophia Loren", "2025-06-07", "05:00 PM", "2025-06-09", "10:30 PM", "Deluxe", 2, "WiFi", 600)]
my_cursor.executemany(sql, values)
mydb.commit()

my_cursor.execute("SELECT * FROM booking")
for x in my_cursor:
    print(x)


                                                emp Table
my_cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
my_cursor.execute("DROP TABLE IF EXISTS emp")
my_cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
my_cursor.execute("""CREATE TABLE IF NOT EXISTS  emp (emp_id INT PRIMARY KEY AUTO_INCREMENT,name VARCHAR(50),department VARCHAR(50),
job_rank VARCHAR(50), salary INT)""")
sql = "INSERT INTO emp(name,department,job_rank,salary) VALUES(%s,%s,%s,%s)"
values = [('Ahmad', 'Security', 'Security Manager', 50000), ('Ali', 'Security', 'Security Supervisor', 20000),
          ('Zain', 'Security', 'Security Guard', 65000), ('Arham', 'Housekeeping', 'Laundry Attendant', 50000),
          ('Balaj', 'Housekeeping', 'Public Area Cleaner', 20000),
          ('Hamza', 'Housekeeping', 'Housekeeping Supervisor', 65000), ('Abdullah', 'Housekeeping', 'TL', 50000),
          ('Farhan', 'Housekeeping', 'Maid', 25000), ('Zohaib', 'Reception', 'Receptionist', 100000),
          ('Balaj', 'Reception', 'Bellboy', 20000),
          ('Hamza', 'Reception', 'Night Auditor', 65000), ('Abdullah', 'Finance', 'Accountant', 50000),
          ('Farhan', 'Finance ', 'Audit Clerk', 25000), ('Zohaib', 'Reception', 'Guest Service Agent', 100000)
          ]
my_cursor.executemany(sql, values)
mydb.commit()
my_cursor.execute("SELECT * FROM emp")
for x in my_cursor:
    print(x)





my_cursor.execute("SHOW TABLES")
for x in my_cursor:
    print(x)




