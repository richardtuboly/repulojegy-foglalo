from abc import ABC, abstractmethod
from datetime import datetime
import uuid


class Flight(ABC):
    def __init__(self, flightnumber, destination, ticketprice):
        self.flightnumber = flightnumber
        self.destination = destination
        self.ticketprice = ticketprice

    @abstractmethod
    def description(self):
        pass


class DomesticFlight(Flight):
    def __init__(self, flightnumber, destination, ticketprice):
        super().__init__(flightnumber, destination, ticketprice * 0.5)

    def description(self):
        return f"Domestic flight {self.flightnumber} -> {self.destination}, Ticket price: £ {self.ticketprice}"


class InternationalFlight(Flight):
    def __init__(self, flightnumber, destination, ticketprice):
        super().__init__(flightnumber, destination, ticketprice * 1.5)

    def description(self):
        return f"International flight {self.flightnumber} -> {self.destination}, Ticket price: £ {self.ticketprice}"


class Airline:
    def __init__(self, name):
        self.name = name
        self.flights = []

    def add_flight(self, flight):
        self.flights.append(flight)

    def get_flight(self, flightnumber):
        for flight in self.flights:
            if flight.flightnumber == flightnumber:
                return flight
        return None

    def list_flights(self):
        for flight in self.flights:
            print(flight.description())


class TicketReservation:
    def __init__(self, flight, passenger_name, date):
        self.id = str(uuid.uuid4())[:8]
        self.flight = flight
        self.passenger_name = passenger_name
        self.date = date

    def __str__(self):
        return f"[{self.id}] {self.passenger_name} - {self.flight.flightnumber} ({self.flight.destination}) {self.date.strftime('%Y-%m-%d')} - Price: £ {self.flight.ticketprice}"


class ReservationSystem:
    def __init__(self, airline):
        self.airline = airline
        self.reservations = []

    def reserve_ticket(self, flightnumber, passenger_name, date_str):
        flight = self.airline.get_flight(flightnumber)
        if not flight:
            print("Error: Flight no. doesn't exist.")
            return None
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d")
            if date < datetime.now():
                print("Error: Only future dates are allowed.")
                return None
        except ValueError:
            print("Error: Invalid date format. Use YYYY-MM-DD.")
            return None

        reservation = TicketReservation(flight, passenger_name, date)
        self.reservations.append(reservation)
        print(f"Successful reservation! Identifier: {reservation.id}")
        return reservation.flight.ticketprice

    def cancel_reservation(self, reservation_id):
        for reservation in self.reservations:
            if reservation.id == reservation_id:
                self.reservations.remove(reservation)
                print("Successful cancellation.")
                return
        print("Error: The specified reservation doesn't exist.")

    def list_reservations(self):
        if not self.reservations:
            print("No reservations found.")
        for f in self.reservations:
            print(f)


def user_interface(system):
    while True:
        print("\n--- Ticket reservation system ---")
        print("1. Ticket reservation")
        print("2. Cancel reservation")
        print("3. List reservations")
        print("4. List flights")
        print("0. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            flightnumber = input("Flight no.: ")
            passenger_name = input("Passenger name: ")
            date = input("Flight date (YYYY-MM-DD): ")
            system.reserve_ticket(flightnumber, passenger_name, date)
        elif choice == "2":
            identifier = input("Reservation identifier: ")
            system.cancel_reservation(identifier)
        elif choice == "3":
            system.list_reservations()
        elif choice == "4":
            system.airline.list_flights()
        elif choice == "0":
            print("Exit...")
            break
        else:
            print("Invalid option. Please try again.")


# Preparation, data initializing
wizzair = Airline("WizzAir")
wizzair.add_flight(DomesticFlight("M001", "Bristol", 10000))
wizzair.add_flight(DomesticFlight("M002", "Luton", 12000))
wizzair.add_flight(InternationalFlight("H001", "Amsterdam", 20000))

system = ReservationSystem(wizzair)

# 6 preloaded reservations
system.reserve_ticket("M001", "Korbin Parker", "2025-06-01")
system.reserve_ticket("M001", "Boyce Ayers", "2025-06-01")
system.reserve_ticket("M002", "Averie Gregory", "2025-06-10")
system.reserve_ticket("M002", "Claire Walton", "2025-06-10")
system.reserve_ticket("H001", "Marion White", "2025-07-15")
system.reserve_ticket("H001", "Daphne Fabian", "2025-07-15")

# Start user interface
user_interface(system)