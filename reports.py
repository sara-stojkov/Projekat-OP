# modul za sve izvestaje za menadzera

from prettytable import PrettyTable
from datetime import datetime, timedelta


def report_a(tickets_list, screenings_list):  # a. Lista prodatih karata za odabran datum prodaje karte
    while True:
        print("You will now see a report on all the tickets sold on a date of your choice. \nType x to go back. ")
        wanted_date = input("Enter the date for which you want to see the reports. (format: dd-mm-YY) >>>  ")
        print('-' * 30)
        if wanted_date.strip().lower() == 'x':
            print("Taking you back to the previous menu. ")
            return
        filtered_ticket_list = []
        for ticket in [a_ticket for a_ticket in tickets_list if a_ticket[4] == 'S']:
            if ticket[3] == wanted_date:
                filtered_ticket_list.append(ticket)

        columns = ['Name', 'Showtime code', 'Movie', 'Sold on', 'Price']
        (names_list, sh_code_list, movies_list, dates_list, prices_list) = ([], [], [], [], [])
        for ticket in filtered_ticket_list:
            if len(ticket) > 5:
                names_list.append(ticket[0])
                sh_code_list.append(ticket[1])
                dates_list.append(ticket[3])
                prices_list.append(ticket[5])
                for screening in screenings_list:
                    if ticket[1][0:4] == screening[0]:
                        # we found the screening that matches the showtime
                        movies_list.append(screening[5])

        mytable = PrettyTable()
        mytable.add_column(columns[0], names_list)
        mytable.add_column(columns[1], sh_code_list)
        mytable.add_column(columns[2], movies_list)
        mytable.add_column(columns[3], dates_list)
        mytable.add_column(columns[4], prices_list)

        if not names_list:
            print("No reservations to display. ")
            return
        print(mytable)
        save_to_a_txt_file(mytable, "List of tickets sold on the date chosen below.")
        return


def report_b(tickets_list, screenings_list, showtime_list):  # b. Lista prodatih karata za odabran datum termina bp
    while True:
        print("You will now see a report on all the tickets sold for a specific date of showtime.\n Type x to go back.")
        wanted_date = input("Enter the date for which you want to see the reports. (format: dd-mm-YY) >>>  ")
        print('-' * 30)
        if wanted_date.strip().lower() == 'x':
            print("Taking you back to the previous menu. ")
            return
        filtered_ticket_list = []
        for ticket in [a_ticket for a_ticket in tickets_list if a_ticket[4] == 'S']:
            for a_showtime in showtime_list:
                if a_showtime[0] == ticket[1] and a_showtime[1] == wanted_date:
                    filtered_ticket_list.append(ticket)

        columns = ['Name', 'Showtime code', 'Movie', 'Date of showtime', 'Price']
        (names_list, sh_code_list, movies_list, dates_list, prices_list) = ([], [], [], [], [])
        for ticket in filtered_ticket_list:
            if len(ticket) > 4:
                names_list.append(ticket[0])
                sh_code_list.append(ticket[1])
                prices_list.append(ticket[5])
                for screening in screenings_list:
                    if ticket[1][0:4] == screening[0]:
                        # we found the screening that matches the showtime
                        movies_list.append(screening[5])
                for a_showtime in showtime_list:
                    if ticket[1] == a_showtime[0]:
                        dates_list.append(a_showtime[1])

        mytable = PrettyTable()
        mytable.add_column(columns[0], names_list)
        mytable.add_column(columns[1], sh_code_list)
        mytable.add_column(columns[2], movies_list)
        mytable.add_column(columns[3], dates_list)
        mytable.add_column(columns[4], prices_list)

        if not names_list:
            print("No tickets to display. ")
            return
        print(mytable)
        save_to_a_txt_file(mytable, "List of tickets sold for a chosen date of showtime.")
        return


def report_c(tickets_list, screenings_list, users_dict):
    # c. Lista prodatih karata za odabran datum prodaje i odabranog prodavca.
    while True:
        print("You will now see a report on all the tickets sold on a specific date by the chosen employee. ")
        print("Type 'x' to go back.")
        wanted_date = input("Enter the date for which you want to see the reports. (format: dd-mm-YY) >>>  ")
        print('-' * 30)
        if wanted_date.strip().lower() == 'x':
            print("Taking you back to the previous menu. ")
            return
        employee_list = [username for username, user_info in users_dict.items() if user_info['role'] == '2']
        print(f"Please write one of the following: {employee_list} or 'x' to go back to the previous menu.")
        selected_employee = input("Enter the username of the employee you're drawing the report on. >>> ")
        if selected_employee.strip().lower() == 'x':
            print("Taking you back to the previous menu. ")
            return
        elif selected_employee not in employee_list:
            print("That username is not in our base. Try again. ")
            print('-' * 30)
            continue
        filtered_ticket_list = []
        for ticket in [a_ticket for a_ticket in tickets_list if a_ticket[4] == 'S']:  # search only through sold tickets
            if ticket[3] == wanted_date and ticket[-1] == selected_employee:
                filtered_ticket_list.append(ticket)

        columns = ['Name', 'Showtime code', 'Movie', 'Sold on', 'Price', 'Employee']
        (names_list, sh_code_list, movies_list, dates_list, prices_list, employees_list) = ([], [], [], [], [], [])
        for ticket in filtered_ticket_list:
            if len(ticket) > 4:
                names_list.append(ticket[0])
                sh_code_list.append(ticket[1])
                dates_list.append(ticket[3])
                prices_list.append(ticket[-2])
                employees_list.append(ticket[-1])
                for screening in screenings_list:
                    if ticket[1][0:4] == screening[0]:
                        # we found the screening that matches the showtime
                        movies_list.append(screening[5])

        mytable = PrettyTable()
        mytable.add_column(columns[0], names_list)
        mytable.add_column(columns[1], sh_code_list)
        mytable.add_column(columns[2], movies_list)
        mytable.add_column(columns[3], dates_list)
        mytable.add_column(columns[4], prices_list)
        mytable.add_column(columns[5], employees_list)

        if not names_list:
            print("No tickets to display. ")
            return
        print(mytable)
        save_to_a_txt_file(mytable, "List of tickets sold on a chosen date by a chosen employee.")
        return


def report_d(tickets_list):   # d. Ukupan broj i ukupna cena prodatih karata za izabran dan (u nedelji) prodaje.
    while True:
        print("You will now see a report on the total number and total price of all tickets sold on a chosen weekday.")
        print('-' * 30)
        weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        print(f"Please write one of the following: {weekdays} or 'x' to go back to the previous menu.")
        print("")
        chosen_weekday = input("Please enter the weekday you want to see the report on. >>>  ")
        print('-' * 30)
        if chosen_weekday.lower().strip() == 'x':
            print("Taking you back. ")
            return
        if chosen_weekday.title().strip() not in weekdays:
            print("Invalid weekday. Try again.")
            continue
        total_number = 0
        total_price = 0
        for ticket in [a_ticket for a_ticket in tickets_list if a_ticket[4] == 'S']:
            date_when_sold = datetime.strptime(ticket[3], '%d-%m-%Y')
            if date_when_sold.weekday() == weekdays.index(chosen_weekday.title()):
                total_number += 1
                total_price += float(ticket[5])

        columns = ['Weekday', 'Number of sold tickets', 'Total price']

        mytable = PrettyTable()
        mytable.add_column(columns[0], [chosen_weekday.title()])
        mytable.add_column(columns[1], [str(total_number)])
        mytable.add_column(columns[2], [str(total_price)])

        print(mytable)
        save_to_a_txt_file(mytable, "Total number and total sum of ticket prices sold on a chosen weekday.")
        return


def report_e(tickets_list, showtime_list):
    # e. Ukupan broj i ukupna cena prodatih karata za izabran dan (u nedelji) održavanja projekcije.
    while True:
        print("You will now see a report on the total number and total price of all tickets sold for a chosen weekday.")
        print('-' * 30)
        weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        print(f"Please write one of the following: {weekdays} or 'x' to go back to the previous menu.")
        print("")
        chosen_weekday = input("Please enter the weekday you want to see the report on. >>>  ")
        print('-' * 30)
        if chosen_weekday.lower().strip() == 'x':
            print("Taking you back. ")
        if chosen_weekday.title().strip() not in weekdays:
            print("Invalid weekday Try again.")
            continue
        total_number = 0
        total_price = 0
        for ticket in [a_ticket for a_ticket in tickets_list if a_ticket[4] == 'S']:
            for a_showtime in showtime_list:
                if a_showtime[0] == ticket[1]:  # finding the exact showtime
                    date_of_showtime = datetime.strptime(a_showtime[1], '%d-%m-%Y')
                    if date_of_showtime.weekday() == weekdays.index(chosen_weekday.title()):
                        total_number += 1
                        total_price += float(ticket[5])

        columns = ['Weekday', 'Number of tickets sold', 'Total price']

        mytable = PrettyTable()
        mytable.add_column(columns[0], [chosen_weekday.title()])
        mytable.add_column(columns[1], [str(total_number)])
        mytable.add_column(columns[2], [str(total_price)])

        print(mytable)
        save_to_a_txt_file(mytable, "Total number and total sum of ticket prices sold for a chosen weekday "
                                    "of showtime.")
        return


def report_f(tickets_list, screenings_list):  # f. Ukupna cena prodatih karata za zadati film u svim projekcijama
    while True:
        print("You will now choose a movie for which you will see the total income. Type x if you want to exit.")
        movie_name = input("Enter the name of the movie you want to check:  >>>  ")
        if movie_name.strip().lower() == 'x':
            print("Taking you back to the previous menu. ")
            return
        if movie_name.lower() not in [screening[5].lower() for screening in screenings_list]:
            print("There are no screenings nor showtime for that movie. Try again.")
            print("-" * 30)
            continue
        filtered_tickets = []
        print("-" * 30)
        choice = input("Do you want to see the final sum (1) or the sum for each screening (2)?  >>>  ")
        if choice.strip() == '1':
            for ticket in [a_ticket for a_ticket in tickets_list if a_ticket[4] == 'S']:
                for a_screening in screenings_list:
                    if ticket[1][0:4] == a_screening[0] and a_screening[5] == movie_name.title():
                        filtered_tickets.append(ticket)

            prices_sum = 0
            for single_ticket in filtered_tickets:
                prices_sum += float(single_ticket[5])

            columns = ['Movie name', 'Sum of ticket prices']

            mytable = PrettyTable()
            mytable.add_column(columns[0], [movie_name.title()])
            mytable.add_column(columns[1], [str(prices_sum)])

            print(mytable)
            save_to_a_txt_file(mytable, "Total sum of ticket prices for a chosen movie in all screenings.")
            return

        elif choice.strip() == '2':
            all_screenings = []
            for ticket in [a_ticket for a_ticket in tickets_list if a_ticket[4] == 'S']:
                for a_screening in screenings_list:
                    if ticket[1][0:4] == a_screening[0] and a_screening[5] == movie_name:
                        filtered_tickets.append(ticket)
                        all_screenings.append(a_screening)

            no_duplicates_screenings = []
            for single_screening in all_screenings:
                if single_screening not in no_duplicates_screenings:
                    no_duplicates_screenings.append(single_screening)   # removing duplicate screenings

            columns = ['Movie name', 'Screening code', 'Sum of ticket prices']
            (movie_name_list, screening_code_list, money_sum_list) = ([], [], [])

            for screening in no_duplicates_screenings:
                current_screening_sum = 0
                for ticket in filtered_tickets:
                    if ticket[1][0:4] == screening[0]:
                        current_screening_sum += float(ticket[5])
                screening_code_list.append(screening[0])
                movie_name_list.append(screening[5])
                money_sum_list.append(str(current_screening_sum))

            mytable = PrettyTable()
            mytable.add_column(columns[0], movie_name_list)
            mytable.add_column(columns[1], screening_code_list)
            mytable.add_column(columns[2], money_sum_list)

            if not movie_name_list:
                print("No sums to display. ")
                return
            print(mytable)
            save_to_a_txt_file(mytable, " ")
            return

        elif choice.lower().strip() == 'x':
            print("Going back.")
            return
        else:
            print("Invalid input. Try again.")
            continue


def report_g(tickets_list, users_dict):
    # g. Ukupan broj i ukupna cena prodatih karata za izabran dan prodaje i odabranog prodavca.
    while True:
        print("You will now see a report on the total number and total price of all tickets sold on a chosen weekday "
              "by a chosen employee.")
        print('-' * 30)
        weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        print(f"Please write one of the following: {weekdays} or 'x' to go back to the previous menu.")
        chosen_weekday = input("Please enter the weekday you want to see the report on. >>>  ")
        print('-' * 30)
        if chosen_weekday.lower().strip() == 'x':
            print("Taking you back. ")
            return
        elif chosen_weekday.title().strip() not in weekdays:
            print("Invalid weekday. Try again.")
            continue
        employee_list = [username for username, user_info in users_dict.items() if user_info['role'] == '2']
        print(f"Please write one of the following: {employee_list} or 'x' to go back to the previous menu.")
        chosen_employee = input("Please enter the username of the employee you want to draw the report up on. >>> ")
        if chosen_employee.lower().strip() == 'x':
            print("Going back.")
            return
        elif chosen_employee.lower() not in employee_list:
            print("Invalid username of an employee. Try again.")
            continue
        total_number = 0
        total_price = 0
        for ticket in [a_ticket for a_ticket in tickets_list if a_ticket[4] == 'S']:
            date_when_sold = datetime.strptime(ticket[3], '%d-%m-%Y')
            if date_when_sold.weekday() == weekdays.index(chosen_weekday.title()) and ticket[-1] == chosen_employee:
                total_number += 1
                total_price += float(ticket[5])

        columns = ['Weekday', 'Employee', 'Number of sold tickets', 'Total price']

        mytable = PrettyTable()
        mytable.add_column(columns[0], [chosen_weekday.title()])
        mytable.add_column(columns[1], [chosen_employee])
        mytable.add_column(columns[2], [str(total_number)])
        mytable.add_column(columns[3], [str(total_price)])

        print(mytable)
        save_to_a_txt_file(mytable, "Total number and total sum of tickets sold on a chosen weekday by "
                                    "the chosen employee.")
        return


def report_h(tickets_list, users_dict):
    # h. Ukupan broj i ukupna cena prodatih karata po prodavcima (za svakog prodavca) u poslednjih 30 dana.
    print("You will now see the total number of tickets and their total cost for each employee in the last 30 days.")
    last_30_days_tickets = []
    for ticket in [a_ticket for a_ticket in tickets_list if a_ticket[4] == 'S']:
        date_when_sold = datetime.strptime(ticket[3], '%d-%m-%Y')
        todays_date = datetime.today()
        today_minus30 = todays_date - timedelta(days=30)
        if today_minus30 <= date_when_sold:
            last_30_days_tickets.append(ticket)

    employee_list = [username for username, user_info in users_dict.items() if user_info['role'] == '2']
    (total_numbers_list, total_cost_list) = ([], [])
    for an_employee in employee_list:
        total_number = 0
        total_price = 0
        for a_ticket in last_30_days_tickets:
            if a_ticket[-1] == an_employee:
                total_number += 1
                total_price += float(a_ticket[-2])
        total_numbers_list.append(total_number)
        total_cost_list.append(total_price)

    columns = ['Employee', 'Total number of tickets sold', 'Total cost of those tickets']

    mytable = PrettyTable()
    mytable.add_column(columns[0], employee_list)
    mytable.add_column(columns[1], total_numbers_list)
    mytable.add_column(columns[2], total_cost_list)

    print(mytable)
    save_to_a_txt_file(mytable, "Total number of tickets and total sum of their prices for each employee "
                                "(in the last 30 days).")
    return


def save_to_a_txt_file(a_table, report_name):
    print("Do you want to save this report into a text file?")
    yes_no = input("Enter YES if you do or enter NO if you don't.  >>>>  ")
    print('-' * 30)
    if yes_no.upper().strip() == 'YES':
        file_name = input("Please enter the name of the file you want to save it as (the .txt extension will be added "
                          "automatically). >>>> ")
        print('-' * 30)
        file_path = file_name + '.txt'
        todays_actual_date = datetime.today()
        todays_date = datetime.strftime(todays_actual_date, "%d-%m-%Y")
        with open(file_path, 'w') as f:
            f.write(f"{report_name}\n")
            f.write(f"Report drawn up on {todays_date}.\n")
            f.write(str(a_table))
        print("File saved successfully. Going back.")
        return
    print("Taking you to the previous menu.")
    return
