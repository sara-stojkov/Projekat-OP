# modul za karte, rezervacije, kupovinu itd
from datetime import date, datetime, timedelta
from prettytable import PrettyTable
from projections import search_for_showtime


def spaces4():
    print("-" * 30)


def display_seats(tickets_list, single_auditorium, single_showtime, only_display):
    # only display will be a boolean value that allows multiple uses of this function - displaying and choosing a seat
    print("You will now see the seats on the screening of your choice.")
    spaces4()
    tickets_for_this = [ticket for ticket in tickets_list if ticket[1] == single_showtime[0]]
    taken_seats = [ticket[2] for ticket in tickets_for_this]
    all_rows = [number for number in range(1, int(single_auditorium[0][1]) + 1)]
    all_columns = [letter for letter in single_auditorium[0][2].split(",")]
    all_seats = []
    print("       " + "/" * 33)
    for row in all_rows:
        for a_column in all_columns:
            current_seat = str(row) + a_column
            all_seats.append(current_seat)
    for row in all_rows:
        current_row = []
        for a_column in all_columns:
            current_seat = str(row) + a_column
            if current_seat in taken_seats:
                current_seat = "XX"
            current_row.append(current_seat)
        print(f"Row {row}:  " + (" " * 4).join(current_row))
    spaces4()
    print("The seats labeled XX are not available (they have been sold or reserved).")
    print("The movie screen is closest to the first row. (as shown as //////)")
    if not only_display:
        while True:
            spaces4()
            print("If you want to go back type 'x'.")
            seat_choice = input("Please enter the seat you want (example: 4C)  >>> ")
            spaces4()
            if seat_choice.lower().strip() == 'x':
                print("Going back.")
                return 0
            if len(seat_choice) > 2:
                print("Input too long.")
                continue
            elif seat_choice.upper().strip() in taken_seats:
                print("That seat has already been taken. Try again.")
                continue
            elif seat_choice.upper().strip() not in all_seats:
                print("Invalid input. ")
                continue
            print("Seat chosen successfully. ")
            return seat_choice.upper().strip()
    else:
        return


def loyalty_card_discount(tickets_list, username):
    total = 0
    for ticket in [a_ticket for a_ticket in tickets_list if a_ticket[4] == 'S']:
        date_when_sold = datetime.strptime(ticket[3], '%d-%m-%Y')
        todays_date = datetime.today()
        one_year_ago = todays_date - timedelta(days=365)   # assuming the year is 365 days long
        if ticket[0] == username and one_year_ago <= date_when_sold and len(ticket) > 5:
            total += float(ticket[5])
    if total >= 5000:
        print("You are qualified for our loyalty card discount! Your ticket will be 10% cheaper.")
        return True
    return False


def make_reservation_buy(customer_name, employees_name, showtime_list, screenings_list, tickets_list, auditoriums_list,
                         purpose, users_list):
    # data needed for a ticket: name, showtime, a seat, date of action, Sold or Reserved
    print("In case you want to exit, no matter which step, type in 'x'.")
    while True:
        sh_code = input("What is the code of the showtime you're interested in?  (4 digits and 2 uppercase letters)  ")
        spaces4()
        all_sh_codes = [a_showtime[0] for a_showtime in showtime_list]
        if sh_code.lower().strip() == 'x':
            print("Taking you back to the previous menu.")
            spaces4()
            return
        if sh_code not in all_sh_codes and len(sh_code) == 6:
            print("Sorry, there seems to be some sort of mistake. Please try typing the code again.")
            spaces4()
            continue
        elif len(sh_code) != 6:
            print("Check the length of your code and try again.")
            continue
        a_showtime = showtime_list[all_sh_codes.index(sh_code)]  # current showtime
        showtime_date = a_showtime[1]
        print("Showtime chosen successfully.")
        spaces4()
        screening_code = sh_code[0:4]
        for screening in screenings_list:
            if screening_code == screening[0]:
                auditorium_name = screening[1]
                an_auditorium = [auditorium for auditorium in auditoriums_list if auditorium_name == auditorium[0]]
                chosen_seat = display_seats(tickets_list, an_auditorium, a_showtime, False)
                if chosen_seat == 0:
                    spaces4()
                    print("Since no seat was chosen, this will take you back to the previous menu.")
                    return
                today = date.today()
                today_str = today.strftime("%d-%m-%Y")
                while True:
                    if purpose == "S":
                        print("Are you sure you want to sell this ticket? ( or type 'x' to go back) ")
                        choice = input("Type YES or x. >>> ")
                        spaces4()
                        if choice.lower().strip() == 'x':
                            print("You have exited this process.\nGoing back. ")
                            return
                        elif choice.upper().strip() == "YES":
                            price = float(screening[6])
                            showtime_actual_date = datetime.strptime(showtime_date, '%d-%m-%Y')
                            if showtime_actual_date.weekday() == 1:
                                price -= 50
                                print("You have got a 50 RSD discount since the showtime is on a Tuesday! Yay!")
                            elif showtime_actual_date.weekday() == 5 or showtime_actual_date.weekday() == 6:
                                price += 50
                                print("Showtime on weekends cost 50 RSD more.")
                            if len(customer_name.split(" ")) < 2:  # if it is in fact a username and not a first and
                                # last name  - REGISTERED OR NOT REGISTERED USER
                                if loyalty_card_discount(tickets_list, customer_name):
                                    price = price * 0.9  # 10% off for the loyalty card
                            ticket = [customer_name, sh_code, chosen_seat, today_str, "S", str(price), employees_name]
                            tickets_list.append(ticket)
                            print(f"Your ticket has been saved for a price of {price} RSD. Have a good day!")
                            spaces4()
                            print("You will also now have a chance to sell more tickets.")
                            spaces4()
                            return tickets_list, users_list
                        else:
                            print("Invalid input. Try again. ")
                            continue
                    elif purpose == "R":
                        print("Are you sure you want to reserve this seat? (type 'x' to go back)  >>> ")
                        choice = input("Type YES or x. >>> ")
                        spaces4()
                        if choice.lower().strip() == 'x':
                            print("You have exited this process.\nGoing back. ")
                            return
                        elif choice.upper().strip() == "YES":
                            print("Your reservation has been saved. Thanks for using our services!")
                            print("Reservations are kept for up until 30 minutes before the showtime! ")
                            print("You will now have a chance to reserve more tickets.")
                            spaces4()
                            ticket = [customer_name, sh_code, chosen_seat, today_str, "R"]
                            tickets_list.append(ticket)
                            return tickets_list
                        else:
                            print("Invalid input. Try again. ")
                            continue
        spaces4()


def display_reservations(tickets_list, screenings_list, showtime_list):
    columns = ['Username', 'Showtime code', 'Movie', 'Date of showtime', 'Start time', 'End time', 'Auditorium', 'Seat',
               'Sold or Reserved']
    (names_list, showtime_code_list, movies_list, dates_list, starts_list, ends_list, auditoriums_list, seats_list,
     states_list) = ([], [], [], [], [], [], [], [], [])
    for ticket in tickets_list:
        if len(ticket) > 4:
            for a_showtime in showtime_list:
                date_of_sh = datetime.strptime(a_showtime[1], '%d-%m-%Y') + timedelta(hours=23)
                # we need to add the 23 hours just because the comparison also takes the time into account
                today_date = datetime.today()
                if date_of_sh >= today_date:    # displays only the showtimes that are from today and so on
                    if ticket[1] == a_showtime[0]:
                        dates_list.append(a_showtime[1])
                        names_list.append(ticket[0])
                        showtime_code_list.append(ticket[1])
                        seats_list.append(ticket[2])
                        if ticket[4] == "R":
                            states_list.append("Reservation")
                        elif ticket[4] == "S":
                            states_list.append("Sold")
                        for screening in screenings_list:
                            if ticket[1][0:4] == screening[0]:
                                # we found the screening that matches the showtime
                                movies_list.append(screening[5])
                                starts_list.append(screening[2])
                                ends_list.append(screening[3])
                                auditoriums_list.append(screening[1])

    mytable = PrettyTable()

    mytable.add_column(columns[0], names_list)
    mytable.add_column(columns[1], showtime_code_list)
    mytable.add_column(columns[2], movies_list)
    mytable.add_column(columns[3], dates_list)
    mytable.add_column(columns[4], starts_list)
    mytable.add_column(columns[5], ends_list)
    mytable.add_column(columns[6], auditoriums_list)
    mytable.add_column(columns[7], seats_list)
    mytable.add_column(columns[8], states_list)

    if not names_list:
        print("No reservations to display. ")
        return 0
    print(mytable)


def find_a_ticket(tickets_list, screenings_list, showtime_list, display_all):
    while True:
        if display_all:
            print("Here are all the tickets:")
            x = display_reservations(tickets_list, screenings_list, showtime_list)
            if x == 0:
                spaces4()
                print("Since there are no reservations, you will be taken back.")
                return 1
        print("If at any moment you want to exit, just type 'x'. ")
        name = input("Name on the reservation (or username) >>>  ")
        spaces4()
        if name.lower().strip() == 'x':
            return 0
        elif name not in [ticket[0] for ticket in tickets_list]:
            print("There is no reservation under that name. Try again.")
            spaces4()
            continue
        while True:
            showtime_code = input("The code of the showtime on the reservation >>>  ")
            spaces4()
            if showtime_code.lower().strip() == 'x':
                return 0
            elif showtime_code not in [ticket[1] for ticket in tickets_list]:
                print("There is no reservation for that showtime. Try again.")
                spaces4()
                continue
            while True:
                seat = input("The seat reserved (example: 4C) >>>  ")
                spaces4()
                if seat.lower().strip() == 'x':
                    return 0
                for ticket in tickets_list:
                    if name == ticket[0] and showtime_code == ticket[1]:
                        if seat.upper() == ticket[2]:
                            print(f"The selected ticket:")
                            a_ticket = [ticket]
                            display_reservations(a_ticket, screenings_list, showtime_list)
                            return ticket
                print("No tickets with that seat were found. Taking you back.")
                return 0


def edit_a_reservation(ticket_list, screenings_list, showtime_list, auditoriums_list):
    ticket = find_a_ticket(ticket_list, screenings_list, showtime_list, True)
    if ticket == 0:
        print("Since no reservation was chosen, this will take you back to the previous menu.")
        return
    print("Do you want to edit:\n  1. Name\n  2. Showtime code\n  3. Seat")
    choice = input("Enter 1-3 or 'x' to exit >>>  ")
    if choice.lower().strip() == 'x':
        spaces4()
        print("Going back to the previous menu.")
        return
    if choice.strip() == '1':
        spaces4()
        if len(ticket[0].split(" ")) < 2:
            print("You can't change the username on a ticket. Taking you back.")
            return
        new_name = input("Enter the changed first and last name (or 'x' to keep the old one) >>> ")
        if new_name.lower().strip() == 'x':
            print("Change cancelled. Going back.")
            return
        ticket[0] = new_name
        print("Name changed. Going back.")
        return ticket_list
    elif choice.strip() == '2':
        while True:
            search_for_showtime(showtime_list, screenings_list)
            new_showtime = input("Enter the new showtime code - 4 numbers 2 letters (or 'x' to go back). >>> ")
            spaces4()
            if new_showtime.lower().strip() == 'x':
                print("Taking you back.")
                return
            elif new_showtime not in [a_showtime[0] for a_showtime in showtime_list]:
                print("Invalid showtime code. Taking you a step back.")
                continue
            print("Since you have changed the showtime, you might need to change the seat"
                  " if the same seat in the new showtime is taken.")
            spaces4()
            if ticket[2] in [a_ticket[2] for a_ticket in ticket_list if a_ticket[1] == new_showtime]:
                print("The seat on the ticket is not available in the new showtime.")
                another_choice = input("If you want to change the seat for this new showtime, type '1' \nif you want "
                                       "to keep the old ticket (before change) type '2'. >>>  ")
                spaces4()
                if another_choice.strip() == '1':
                    for screening in screenings_list:
                        if screening[0] == ticket[1][0:4]:
                            an_auditorium = [auditorium for auditorium in auditoriums_list if
                                             screening[1] == auditorium[0]]
                            for a_showtime in showtime_list:
                                if a_showtime[0] == new_showtime:
                                    new_seat = display_seats(ticket_list, an_auditorium,
                                                             a_showtime, False)
                                    ticket[1] = new_showtime
                                    ticket[2] = new_seat
                                    if len(ticket) > 5:
                                        ticket[5] = screening[6]  # the price changes, price alterations do not apply
                                        print("The price has been changed accordingly. Discounts do not apply since the"
                                              "ticket has been changed. \nYou still have the option to cancel the "
                                              "reservation and make a new one.")
                                        spaces4()
                                    print("The reservation changed successfully. Going back.")
                                    return ticket_list
                elif another_choice.strip == '2':
                    spaces4()
                    print("Change cancelled. Taking you back.")
            else:
                print("The previous seat is available in the new showtime, so it will remain like so.")
            if ticket[4] == 'S':
                for screening in screenings_list:
                    if screening[0] == new_showtime[0:4]:
                        ticket[5] = screening[6]  # the price changes, price alterations do not apply
                        print("The price has been changed accordingly. Discounts do not apply since the"
                              "ticket has been changed. \nYou still have the option to cancel the "
                              "reservation and make a new one.")
            ticket[1] = new_showtime
            return ticket_list
    elif choice.strip() == '3':
        print("You will have a chance to change the seat you have.")
        exit_chance = input("In case you don't want to do this, type 'x' now (in any other "
                            "case you will have a chance to change the seat) >>>  ")
        spaces4()
        if exit_chance.strip().lower() == 'x':
            print('Taking you to the previous menu.')
            return
        new_ticket_list = ticket_list.copy()
        new_ticket_list.remove(ticket)  # so we don't display the old seat
        for a_ticket in ticket_list:
            if a_ticket == ticket:
                ticket_list.remove(a_ticket)
                for screening in screenings_list:
                    if screening[0] == ticket[1][0:4]:
                        an_auditorium = [auditorium for auditorium in auditoriums_list if
                                         screening[1] == auditorium[0]]
                        for a_showtime in showtime_list:
                            if a_showtime[0] == ticket[1]:
                                new_seat = display_seats(new_ticket_list, an_auditorium, a_showtime, False)
                                a_ticket[2] = new_seat
                                ticket_list.append(a_ticket)
                                print("Seat changed successfully. Going back.")
                                return ticket_list
    else:
        print("Invalid input. Please try again.")
        return


def delete_reservation(ticket_list, screenings_list, showtime_list, users_list, display_all):
    ticket = find_a_ticket(ticket_list, screenings_list, showtime_list, display_all)
    if ticket == 0:
        print("Since no reservation was chosen, this will take you back to the previous menu.")
        return 0
    confirmation = input("Are you sure you want to delete this reservation? (YES/NO) >>>>  ")
    spaces4()
    if confirmation.upper().strip() == "YES":
        if ticket[4] == 'R':
            print("Reservation deleted.")
            spaces4()
        elif ticket[4] == 'S' and len(ticket) > 5:
            print("Ticket un-sold. Going back. ")
        ticket_list.remove(ticket)
        return ticket_list, users_list
    print("The reservation isn't deleted. \nGoing back to the previous menu.")
    return


def sell_a_reserved_ticket(employees_username, ticket_list, screenings_list, showtime_list, users_list):
    ticket = find_a_ticket([a_ticket for a_ticket in ticket_list if a_ticket[4] == 'R'], screenings_list,
                           showtime_list, True)
    if ticket == 0:
        print("Since no reservation was chosen, this will take you back to the previous menu.")
        return 0
    elif ticket == 1:
        return 0
    print("Are you sure you want to sell this ticket? ")
    confirmation = input("Type YES or NO  >>>> ")
    spaces4()
    if confirmation.upper().strip() == 'YES':
        ticket[4] = "S"
        today = date.today()
        today_str = today.strftime("%d-%m-%Y")
        ticket[3] = today_str
        for screening in screenings_list:
            if screening[0] == ticket[1][0:4]:  # showtime code = screening code + xx
                price = float(screening[6])
                for a_showtime in showtime_list:
                    if a_showtime[0] == ticket[1]:
                        showtime_actual_date = datetime.strptime(a_showtime[1], '%d-%m-%Y')
                        if showtime_actual_date.weekday() == 1:
                            price -= 50
                            print("You have got a 50 RSD discount since the showtime is on a Tuesday! Yay!")
                        elif showtime_actual_date.weekday() == 5 or showtime_actual_date.weekday() == 6:
                            price += 50
                            print("Showtime on weekends cost 50 RSD more.")
                        if len(ticket[0].split(" ")) < 2:  # if it is in fact a username and not a first and last name
                            if loyalty_card_discount(ticket_list, ticket[0]):
                                price = price * 0.9  # 10% off for the loyalty card
                                print("Thanks to our loyalty card, you have a 10% off discount!")
                            # check if the showtime date is tuesday or weekend
                ticket.append(str(price))
                ticket.append(employees_username)
                print(f"Your ticket has been saved for a price of {price} RSD. Have a good day!")
                spaces4()
        return ticket_list, users_list
    return


def in_30_min_reservation_cancellation(tickets_list, showtime_list, screenings_list):   # also deletes past reservations
    print("Here are all the reservations (and ONLY  reservations, not sold tickets).")
    display_reservations([ticket for ticket in tickets_list if ticket[4] == 'R'], screenings_list, showtime_list)
    print("Now the reservations for the screenings that start in 30 minutes or less will be canceled. ")
    current_plus_30 = datetime.now() + timedelta(minutes=30)
    todays_date = date.today()
    modified_list = tickets_list.copy() # so we don't change the original through the iteration
    for ticket in tickets_list:
        for a_showtime in showtime_list:
            showtime_date = datetime.strptime(a_showtime[1], '%d-%m-%Y')
            if ticket[1] == a_showtime[0] and todays_date >= showtime_date.date():
                for screening in screenings_list:  # we will find the screening
                    if screening[0] == ticket[1][0:4] and ticket[4] == "R":
                        start_time = (showtime_date + timedelta(hours=int(screening[2][0:2])) +
                                      timedelta(minutes=int(screening[2][3:5])))
                        if current_plus_30 >= start_time:  # check if it starts in 30 or fewer minutes
                            modified_list.remove(ticket)
    spaces4()
    print("All reservations for the next 30 minutes have been deleted. Going back.")
    return modified_list


def search_through_tickets(tickets_list, screenings_list, showtime_list):
    while True:
        print("By which criteria do you want to search through tickets?")
        print("   1. Name (username)\n   2. Showtime code \n   3. Date of reservation\n   4. Starting time")
        print("   5. End time\n   6. Sold / Reserved?")
        choice = input("Type a number 1-6 or 'x' to go back.  >>> ")
        spaces4()
        print("Please be precise while searching if you want to see valid search results.")
        filtered_list = []
        if choice.lower().strip() == 'x':
            print("Taking you back to the previous menu.")
            return
        elif choice.strip() == '1' or choice.strip() == '2':
            value = input("Please enter the value you want to search for >>>  ")
            choice = int(choice) - 1
            for ticket in tickets_list:
                if ticket[choice] == value:
                    filtered_list.append(ticket)
        elif choice.strip() == '3':
            print("You will now have the chance to search for a specific date. Please use the format dd-mm-YY.")
            wanted_date = input("Please enter the day on which the reservation was made (or the ticket sold)  >>>  ")
            for ticket in tickets_list:
                if ticket[int(choice)] == wanted_date:
                    filtered_list.append(ticket)
        elif choice.strip() == '4' or choice.strip() == '5':
            print("Since you chose to search by the time of the screening, please follow the hh:mm format.")
            time_value = input("Please enter the value you're searching for >>> ")
            choice = int(choice) - 2
            for ticket in tickets_list:
                for screening in screenings_list:
                    if ticket[1][0:4] == screening[0]:
                        if screening[choice] == time_value:
                            filtered_list.append(ticket)
        elif choice.strip() == '6':
            option = input("Please enter R if you want to see reservations and S to see sold tickets >>>  ")
            for ticket in tickets_list:
                if ticket[4] == option.upper().strip():
                    filtered_list.append(ticket)
        else:
            print("Invalid input.")
            continue

        if filtered_list:
            display_reservations(filtered_list, screenings_list, showtime_list)
            return
        spaces4()
        print("Sorry, no tickets fulfil the criteria you entered.")
        return


def read_entity_to_list(file):  # nije korisceno u main-u, samo za probu za mene
    with open(file, "r+") as f:
        destination_list = [item.strip().split("|") for item in f.readlines()]
    return destination_list


if __name__ == "__main__":
    tickets = read_entity_to_list("tickets.txt")
    auditoriums = read_entity_to_list("auditoriums.txt")
    showtime = read_entity_to_list("showtime.txt")
    screenings = read_entity_to_list("screenings.txt")
    display_reservations(tickets, screenings, showtime)
