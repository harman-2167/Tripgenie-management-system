# tripgenie application built with Python and sql 

import pymysql

db = pymysql.connect(
    host="localhost",
    user="root",
    password="YourPasswordHere",
    database="TripGenie"
)

cursor = db.cursor()


#-------------LOGIN PAGE---------------

def customer_login(booking_type, booking_number):
    global Name

    Name = input("Enter your name: ")
    Phone = int(input("Enter phone number: "))
    Email = input("Enter email id: ")

    if "@" not in Email:
        print("Invalid Email! Email must contain @")
        return
    
    City = input("Enter your city: ")

    query = """
    INSERT INTO bookings (name, phone, email, city, booking_type, booking_number)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    values = (Name, Phone, Email, City, booking_type, booking_number)

    cursor.execute(query, values)
    db.commit()

    print("Customer details saved in database successfully!")


#-------------GLOBAL VARIABLES---------------

booked_place = []
booked_hotel = []

selected_place = None
hotel_fare = 0
transport_fare = 0
members=0

booking_id =1


#-----------REGION MENU------------

def region():
    print("""\nSELECT YOUR REGION 
1 → North India
2 → South India
3 → East India
4 → West India
""")


def north():
    print("""
1 → Amritsar
2 → Shimla
3 → Dharamshala
4 → Manali
5 → Srinagar
""")


def south():
    print("""
6 → Ooty
7 → Munnar
8 → Coorg
9 → Mysore
10 → Kodaikanal
""")


def east():
    print("""
11 → Darjeeling
12 → Gangtok
13 → Puri
14 → Shillong
15 → Kaziranga
""")


def west():
    print("""
16 → Goa
17 → Udaipur
18 → Jaisalmer
19 → Mount Abu
20 → Mumbai
""")


#-------------PLACE MAP---------------

place_map = {
    1: "Amritsar", 2: "Shimla", 3: "Dharamshala", 4: "Manali", 5: "Srinagar",
    6: "Ooty", 7: "Munnar", 8: "Coorg", 9: "Mysore", 10: "Kodaikanal",
    11: "Darjeeling", 12: "Gangtok", 13: "Puri", 14: "Shillong", 15: "Kaziranga",
    16: "Goa", 17: "Udaipur", 18: "Jaisalmer", 19: "Mount Abu", 20: "Mumbai"
}


#-------------REGION BOOKING---------------

def region_booking():
    region()

    choice = int(input("Enter region (1-4): "))

    if choice == 1:
        north()
    elif choice == 2:
        south()
    elif choice == 3:
        east()
    elif choice == 4:
        west()
    else:
        print("Invalid choice")
        return

    places_booking()


#-------------PLACE BOOKING---------------

def places_booking():

    global selected_place

    place = int(input("Enter your destination (1-20): "))

    if place in booked_place:
        print("This place is already booked.")
        return

    if place not in place_map:
        print("Invalid place")
        return

    booked_place.append(place)
    selected_place = place_map[place]

    print("Your destination is booked successfully!")
    print("Selected Place:", selected_place)
    
    query = """
    INSERT INTO place_booking (customer_name, place_name, place_fare)
    VALUES (%s, %s, %s)
    """

    # place_fare abhi 0 hai (simple version)
    cursor.execute(query, (Name, selected_place, 0))
    db.commit()

    print("Place saved in database!")


#-------------HOTEL BOOKING---------------

def hotel():

    global hotel_fare, selected_place, booked_hotel,booking_id,members

    if selected_place is None:
        print("Please book a place first!")
        return

    rooms = {
        1: ("Family Room", 2500),
        2: ("Couple Room", 2200),
        3: ("Single Room", 1800),
        4: ("AC Premium Room", 3000),
        5: ("Non AC Room", 2000)
    }

    print("""
1 → Family Room
2 → Couple Room
3 → Single Room
4 → AC Premium Room
5 → Non AC Room
""")

    Room = int(input("Enter room number (1–5): "))

    if Room not in rooms:
        print("Invalid choice")
        return
    
    members=int(input("enter how many members:"))
    if (selected_place, Room) in booked_hotel:
        print("This room is already booked for this place.")
        return

    Room_selected, room_price = rooms[Room]
    hotel_fare = room_price * members
    
    
    query = """
    INSERT INTO hotel_booking (customer_name, room_type, room_fare)
    VALUES (%s, %s, %s)
    """

    cursor.execute(query, (Name, Room_selected, hotel_fare))
    db.commit()

    print("Hotel booking saved in database!")

    booked_hotel.append((selected_place, Room))
    booking_id= booking_id+1

    customer_login("Hotel Booking", Room)

    print("You selected:", Room_selected)
    print("Members:", members)
    print("Room cost:", hotel_fare )
    print("Room booked successfully!")


#-------------TRANSPORT---------------

def transportation():

    global transport_fare,selected_place, members
    if selected_place is None:
        print("please book place first")
        return 

    print("""
1 → Bus    ₹800
2 → Train  ₹600
3 → Cab    ₹3500
""")

    choice = int(input("Enter your choice (1-3): "))

    if choice == 1:
        transport_name = "Bus"
        transport_fare = 800 *members
    elif choice == 2:
        transport_name = "Train"
        transport_fare = 600 *members
    elif choice == 3:
        transport_name = "Cab"
        transport_fare = 3500 *members
    else:
        print("Invalid choice")
        return

    print("\nTransport Confirmed")
    print("Name:", transport_name)
    print("Fare:", transport_fare)
    
   
    query = """
    INSERT INTO transport_booking (customer_name, transport_type, transport_fare)
    VALUES (%s, %s, %s)
    """

    cursor.execute(query, (Name, transport_name, transport_fare))
    db.commit()

    print("Transport booking saved in database!")


#-------------TOTAL EXPENSE---------------

def total_expense():
    
    total = hotel_fare + transport_fare
    gst = total * 0.18
    final_total = total + gst

    print("\n========================")
    print("     TRIPGENIE BILL     ")
    print("========================")

    print("Customer Name :", Name)
    print("Place :", selected_place)
    print("Hotel Fare :", hotel_fare)
    print("Transport Fare :", transport_fare)
    print("Subtotal :", total)
    print("GST (18%) :", gst)
    print("FINAL TOTAL :", final_total)

    print("========================")
    print("THANK YOU FOR BOOKING")


#-------------HELP---------------

complaints = []

def help_section():

    print("\nHELP SECTION")

    print("""
Owner: Miss Harmandeep Kaur
Contact: 9876543210
Email: tripgenie@gmail.com
""")

    choice = int(input("1 → Complaint | 2 → Exit: "))

    if choice == 1:
        comp = input("Enter complaint: ")
        query = """
        INSERT INTO complaints (complaint_text)
        VALUES (%s)
        """

        cursor.execute(query, (comp,))
        db.commit()

        print("Complaint saved in database!")

    else:
        print("Exit Help")

    print("Total complaints:", len(complaints))


#-------------FEEDBACK---------------

def feedback():
    
    print("\n----- PREVIOUS CUSTOMER REVIEWS -----")

    cursor.execute("SELECT customer_name, rating, review_text FROM feedback")
    reviews = cursor.fetchall()

    for review in reviews:
        print(f"""
Name   : {review[0]}
Rating : {review[1]}/5
Review : {review[2]}
-------------------------
""")

    print("\nCUSTOMER REVIEW")

    name = input("Name: ")
    rating = int(input("Rating (1-5): "))
    message = input("Review: ")

    query = """
    INSERT INTO feedback
    (customer_name, rating, review_text)
    VALUES (%s, %s, %s)
    """

    cursor.execute(query, (name, rating, message))
    db.commit()

    print("Feedback saved in database!")



#-------------OWNER-LOGIN-----------------
def owner_login():
    password = input("Enter Owner Password: ")

    if password == "Admin123":
        print("Login Successful")

        cursor.execute("SELECT * FROM bookings")
        records = cursor.fetchall()

        for row in records:
            print(row)

    else:
        print("Wrong Password")
        
#-------------DECORATOR---------------

def deco(func):
    def wrapper():
        print("WELCOME TO TRIPGENIE")
        func()
        print("THANK YOU")
    return wrapper


#-------------MAIN MENU---------------

@deco
def query():

    print("""
1 → Login + Place + Hotel flow
2 → Region Booking
3 → Place Booking
4 → Hotel Booking
5 → Transport Booking
6 → Help
7 → Feedback
8 → Total Expense
""")

    ent = int(input("Enter choice: "))

    if ent == 1:
        customer_login("login", 0)
        region_booking()
        hotel()
        transportation()
        total_expense()

    elif ent == 2:
        region_booking()

    elif ent == 3:
        places_booking()

    elif ent == 4:
        hotel()

    elif ent == 5:
        transportation()

    elif ent == 6:
        help_section()

    elif ent == 7:
        feedback()

    elif ent == 8:
        total_expense()

    elif ent == 9:
        owner_login()

    else:
        print("Invalid Choice")


query()