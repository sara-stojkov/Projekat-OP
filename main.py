# Sara Stojkov, SV38/2023
# Odbrana (predrok)
from movies import (new_movie, all_movies, read_file_into_list, write_a_file_from_lists, delete_a_movie,
                    pre_filtered_search, edit_movie, multivariate_search)

from projections import search_for_showtime, new_screening, delete_screening, edit_screening, generate_showtime

from tickets import (make_reservation_buy, display_reservations, delete_reservation, sell_a_reserved_ticket,
                     in_30_min_reservation_cancellation, search_through_tickets, edit_a_reservation)

from reports import report_a, report_b, report_c, report_d, report_e, report_f, report_g, report_h


def spaces():
    print("-" * 30)
    return


def valid_password(password):
    if len(password) <= 6:
        print("The password is too short.")
        return False
    if not any(i.isdigit() for i in password):
        print("The password needs to contain at least 1 numeric digit.")
        return False
    return True


def confirm_identity(a_username):
    while True:
        password = input("Enter the password:  ")
        spaces()
        if a_username in users.keys() and password == users[a_username]['password']:
            print("You have confirmed your identity.")
            return True
        elif a_username in users.keys() and password != users[a_username]['password']:
            print("Wrong password. Try again.")
            continue
        elif a_username not in users.keys():
            print("Username doesn't exist in the system. Try again.")
            spaces()
            return


def register_user(role_code):
    # (x) will be the code for each role: 1 - customer, 2 - employee, 3 - manager
    while True:
        spaces()
        username: str = input("Enter the username (or type 'x' to go back):  ")
        if username.lower() == "x":
            spaces()
            print("You have chosen to exit. You will be taken back to the main menu.")
            return
        elif len(username) < 3:
            print("That is way too short for a username. Try again.")
            continue
        elif username in users.keys():
            print("That username has already been used. Try another one.")
            continue
        elif len(username.split(" ")) > 1:
            print("The username has to be only one word. Try using _ or . if you want.")
            continue
        password1 = input("Enter the password (at least 7 characters long, contains a number): ")
        password2 = input("Confirm the password: ")
        # checking the password
        if valid_password(password1) and password1 == password2:
            first_name = input("Enter first name: ")
            last_name = input("Enter last name: ")
            if len(first_name) < 1 or len(last_name) < 1:
                print("Sorry, seems like you didn't enter a valid first or last name. Try again.")
            else:
                print("Registration successful.")
                spaces()
                # the user can be registered
                new_user = {'username': username, 'password': password1, 'role': role_code, 'first name': first_name,
                            'last name': last_name + '\n'}
                users[username] = new_user
                write_a_file_from_dictionary("users.txt", users)
                new_user = input("Do you want to register another user? (YES/NO) ")
                if new_user.upper() == "YES":
                    spaces()
                    print("You will be taken to the register page again. ")
                else:
                    print("You will be taken back.")
                    return users
        elif password1 != password2:
            print("The passwords don't match. Try again.")
        else:
            print("The password needs to contain a numeric digit. Try again.")


def login():
    while True:
        spaces()
        username = input("Write your username (type 'x' to exit):  ")
        if username.lower().strip() == "x":
            spaces()
            print("This will take you back.")
            return
        password = input("Write your password:  ")
        spaces()
        if username in users.keys() and password == users[username]['password']:
            print("You have been successfully logged in.")
            if users[username]['role'] == "1":
                menu_level1(username)
            elif users[username]['role'] == "2":
                menu_level2(username)
            elif users[username]['role'] == "3":
                menu_level3()
            return
        elif username in users.keys() and password != users[username]['password']:
            print("Wrong password. Try again.")
        if username not in users.keys():  # this function is True if the username is in the system
            print("This username does not exist in the system. Try again.")


def edit_info():
    username = input("Enter the username (type 'x' to go back):  ")
    if username.lower().strip() == "x":
        return
    if confirm_identity(username):
        print("1 - Password;  2 - First Name;  3 - Last Name")
        while True:
            choice = input("What do you want to edit? (Enter a number 1-3 or type x to exit) ")
            spaces()
            if choice == "x":
                return
            try:
                choice = int(choice)
                if 1 <= choice <= 3:
                    while True:
                        change = input("Enter the new value (or x to exit):  ")
                        if change.lower().strip() == "x":
                            print("Going back to the previous menu.")
                            return
                        change1 = input("Confirm, write it again:  ")
                        spaces()
                        if change == change1 and len(change) >= 3:
                            if choice == 1:
                                if valid_password(change):
                                    users[username]['password'] = change
                                else:
                                    print("You will be taken back.")
                                    return
                            elif choice == 2:
                                users[username]['first name'] = change
                            elif choice == 3:
                                users[username]['last name'] = change + '\n'  # we have to add \n so it doesn't
                                # connect to the next user while writing it out
                            print("Personal data changed successfully. You will be returned to the previous menu.")
                            return users
                        elif change != change1:
                            print("The data you entered doesn't match. Please correct that.")
                            spaces()
                        else:
                            print("Seems like that text is too short. Going back.")
            except ValueError:
                print("Invalid input. Try again.")
                spaces()
                continue


def main_menu():
    while True:
        spaces()
        print("Welcome to Sara's cinemas. This is the main menu.\nChoose one of the options below:")
        print("1. Create a new account or log into your own. (recommended for more options)")
        print("2. Check all the available movies.")
        print("3. Filter your search for a movie. ")
        print("4. Have a look at the movies being shown. ")
        print("x. Exit the application. ")
        print("In case you want to make a reservation without registering, call our front desk at +381 61 234567 or "
              "come in person.")
        print("~~~ We are open every day from 1PM until 12AM at Bulevar oslobođenja 32a, 21000 Novi Sad ~~~")
        spaces()
        choice = input("Enter the code (number 1-4) of the functionality which you want or type 'x' to exit:  ")
        spaces()
        if choice == "1":
            choice2 = input("Do you already have an account? (YES / NO)  ")
            if choice2.upper() == "YES":
                login()
            elif choice2.upper() == "NO":
                register_user("1")
            else:
                print("Sorry, that is not valid input. You will be returned to the main menu.")
        elif choice == "2":
            print("You have chosen option 2. You can now look at all the available movies.")
            all_movies(movies)
        elif choice == "3":
            print("You have chosen option 3. You can filter your search.")
            spaces()
            print("Do you want to search by one or by multiple criteria? ")
            choice3 = input("Type 1 for one and 'M' for multiple - or 'x' to exit.  ")
            if choice3.strip().lower() == 'x':
                spaces()
                print("You have chosen to go back.")
                continue
            elif choice3.strip() == "1":
                all_movies(pre_filtered_search(movies))
            elif choice3.upper().strip() == "M":
                multivariate_search(movies)
            else:
                print("Invalid input. Taking you back.")
        elif choice == "4":
            print("You have chosen option 4. You can now look at available movie screenings.")
            search_for_showtime(showtime, screenings)
        elif choice.lower().strip() == "x":
            print("The application will close.")
            spaces()
            return users
        else:
            print("Sorry, that was not a valid input. Try again.")


def menu_level1(username):
    while True:
        spaces()
        print(f"Hello {username}. Hope you're having a good day!")
        print("Your options are: ")
        print("1. Change your account information.")
        print("2. Make a reservation.")
        print("3. Take a look at all your reservations (or cancel them).")
        print("4. Check all the available movies.")
        print("5. Filter your search for a movie. ")
        print("6. Have a look at the movies being shown. ")
        print("x. Log out (back to the main menu).")
        choice = input("Write the number of the option you want (1-6) or type 'x' to log out.  ")
        spaces()
        if choice == "1":
            edit_info()
        elif choice == "2":
            print("Keep in mind that on Tuesdays all movies cost 50 RSD less and on weekends they cost 50 RSD more.")
            spaces()
            while True:
                print("You can now make a reservation. ")
                print("First, you will have the option to search for specific showtime, since you'll need the code.")
                x = search_for_showtime(showtime, screenings)
                if x == 0:
                    break
                make_reservation_buy(username, 0, showtime, screenings, tickets, auditoriums, "R", users)
                another = input("Type YES if you want to make another reservation or NO if you want to go back. >>>  ")
                if another.upper().strip() == 'YES':
                    continue
                break
        elif choice == "3":
            while True:
                x = display_reservations([ticket for ticket in tickets if ticket[0] == username and ticket[4] == 'R'],
                                         screenings, showtime)
                if x != 0:
                    print("Do you want to cancel some of these reservations?")
                    q_cancel = input("Type YES to cancel some reservations or NO to go back >>> ")
                    if q_cancel.upper().strip() == "YES":
                        while True:
                            spaces()
                            x = delete_reservation(tickets, screenings, showtime, users, False)
                            if x == 0:
                                break
                            another_cancellation = input("Do you want to cancel more tickets? Type YES or NO >>>> ")
                            if another_cancellation.upper().strip() == "YES":
                                print("Taking you back to the beginning of cancelling a reservation.")
                                continue
                            break
                    spaces()
                    print("Taking you back to the previous menu, then.")
                    break
                spaces()
                print("Since you have no reservations currently, this will take you back.")
                break
        elif choice == "4":
            print("You can now check out all available movies. ")
            all_movies(movies)
        elif choice == "5":
            print("You have chosen option 5. You can filter your search for movies.")
            spaces()
            print("Do you want to search by one or by multiple criteria? ")
            choice3 = input("Type 1 for one and 'M' for multiple - or 'x' to exit.  ")
            if choice3.strip().lower() == 'x':
                spaces()
                print("You have chosen to go back.")
                continue
            elif choice3.strip() == "1":
                all_movies(pre_filtered_search(movies))
            elif choice3.upper().strip() == "M":
                multivariate_search(movies)
            else:
                print("Invalid input. Taking you back.")
        elif choice.lower().strip() == "6":
            search_for_showtime(showtime, screenings)
        elif choice.lower().strip() == "x":
            print("You have been logged out.")
            return users
        else:
            print("Invalid input. You will be taken back. ")


def menu_level2(username):
    global tickets
    while True:
        spaces()
        print("Hello, dear employee!")
        spaces()
        print(" Here are your options:")
        print("1. Edit your account information.")
        print("2. Make a reservation or sell a ticket to a customer.")
        print("3. Sell a seat that has been reserved.")
        print("4. Take a look at the reservations, cancel them or change them.")
        print("5. Search through the tickets.")
        print("6. Check all the available movies.")
        print("7. Filter your search for a movie. ")
        print("8. Have a look at the movies being shown. ")
        print("9. Cancel the reservations 30 minutes before the showtime. ")
        print("x. Log out (back to the main menu).")
        option = input("Choose an option (1-9) or type 'x' to log out and go back to the main menu. ")
        spaces()
        if option.lower().strip() == "x":
            print("You have been logged out.")
            return users
        elif option == "1":
            edit_info()
        elif option == "2":
            print("Before doing anything notify the customer that showtime on weekends costs 50 RSD more and on "
                  "Tuesdays it's 50 RSD less.")
            spaces()
            while True:
                print("Do you want to make reservation on someone's behalf (R) or sell a ticket directly (S)?")
                choice = input("Type R or S. (or 'x' to go back) >> ")
                spaces()
                if choice.lower().strip() == 'x':
                    print("Going back to the previous menu.")
                    break
                if choice.upper().strip() == "R":
                    # check if the username exists in the system
                    print("The ticket is bound either to someone's username (registered users) or to their first and "
                          "last name (unregistered users).")
                    while True:
                        name = input("Please enter the username or the first and last name of the person the "
                                     "reservation's for (or 'x' to exit):  >>>  ")
                        if name.lower().strip() == 'x':
                            spaces()
                            print("Going back. ")
                            break
                        if len(name.split(" ")) < 2 and name not in list(users.keys()):
                            print("That username is not in our system. Try again.")
                            spaces()
                            continue
                        x = search_for_showtime(showtime, screenings)
                        if x != 0:
                            make_reservation_buy(name, username, showtime, screenings, tickets, auditoriums, "R", users)
                        break
                elif choice.upper().strip() == "S":
                    print("The ticket is bound either to someone's username (registered users) or to their first and "
                          "last name (unregistered users).")
                    while True:
                        name = input("Please enter the username or the first and last name of the person the "
                                     "ticket's for (or 'x' to exit):  >>>  ")
                        if name.lower().strip() == 'x':
                            spaces()
                            print("Going back. ")
                            break
                        if len(name.split(" ")) < 2:
                            if name not in list(users.keys()):
                                print("That username is not in our system. Try again.")
                                continue
                        x = search_for_showtime(showtime, screenings)
                        if x != 0:
                            make_reservation_buy(name, username, showtime, screenings, tickets, auditoriums, "S", users)
                        break
        elif option == "3":
            while True:
                a = sell_a_reserved_ticket(username, tickets, screenings, showtime, users)
                if a == 0:
                    break
                another = input("Do you want to sell another ticket? Type YES if you do or NO to go back. >>>  ")
                if another.upper().strip() == 'YES':
                    continue
                break
        elif option == "4":
            print("  1. See all reservations \n  2. Cancel a reservation \n  3. Change a reservation")
            choice = input("Enter 1, 2 or 3 (or 'x' to go back).  >> ")
            if choice.lower().strip() == 'x':
                print("Going back to the previous menu.")
                continue
            elif choice.strip() == '1':
                display_reservations(tickets, screenings, showtime)
                continue
            elif choice.strip() == '2':
                print("You will now have a chance to cancel a particular reservation.")
                while True:
                    delete_reservation(tickets, screenings, showtime, users, True)
                    another_cancellation = input("Do you want to cancel more tickets? Type YES or NO >>>> ")
                    if another_cancellation.upper().strip() == "YES":
                        print("Taking you back to the beginning of cancelling a reservation.")
                        spaces()
                        continue
                    break
                continue
            elif choice.strip() == '3':
                edit_a_reservation(tickets, screenings, showtime, auditoriums)
            else:
                print("Invalid input. Taking you back to the previous menu.")
        elif option == "5":
            search_through_tickets(tickets, screenings, showtime)
        elif option == "6":
            print("You can now check out all available movies. ")
            all_movies(movies)
        elif option == "7":
            print("You have chosen option 5. You can filter your search for movies.")
            spaces()
            print("Do you want to search by one or by multiple criteria? ")
            choice3 = input("Type 1 for one and 'M' for multiple - or 'x' to exit.  ")
            if choice3.strip().lower() == 'x':
                spaces()
                print("You have chosen to go back.")
                continue
            elif choice3.strip() == "1":
                all_movies(pre_filtered_search(movies))
            elif choice3.upper().strip() == "M":
                multivariate_search(movies)
            else:
                print("Invalid input. Taking you back.")
        elif option.strip() == "8":
            search_for_showtime(showtime, screenings)
        elif option.strip() == '9':
            tickets = in_30_min_reservation_cancellation(tickets, showtime, screenings)
        else:
            print("Invalid input. Try again.")


def menu_level3():
    global showtime
    while True:
        spaces()
        print("Hello manager! Here are your options:")
        print("1. Edit your personal data.")
        print("2. Register a new employee or a manager.")
        print("3. Check all the available movies.")
        print("4. Alter the available movies - add a new movie, delete or edit an existing one.")
        print("5. Filter your search for a movie. ")
        print("6. Have a look at the movies being shown. ")
        print("7. Alter the available screenings - add, edit or delete.")
        print("8. See the reports.")
        print("9. GENERATE THE SHOWTIME")
        print("x. Log out (back to the main menu).")
        option = input("Choose one of the options above or type 'x' to go back. ")
        spaces()
        if option == "1":
            edit_info()
        elif option == "2":
            choice = input("Do you want to register a manager or an employee? (M/E) ")
            if choice.upper() == "M":
                register_user("3")
            elif choice.upper() == "E":
                register_user("2")
            else:
                print("Seems like that is not M or E, please try again.")
        elif option == "3":
            all_movies(movies)
        elif option == "4":
            choice = input("Enter 'N' if you want to add a new movie\nEnter 'D' to delete an existing one\n"
                           "Enter 'E' to edit a movie \nor 'x' to go back.  ")
            if choice.lower().strip() == 'x':
                spaces()
                print("Going to the previous menu.")
                continue
            if choice.lower().strip() == "n":
                print("You have chosen to enter a new movie.")
                spaces()
                new_movie(movies)
            elif choice.lower().strip() == "d":
                print("You have chosen to delete a movie. ")
                spaces()
                delete_a_movie(movies, screenings)
            elif choice.lower().strip() == "e":
                print("You have chosen to edit a movie. ")
                spaces()
                edit_movie(movies)
            else:
                print("Invalid input. Try again.")
                continue
        elif option.strip() == "5":
            print("You have chosen option 6. You can filter your search for movies.")
            spaces()
            print("Do you want to search by one or by multiple criteria? ")
            choice3 = input("Type 1 for one and 'M' for multiple -  or 'x' to go back.  ")
            if choice3.strip().lower() == "x":
                print("Going back.")
                return
            elif choice3.strip() == "1":
                pre_filtered_search(movies)
                all_movies(filtered_list)
            elif choice3.upper().strip() == "M":
                multivariate_search(movies)
            else:
                print("Invalid input. Taking you back.")
        elif option.lower().strip() == "6":
            search_for_showtime(showtime, screenings)
        elif option.lower().strip() == "7":
            choice = input("Enter 'N' if you want to add a new screening\nEnter 'D' to delete an existing one\n"
                           "Enter 'E' to edit a screening \nor 'x' to go back.  ")
            if choice.lower().strip() == 'x':
                spaces()
                print("Going to the previous menu.")
                continue
            if choice.lower().strip() == "n":
                print("You have chosen to enter a new screening.")
                spaces()
                new_screening(movies, screenings)
            elif choice.lower().strip() == "d":
                print("You have chosen to delete a movie. ")
                spaces()
                delete_screening(screenings, showtime)
            elif choice.lower().strip() == "e":
                print("You have chosen to edit a movie. ")
                spaces()
                edit_screening(screenings, movies, showtime)
            else:
                print("Invalid input. Try again.")
                continue
        elif option.strip() == "8":
            print("Which report do you want to see?")
            print("  a. List of tickets sold on a chosen date.")
            print("  b. List of tickets sold for a specific date od showtime.")
            print("  c. List of tickets sold on a chosen date and by a chosen employee.")
            print("  d. Total number and total cost of tickets sold on a specific weekday.")
            print("  e. Total number and total cost of tickets sold for a specific showtime weekday.")
            print("  f. Total cost of all tickets sold for a chosen movie in all screenings.")
            print("  g. Total number and total cost of all tickets sold on a chosen date and by a chosen employee.")
            print("  h. Total number and total cost of sold tickets for each employee in the last 30 days.")
            choice = input("Type a letter A-H or 'x' to go back. >>>  ")
            spaces()
            if choice.lower().strip() == 'x':
                print("Going back to the previous menu.")
                continue
            elif choice.lower().strip() == 'a':
                report_a(tickets, screenings)
            elif choice.lower().strip() == 'b':
                report_b(tickets, screenings, showtime)
            elif choice.lower().strip() == 'c':
                report_c(tickets, screenings, users)
            elif choice.lower().strip() == 'd':
                report_d(tickets)
            elif choice.lower().strip() == 'e':
                report_e(tickets, showtime)
            elif choice.lower().strip() == 'f':
                all_movies(movies)
                report_f(tickets, screenings)
            elif choice.lower().strip() == 'g':
                report_g(tickets, users)
            elif choice.lower().strip() == 'h':
                report_h(tickets, users)
            else:
                print("Invalid input. Please try again.")
                continue

        elif option.lower().strip() == "9":
            print("You will now have to choice to generate the showtime for the near future. ")
            spaces()
            new_showtime = generate_showtime(screenings, showtime)
            adding_into_a_file("showtime.txt", new_showtime)
            showtime = read_file_into_list("showtime.txt")
            continue
        elif option.lower().strip() == "x":
            print("You have been logged out. Going back. ")
            return users
        else:
            print("Invalid input. Try again. ")


def read_users(file_name, destination_dictionary):
    with open(file_name, "r+") as f:
        for line in f.readlines():
            "\n".strip(line)
            a_split_list = line.split('|')
            if len(a_split_list) == 6:   # customers and employees will also have tracked money spent or earned
                single_entity = {'username': a_split_list[0], 'password': a_split_list[1], 'role': a_split_list[2],
                                 'first name': a_split_list[3], 'last name': a_split_list[4]}
            else:
                single_entity = {'username': a_split_list[0], 'password': a_split_list[1], 'role': a_split_list[2],
                                 'first name': a_split_list[3], 'last name': a_split_list[4]}
            destination_dictionary[a_split_list[0]] = single_entity
    return destination_dictionary


def write_a_file_from_dictionary(file_name, data_dictionary):
    with open(file_name, "w") as g:
        for specific_data in list(data_dictionary.keys()):
            list(data_dictionary.keys())[-1] += '\n'
            a_line = '|'.join(list(data_dictionary[specific_data].values()))
            g.write(a_line)
    return file_name


def adding_into_a_file(file_path, list_of_lists):
    with open(file_path, 'a') as f:
        for item in list_of_lists:
            f.write("|".join(item) + '\n')
    return file_path


if __name__ == "__main__":
    users = {}
    read_users("users.txt", users)
    movies = read_file_into_list("movies.txt")
    filtered_list = []
    screenings = read_file_into_list("screenings.txt")
    auditoriums = read_file_into_list("auditoriums.txt")
    tickets = read_file_into_list("tickets.txt")
    showtime = read_file_into_list("showtime.txt")
    main_menu()
    write_a_file_from_dictionary("users.txt", users)
    write_a_file_from_lists("movies.txt", movies)
    write_a_file_from_lists("screenings.txt", screenings)
    write_a_file_from_lists("auditoriums.txt", auditoriums)
    write_a_file_from_lists("tickets.txt", tickets)
