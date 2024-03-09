# .py fajl gde su funkcije vezane za projekcije i termine projekcija

from datetime import datetime, timedelta, date

from prettytable import PrettyTable  # library which will be used
from movies import all_movies


def spaces3():
    print("-" * 30)
    return


def valid_time(weekdays, start, end, auditorium_code, existing_screenings):
    for weekday in weekdays:
        for screening in existing_screenings:
            if weekday in screening[4]:  # if they happen on the same day
                if auditorium_code == screening[1]:  # if they are in the same auditorium
                    if (int(screening[2][0:2])) <= int(start[0:2]) <= (int(screening[3][0:2])):
                        return False  # we are focusing purely on the hours part of each time:
                        # this will return false if the hour of the new time is between the starting
                        # hour of the start of some screening or the hour of the ending
                    if (int(screening[2][0:2])) <= int(end[0:2]) <= (int(screening[3][0:2])):
                        return False
    return True


def new_screening(list_of_movies, list_of_screenings):
    print("You will now be able to add a new screening.")
    spaces3()
    movie_names = [movie[0] for movie in list_of_movies]
    screening_codes = [screening[0] for screening in list_of_screenings]
    code = int(screening_codes[-1]) + 1
    while True:
        all_movies(list_of_movies)
        movie_name = input("Which movie is being shown?  ")
        spaces3()
        if movie_name not in movie_names:
            print("Sorry, we don't have this movie. Going back.")
            spaces3()
            continue
        elif list_of_movies[movie_names.index(movie_name)][8] == "False":
            print("This movie is not available anymore. Please try again. ")
            spaces3()
            continue
        else:
            while True:
                start_time = input("Start of the screening (hours:minutes):  ")
                spaces3()
                try:
                    start_t = datetime.strptime(start_time, "%H:%M")
                    end_t = start_t + timedelta(minutes=int(list_of_movies[movie_names.index(movie_name)][2]))
                    end_time = str(end_t.time())[0:5]
                    all_auditoriums = read_entity_to_list("auditoriums.txt")
                    auditorium_names = [auditorium[0] for auditorium in all_auditoriums]
                    while True:
                        print(f"The available auditoriums are: {auditorium_names}")
                        auditorium = input("Where will the movie be shown?  (type the name of the auditorium)  ")
                        spaces3()
                        try:
                            if auditorium in auditorium_names:
                                print("Valid input.")
                                spaces3()
                        except Exception:
                            print("Try again. That is not a valid name. ")
                            continue
                        all_weekdays = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
                        print(f"You will now be able to choose one of the following weekdays: {all_weekdays}")
                        chosen_weekdays = []
                        while True:
                            spaces3()
                            weekday = input("Which day in the week will this movie be shown? (type 'x' when done)  ")
                            weekday = weekday.strip().lower()
                            if weekday == "x":
                                spaces3()
                                if not valid_time(chosen_weekdays, start_time, end_time, auditorium,
                                                  list_of_screenings):
                                    print("Seems like the auditorium is not available at the time you wanted.")
                                    print("Taking you back.")
                                    return
                                try:
                                    price = float(input("Enter the price of this screening:  "))
                                    spaces3()
                                    chosen_weekdays = ",".join(chosen_weekdays)
                                    another_screening = [code, auditorium, start_time, end_time,
                                                         chosen_weekdays, movie_name, price, 'True']
                                    list_of_screenings.append(another_screening)
                                    print("Screening added successfully. \nPlease generate the showtime accordingly.")
                                    return list_of_screenings
                                except ValueError:
                                    print("That is not a valid number. Try again. ")
                            elif weekday in all_weekdays and weekday not in chosen_weekdays:
                                chosen_weekdays.append(weekday)
                                print("Weekday added. Going back.")
                                continue
                            elif weekday in chosen_weekdays:
                                print("This weekday has already been added. Try again.")
                                continue
                            else:
                                print("That is not valid input. Try again. ")
                                continue

                except ValueError:
                    print("Sorry, that is not a valid input. Try again. ")


def edit_screening(list_screenings, list_movies, showtime_list):
    scr_codes_list = [screening[0] for screening in list_screenings]
    while True:
        display_showtime(showtime_list, list_screenings)
        spaces3()
        print("Now, note that the first four digits in the column code are the code of the screening.")
        print("You can change everything about a screening except for the code.")
        choice = input("Enter the code (first four digits) of the screening you want to edit (or x to exit):  ")
        spaces3()
        if choice.lower().strip() == 'x':
            print("Taking you back.")
            return
        elif len(choice) == 4 and choice in scr_codes_list:
            a_screening = list_screenings[scr_codes_list.index(choice)]
            print("Be mindful that changing the time or place of screening may cause some overlaps. \nThe app will "
                  "prevent you from doing so, but it is best to take that into account.")
            spaces3()
            if a_screening[0] == choice:
                print(" 1. Auditorium   2. Start time   3. Weekday   4. Movie   5. Price")
                option = input("What do you want to edit? (enter a number 1-5 or 'x' to exit)  ")
                spaces3()
                if option.lower().strip() == 'x':
                    return
                elif option.strip() == "5":
                    try:
                        new_price = float(input("The new price:  "))
                        a_screening[6] = new_price
                        print("Value changed successfully.")
                        print("Please notify the customers who have tickets for this screening in the future. ")
                        return list_screenings
                    except ValueError:
                        print("Try again, that was not a valid number.")
                elif option.strip() in ["1", "2", "3", "4"]:  # for these we need to check the availability
                    if option.strip() == "1":
                        new_value = input("Enter the new value of the option you chose:  ")
                        all_auditoriums = read_entity_to_list("auditoriums.txt")
                        auditorium_names = [auditorium[0] for auditorium in all_auditoriums]
                        if new_value not in auditorium_names:
                            print("Sorry, that is not a name of the auditorium we have.")
                        else:
                            a_screening[1] = new_value
                            print("The change was made successfully! ")
                            spaces3()
                            print("Please notify the customers who have tickets for this screening in the future. ")
                            return list_screenings
                    elif option.strip() == "2":
                        movie_names = [movie[0] for movie in list_movies]
                        start_time = input("New start of the screening (hours:minutes):  ")
                        spaces3()
                        try:
                            start_t = datetime.strptime(start_time, "%H:%M")
                            start_time = str(start_t.time())[0:5]
                            end_t = start_t + timedelta(minutes=int(list_movies[movie_names.index(a_screening[5])][2]))
                            end_time = str(end_t.time())[0:5]
                            a_screening[2] = start_time
                            a_screening[3] = end_time
                            print("The change was made successfully! ")
                            spaces3()
                            print("Please notify the customers who have tickets for this screening in the future. ")
                            return list_screenings
                        except ValueError:
                            print("Sorry, that is not a valid input. Try again. ")
                    elif option.strip() == "4":
                        movie_names = [movie[0] for movie in list_movies]
                        movie_name = input("Enter the new movie:  ")
                        spaces3()
                        if movie_name not in movie_names:
                            print("Sorry, we don't have this movie. Going back.")
                            spaces3()
                            continue
                        elif list_movies[movie_names.index(movie_name)][8] == "False":
                            print("This movie is not available anymore. Please try again. ")
                            spaces3()
                            continue
                        else:
                            # we also need to change the ending time because of the different duration
                            a_screening[5] = movie_name
                            start_t = datetime.strptime(a_screening[2], "%H:%M")
                            end_t = start_t + timedelta(minutes=int(list_movies[movie_names.index(a_screening[5])][2]))
                            end_time = str(end_t.time())[0:5]
                            a_screening[3] = end_time
                            print("The change was made successfully! ")
                            spaces3()
                            print("Please notify the customers who have tickets for this screening in the future. ")
                            return list_screenings
                    elif option.strip() == "3":
                        all_weekdays = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
                        print(f"You will now be able to choose one of the following weekdays: {all_weekdays}")
                        chosen_weekdays = []
                        while True:
                            spaces3()
                            weekday = input("Which day in the week will this movie be shown? (type 'x' when done)  ")
                            weekday = weekday.strip().lower()
                            if weekday == "x":
                                spaces3()
                                if not valid_time(chosen_weekdays, a_screening[2], a_screening[3], a_screening[1],
                                                  list_screenings):
                                    print("Seems like the auditorium is not available at the time you wanted.")
                                    print("Taking you back.")
                                    return
                                a_screening[4] = str(chosen_weekdays).join(',')
                                spaces3()
                                print("Change successful! Going back. ")
                                spaces3()
                                print("Please notify the customers who have tickets for this screening in the future. ")
                                return list_screenings
                            elif weekday in all_weekdays and weekday not in chosen_weekdays:
                                chosen_weekdays.append(weekday)
                                print("Weekday added. Going back.")
                                continue
                            elif weekday in chosen_weekdays:
                                print("This weekday has already been added. Try again.")
                                continue
                            else:
                                print("That is not valid input. Try again. ")
                                continue
        else:
            print("That was not valid input. Taking you back.")
            continue


def delete_screening(list_screenings, showtime_list):
    scr_codes_list = [screening[0] for screening in list_screenings]
    print("You will now have a chance to delete (cancel) a screening. ")
    print("First, you will see the whole repertoire.")
    display_showtime(showtime_list, list_screenings)
    spaces3()
    print("Now, note that the first four digits in the column code are the code of the screening.")
    while True:
        scr_code = input("Enter the code of the screening you want to cancel or type 'x' to go back.  ")
        spaces3()
        if scr_code.lower().strip() == 'x':
            print("Going back to the previous menu.")
            return
        elif len(scr_code) == 4 and scr_code in scr_codes_list:
            a_screening = list_screenings[scr_codes_list.index(scr_code)]
            print("Screening found.")
            confirmation = input("Type YES if you are sure you want to delete this screening.  >>")
            if confirmation.upper().strip() == 'YES':
                a_screening[-1] = "False"
                print("Screening removed. The existing (generated) show times will still play out.")
                print("You might want to generate the showtime again.")
                return list_screenings, showtime_list
            else:
                print("Going back.")
                return
        else:
            print("Invalid input. Try again, check the codes in the table.")


def search_for_showtime(showtime_list, list_of_screenings):
    while True:
        spaces3()
        print("By which criteria do you want to search for a showtime?")
        print("  1. Date\n  2. Auditorium\n  3. Starting time\n  4. Ending time\n  5. Movie name")
        criteria = input("Enter the number of the option you want or '0' to see everything (type 'x' to go back):  ")
        spaces3()
        filtered_list_sh = []  # showtime
        if criteria.isdigit():
            if criteria == "0":
                print("You will now see all the available showtime in the next 2 weeks.")
                display_showtime([a_showtime for a_showtime in showtime_list if datetime.today() + timedelta(weeks=2) >=
                                  datetime.strptime(a_showtime[1], "%d-%m-%Y") + timedelta(hours=23)],
                                 list_of_screenings)
                return
            elif criteria == "1":  # searching by date
                while True:
                    a_date = input("The date you're searching for (date-month-year):  ")
                    try:
                        date_actually = datetime.strptime(a_date, "%d-%m-%Y")
                        for a_showtime in showtime_list:
                            if date_actually == datetime.strptime(a_showtime[1], "%d-%m-%Y"):
                                filtered_list_sh.append(a_showtime)
                        display_showtime(filtered_list_sh, list_of_screenings)
                        return
                    except ValueError:
                        print("That doesn't seem to be valid. Try again.")
                        spaces3()
                        continue
            elif 2 <= int(criteria) <= 5:  # searching by an auditorium, start or end time, or movie name
                value = input("Please enter the value of the criteria you want to find:  ")
                for a_showtime in showtime_list:
                    screening_code = a_showtime[0][0:4]  # we need only the first four digits
                    for screening in list_of_screenings:
                        if screening[0] == screening_code:
                            if int(criteria) in [2, 3, 4]:
                                if screening[int(criteria) - 1] == value:
                                    filtered_list_sh.append(a_showtime)
                            elif int(criteria) == 5:
                                if screening[int(criteria)].lower() == value.lower():
                                    filtered_list_sh.append(a_showtime)
                display_showtime(filtered_list_sh, list_of_screenings)
                return
            else:
                print("Invalid option.")
        elif criteria.lower().strip() == 'x':
            print("Going back to the previous menu.")
            spaces3()
            return 0
        else:
            print("Invalid input, type a number. Try again.")
            continue


def display_showtime(list_of_showtime, list_of_screenings):
    if not list_of_showtime:  # no need to start the function if the list is empty
        print("No movies to display. ")
        return
    columns = ['Date', 'Code', 'Weekday', 'Movie', 'Starting time', 'Ending time', 'Auditorium', 'Price']
    dates_list, codes_list, weekdays_list, movies_list, starts_list, ends_list, auditoriums_list, prices_list = (
        [], [], [], [], [], [], [], [])
    for a_showtime in list_of_showtime:
        if datetime.today() <= datetime.strptime(a_showtime[1], "%d-%m-%Y") + timedelta(hours=23):
            # not showing old show times, we add 23 hours, so we show all the show times today
            codes_list.append(a_showtime[0])  # saving the code for selling tickets later
            dates_list.append(a_showtime[1])  # saving a date
            exact_date = datetime.strptime(a_showtime[1], "%d-%m-%Y")
            weekdays_list.append(exact_date.strftime('%A'))  # adds the name of the weekday
            screening_code = a_showtime[0][0:4]  # that is the screening code, first 4 digits
            for screening in list_of_screenings:
                if screening[0] == screening_code:  # we need to find the exact screening
                    if len(screening) > 6:
                        auditoriums_list.append(screening[1])
                        starts_list.append(screening[2])  # starting time
                        ends_list.append(screening[3])  # starting time
                        movies_list.append(screening[5])  # movie name
                        prices_list.append(screening[6])  # price of the ticket

    t = PrettyTable()
    t.add_column(columns[0], dates_list)  # first column consists of dates and so on
    t.add_column(columns[1], codes_list)
    t.add_column(columns[2], weekdays_list)
    t.add_column(columns[3], movies_list)
    t.add_column(columns[4], starts_list)
    t.add_column(columns[5], ends_list)
    t.add_column(columns[6], auditoriums_list)
    t.add_column(columns[7], prices_list)

    print(t)


def generate_showtime(list_screenings, list_showtime):
    while True:
        showtime_list = []
        weeks_number = int(input("How many weeks from today do you want to generate? (or '0' to go back.)  "))
        if not type(weeks_number) == int or weeks_number > 4:
            print("Invalid input. Try again.")
            continue
        elif weeks_number == 0:
            return

        today = date.today()
        last_date = today + timedelta(weeks=weeks_number)
        final_date = last_date.strftime("%d-%m-%Y")
        print(f"The dates of the screenings will be generated for up until {final_date}.")

        list_of_dates = [today + timedelta(days=i) for i in range((last_date - today).days + 1)]

        last_showtime_codes = {}
        for screening_code in set([a_screening[0] for a_screening in list_screenings]):
            matching_showtimes = [s[0] for s in showtime_list if s[0].startswith(screening_code)]
            if matching_showtimes:  # we need to check all the existing showtime for a screening
                last_showtime_code = max(matching_showtimes)
                last_showtime_codes[screening_code] = last_showtime_code[4:6]
            else:
                last_showtime_codes[screening_code] = 'AA'  # if there aren't any showtimes, we start from AA

        for a_screening in list_screenings:
            weekdays = a_screening[4].split(",")
            current_code = last_showtime_codes.get(a_screening[0], 'AA')

            for a_date in list_of_dates:
                if len(current_code) >= 2:
                    if current_code[1] > 'Z':
                        current_code = chr(ord(current_code[0]) + 1) + 'A'

                for weekday in weekdays:
                    if a_date.strftime('%A') == weekday.title():
                        showtime_code = str(a_screening[0]) + current_code
                        single_showtime = [showtime_code, a_date.strftime("%d-%m-%Y")]
                        existing_codes = [a_showtime[0] for a_showtime in list_showtime]
                        if showtime_code not in existing_codes and a_screening[-1] == 'True':
                            # since deleted screenings will have 'False' as their last element,
                            # we don't want to generate them for the future
                            showtime_list.append(single_showtime)
                        current_code = current_code[0] + chr(ord(current_code[1]) + 1)
        spaces3()
        print("Showtime generation successful. Going back. ")
        return showtime_list


def read_entity_to_list(file):  # nije korisceno u main-u, samo za probu za mene
    with open(file, "r+") as f:
        destination_list = [item.strip().split("|") for item in f.readlines()]
    return destination_list


def write_a_file_from_lists(file_name, data_list):
    with open(file_name, "w") as g:
        for item in data_list:
            item = [str(elem) if not isinstance(elem, list) else ",".join(map(str, elem)) for elem in item]
            # converts every item of list into a string for the .join function and also deals with lists
            g.write("|".join(item) + '\n')
    return file_name


if __name__ == "__main__":
    screenings = read_entity_to_list("screenings.txt")
    showtime = read_entity_to_list("showtime.txt")
    display_showtime(showtime, screenings)
    new_showtime = generate_showtime(screenings, showtime)
    showtime = showtime + new_showtime
    display_showtime(showtime, screenings)
    write_a_file_from_lists("showtime.txt", showtime)
