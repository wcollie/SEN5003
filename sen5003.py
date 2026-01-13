import csv #import csv module
import os #import os module
from datetime import datetime #for date parsing

flights = {} #store flights
passengers = {} #store passengers
reservations = [] #store reservations

flightsFile = "flights.csv" #filename for flights
passengerFile = "passengers.csv" #filename for passengers
reservationsFile = "reservations.csv" #filename for reservations

def load_data(): #load all csv data into memory
    if os.path.exists(flightsFile): 
        with open(flightsFile, newline="") as file: 
            reader = csv.DictReader(file)
            for row in reader:
                flights[row["flight_id"]] = {
                    "origin": row["origin"],
                    "destination": row["destination"],
                    "date": row["date"],
                    "cost": float(row["cost"]),
                    "seats": int(row["seats"])
                }
    if os.path.exists(passengerFile): 
        with open(passengerFile, newline="") as file: 
            reader = csv.DictReader(file)
            for row in reader:
                passengers[row["passenger_id"]] = row["name"]
    if os.path.exists(reservationsFile): 
        with open(reservationsFile, newline="") as file: 
            reader = csv.DictReader(file)
            for row in reader:
                reservations.append(row)

def save_flights(): #write flights to csv
    with open(flightsFile, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["flight_id", "origin", "destination", "date", "cost", "seats"])
        for flight_id, flight in flights.items():
            writer.writerow([flight_id, flight["origin"], flight["destination"], flight["date"], flight["cost"], flight["seats"]])

def save_passengers(): #write passengers to csv
    with open(passengerFile, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["passenger_id", "name"])
        for pid, name in passengers.items():
            writer.writerow([pid, name])

def save_reservations(): #write reservations to csv
    with open(reservationsFile, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["passenger_id", "flight_id"])
        for r in reservations:
            writer.writerow([r["passenger_id"], r["flight_id"]])

def add_flight(): #input new flight
    flight_id = input("Enter Flight ID: ") 
    origin = input("Origin City: ") 
    destination = input("Destination City: ") 
    try:
        date_input = input("Date (DD-MM-YYYY): ") 
        datetime.strptime(date_input, "%d-%m-%Y") #check correct format
    except ValueError: 
        print("Invalid date format. Please use DD-MM-YYYY.\n") 
        return
    cost = float(input("Ticket Cost: ")) 
    seats = int(input("Available Seats: ")) 
    flights[flight_id] = {"origin": origin, "destination": destination, "date": date_input, "cost": cost, "seats": seats} 
    save_flights() 
    print("Flight added successfully.\n") 

def add_passenger(): #input new passenger
    passenger_id = input("Enter Passenger ID: ") 
    name = input("Passenger Name: ") 
    passengers[passenger_id] = name 
    save_passengers() 
    print("Passenger added successfully.\n") 

def print_flight(flight_id, flight): #show flight details
    print(f"Flight ID: {flight_id}")
    print(f"Origin: {flight['origin']}")
    print(f"Destination: {flight['destination']}")
    print(f"Date: {flight['date']}")
    print(f"Cost: {flight['cost']}")
    print(f"Available Seats: {flight['seats']}")
    print("--------------------------------------------------------")
    print("\n") 

def search_flights(): #find flights by origin/destination/date
    origin = input("Enter Origin City: ") 
    destination = input("Enter Destination City: ") 
    date_filter = input("Enter Date (DD-MM-YYYY or leave blank): ") 
    print("\nAvailable Flights:") 
    found = False 
    for flight_id, flight in flights.items(): 
        if flight["origin"] == origin and flight["destination"] == destination: 
            if date_filter == "" or flight["date"] == date_filter: 
                print_flight(flight_id, flight) 
                found = True 
    if not found: 
        print("No matching flights found. Please ensure data is entered correctly\n") 

def book_reservation(): #reserve a seat
    passenger_id = input("Passenger ID: ") 
    flight_id = input("Flight ID: ") 
    if passenger_id not in passengers: 
        print("Passenger not found. Please ensure Passenger ID is entered correctly\n") 
        return
    if flight_id not in flights: 
        print("Flight not found. Please ensure Flight ID is entered correctly\n") 
        return
    if flights[flight_id]["seats"] <= 0: 
        print("Unfortunatly no seats available. \n") 
        return
    reservations.append({"passenger_id": passenger_id, "flight_id": flight_id}) 
    flights[flight_id]["seats"] -= 1 
    save_reservations() 
    save_flights() 
    print("Reservation booked successfully.\n") 

def cancel_reservation(): #remove reservation
    passenger_id = input("Passenger ID: ") 
    flight_id = input("Flight ID: ") 
    for r in reservations: 
        if r["passenger_id"] == passenger_id and r["flight_id"] == flight_id: 
            reservations.remove(r) 
            flights[flight_id]["seats"] += 1 
            save_reservations() 
            save_flights() 
            print("Reservation successfully cancelled.\n") 
            return
    print("Reservation not found. Please ensure Reservation ID is entered correctly\n") 

def sort_flights(): #view flights sorted
    if len(flights) == 0: 
        print("No flights added.\n") 
        return
    print("Sort flights by:\n1. Cost (Low to High)\n2. Cost (High to Low)\n3. Date (Earliest to Latest)\n4. Date (Latest to Earliest)") 
    choice = input("Choose an option: ") 
    if choice == "1": 
        sorted_flights = sorted(flights.items(), key=lambda x: x[1]["cost"]) 
    elif choice == "2": 
        sorted_flights = sorted(flights.items(), key=lambda x: x[1]["cost"], reverse=True) 
    elif choice == "3": 
        sorted_flights = sorted(flights.items(), key=lambda x: datetime.strptime(x[1]["date"], "%d-%m-%Y")) 
    elif choice == "4": 
        sorted_flights = sorted(flights.items(), key=lambda x: datetime.strptime(x[1]["date"], "%d-%m-%Y"), reverse=True) 
    else: 
        print("Invalid choice.\n") 
        return
    for flight_id, flight in sorted_flights: 
        print_flight(flight_id, flight) 

def sort_passengers(): #view passengers sorted
    if len(passengers) == 0: 
        print("No passengers added.\n") 
        return
    print("Sort passengers by:\n1. Passenger ID\n2. Name") 
    choice = input("Choose an option: ") 
    if choice == "1": 
        sorted_passengers = sorted(passengers.items(), key=lambda x: x[0]) 
    elif choice == "2": 
        sorted_passengers = sorted(passengers.items(), key=lambda x: x[1]) 
    else: 
        print("Invalid choice.\n") 
        return
    for pid, name in sorted_passengers: 
        print(f"Passenger ID: {pid}")
        print(f"Name: {name}")
        print("--------------------------------------------------------")
        print("\n") 

def sort_reservations(): #view reservations sorted
    if len(reservations) == 0: 
        print("No reservations added.\n") 
        return
    print("Sort reservations by:\n1. Flight ID\n2. Passenger ID") 
    choice = input("Choose an option: ") 
    if choice == "1": 
        sorted_res = sorted(reservations, key=lambda x: x["flight_id"]) 
    elif choice == "2": 
        sorted_res = sorted(reservations, key=lambda x: x["passenger_id"]) 
    else: 
        print("Invalid choice.\n") 
        return
    for r in sorted_res: 
        print(f"Passenger ID: {r['passenger_id']}, Flight ID: {r['flight_id']}") 
        print("--------------------------------------------------------")
        print("\n") 

def reservation_count(): #count reservations for each flight
    for flight_id in flights: 
        count = sum(1 for r in reservations if r["flight_id"] == flight_id) 
        print(f"Flight {flight_id}: {count} reservation(s)") 
    print() 

def menu(): #main menu loop
    load_data() 
    while True: 
        print("*****----  EDD Airlines Flight Reservation System  ----*****") 
        print("1. Add Flight") 
        print("2. Add Passenger") 
        print("3. Search Flights") 
        print("4. Book Reservation") 
        print("5. Cancel Reservation") 
        print("6. View Flights") 
        print("7. View Passengers") 
        print("8. View Reservations") 
        print("9. Reservation Count") 
        print("10. Exit") 
        choice = input("Choose an option: ") 
        if choice == "1": 
            add_flight() 
        elif choice == "2": 
            add_passenger() 
        elif choice == "3": 
            search_flights() 
        elif choice == "4": 
            book_reservation() 
        elif choice == "5": 
            cancel_reservation() 
        elif choice == "6": 
            sort_flights() 
        elif choice == "7": 
            sort_passengers() 
        elif choice == "8": 
            sort_reservations() 
        elif choice == "9": 
            reservation_count() 
        elif choice == "10": 
            print("Exiting system...") 
            break

menu() #start program
