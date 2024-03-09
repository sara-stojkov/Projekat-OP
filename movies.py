# .py fajl sa funkcijama vezanim za filmove

from prettytable import PrettyTable  # library which will be used


def spaces2():
    print("-" * 30)


def new_movie(list_of_movies):  # adding a new movie t o the list of movies
    movie_names = [movie[0] for movie in list_of_movies]
    this_movie = []
    while True:
        name = input("Enter the name of the movie (or x to exit):  ")
        if len(name) < 1 or len(name) > 30:
            print("Invalid input. Try at least 2 characters and no more than 30. ")
            continue
        elif name.title() in movie_names:
            print("This movie is already in our database. Try another name.")
            continue
        elif name == 'x':
            return
        this_movie.append(name)
        genres = []  # an empty list used for all genres
        while True:  # a movie can have multiple genres
            genre = input("Enter the genre:  ")
            all_genres = ['romance', 'comedy', 'horror', 'thriller', 'kids', 'psychological', 'documentary',
                          'historical', 'action', 'biographical', 'drama', 'adventure', 'fantasy', 'action',
                          'superhero', 'sci-fi', 'mystery', 'tragedy', 'mythology', 'crime']
            if genre.lower().strip() not in all_genres:
                print("Invalid genre. Choose one of the following: ")
                print(all_genres)
                spaces2()
                continue
            genres.append(genre.lower().strip())
            finished = input("Have you entered all the genres you wanted?  (YES/NO)  ")
            if finished.lower() == "yes":
                this_movie.append(genres)
            elif finished.lower() == "no":
                continue
            else:
                print("Invalid input. Try again.")
                continue
            while True:
                try:
                    duration = int(input("Enter movie duration:  "))
                    if duration < 10:
                        print("Short films are for youtube not cinemas. Try again.")
                        continue
                    this_movie.append(duration)
                except ValueError:
                    print("Please enter a valid number.")
                    continue
                while True:
                    directors = input("Enter the director(s) (separated by a space):  ")
                    lead_actors = input("Enter lead actors (separated by a space):  ")
                    country = input("Enter the country where the movie is from:  ")
                    this_movie.append(directors)
                    this_movie.append(lead_actors)
                    this_movie.append(country)
                    while True:
                        try:
                            year = int(input("Year of publishing:  "))
                            if year > 2024 or year < 1900:
                                print("Are you sure? Try again. ")
                                continue
                            this_movie.append(year)
                        except ValueError:
                            print("Please enter a valid number. Try again.")
                            continue
                        while True:
                            summary = input("Short description:   ")
                            if len(summary) > 120:
                                print("Please shorten the description.")
                                continue
                            this_movie.append(summary)
                            this_movie.append("True")
                            list_of_movies.append(this_movie)
                            print("Movie added successfully.")
                            return list_of_movies


def delete_a_movie(list_of_movies, list_of_screenings):
    list_of_movie_names = [movie[0] for movie in list_of_movies]
    while True:
        movie_name = input("Enter the name of the movie you want to delete (or type 'x' to exit).  ")
        spaces2()
        if movie_name.strip().lower() == "x":
            return
        elif movie_name not in list_of_movie_names:
            print("This movie does not exist in the database.")
            continue
        else:
            index_of_movie = list_of_movie_names.index(movie_name)  # we will need the index of the movie
            while True:
                confirmation = input("Are you sure?  (YES/NO) >>> ")
                if confirmation.strip().lower() == "yes":
                    list_of_movies[index_of_movie][8] = "False"  # not entirely deleting data of previous movies
                    print("Movie deleted. Going back.")
                    spaces2()
                    print("All screenings for this movie were also deactivated. \nTheir showtime won't be generated "
                          "in the future, but showtimes already generated will still play out.")
                    for screening in list_of_screenings:
                        if screening[5] == movie_name:
                            screening[-1] = 'False'  # 'deleting' all related screenings
                    return list_of_movies, list_of_screenings
                elif confirmation.strip().lower() == "no":
                    print("Going back then.")
                    return
                else:
                    print("That was not valid input. Try again.")
                    continue


def create_a_list(original_list, an_index, specific_list):  # original list us a list of lists
    if an_index < len(original_list):
        for item in original_list:
            specific_list.append(item[an_index])
    return specific_list


def all_movies(movies_list):  # function that displays all movies for the user using the pretty tables library
    columns = ['Name', 'Genre', 'Duration', 'Director(s)', 'Lead actor(s)', 'Country', 'Year',
               'Short description']
    names_list, genres_list, durations_list, directors_list, leads_list, countries_list, years_list, summaries_list = (
        [], [], [], [], [], [], [], [])
    for movie in movies_list:
        if len(movie) > 8 and movie[8] == "True":  # displaying only available movies
            names_list.append(movie[0])
            if isinstance(movie[1], list):
                genres_list.append(",".join(movie[1]))
            else:
                genres_list.append(movie[1])
            durations_list.append(movie[2])
            directors_list.append(movie[3])
            leads_list.append(movie[4])
            countries_list.append(movie[5])
            years_list.append(movie[6])
            summaries_list.append(movie[7])

    mytable = PrettyTable()

    mytable.add_column(columns[0], names_list)  # first column consists of movie names and so on
    mytable.add_column(columns[1], genres_list)
    mytable.add_column(columns[2], durations_list)
    mytable.add_column(columns[3], directors_list)
    mytable.add_column(columns[4], leads_list)
    mytable.add_column(columns[5], countries_list)
    mytable.add_column(columns[6], years_list)
    mytable.add_column(columns[7], summaries_list)

    if not movies_list:
        print("No movies to display. ")
        return
    print(mytable)


def duration_options(code, list_of_movies):
    while True:
        print("You have chosen to filter the movies by duration.")
        print("You will now have the choice of how exactly you want to filter the movies.")
        print("  1. Maximum length\n  2. Minimum length\n  3. Time interval\n  X. to exit")
        choice2 = input("Type the code of the option you want.   ")
        if choice2.strip().lower() == "x":
            return
        try:
            choice2 = int(choice2)
            if choice2 == 1:
                choice3 = int(input("Type the value you want to check. The app will display movies shorter "
                                    "than what you enter.  "))
                return filtered_search(code, choice3, list_of_movies, choice2)
            elif choice2 == 2:
                choice3 = int(input("Type the value you want to check. The app will display movies longer than "
                                    "what you enter.  "))
                return filtered_search(code, choice3, list_of_movies, choice2)
            elif choice2 == 3:
                choice21 = int(input("Type the lower limit. The movies displayed will be longer than this.   "))
                return filtered_search(code, choice21, list_of_movies, choice2)
            else:
                print("Invalid option. Please try again.")
        except ValueError:
            print("Invalid input. Please try again.")
            spaces2()
            continue


def pre_filtered_search(list_of_movies):
    while True:
        spaces2()
        print("Please choose a category:")
        print("  1. Name \n  2. Genre \n  3. Duration \n  4. Director \n  5. Lead actor")
        print("  6. Country\n  7. Year of publishing ")
        code = input("Which criteria do you want?  (or write 'x' to go back)  ")
        spaces2()
        if code.lower().strip() == "x":
            print("Going back.")
            return
        if code.strip() in ["1", "2", "4", "5", "6", "7"]:
            choice = input("Enter the value of the criteria you have chosen to check.  ")
            spaces2()
            time_interval = 0
            return filtered_search(code, choice, list_of_movies, time_interval)
        elif code.strip() == "3":
            return duration_options(code, list_of_movies)
        else:
            print("Not valid input. Try again. ")
            continue


def filtered_search(code, value, movies_list, time_interval):  # code and choice are previously input
    code = int(code) - 1
    filtered_list = []
    # 0 - name, 1 - genre, 2 - duration, 3 - director, 4 - lead actor,
    # 5 - country, 6 - year, 7 - summary
    if code == 0:  # searching a name of the movie
        movie_names = [movie[code].lower().split() for movie in movies_list]
        for movie_name in movie_names:
            choices = value.split()
            for choice in choices:
                if choice.lower() in movie_name and movies_list[movie_names.index(movie_name)] not in filtered_list:
                    filtered_list.append(movies_list[movie_names.index(movie_name)])
    elif code == 1:  # searching a genre
        for movie in movies_list:
            if value.lower().strip() in movie[code].lower():
                filtered_list.append(movie)
    elif code == 2:
        if time_interval == 1:
            for movie in movies_list:
                if int(movie[code]) <= value:
                    filtered_list.append(movie)
        elif time_interval == 2:
            for movie in movies_list:
                if int(movie[code]) >= value:
                    filtered_list.append(movie)
        elif time_interval == 3:
            value2 = int(input("Type the upper limit. The movies displayed will be shorter than this.  "))
            try:
                value2 = int(value2)
                for movie in movies_list:
                    if value2 >= int(movie[code]) >= value:
                        filtered_list.append(movie)
            except ValueError:
                print("Please type a valid integer.")
                return filtered_list
        else:
            print("Looks like a mistake. Try again. ")
    elif code == 3 or code == 4:
        for a_movie in movies_list:
            if value.title() in a_movie[code].split() and a_movie not in filtered_list:
                filtered_list.append(a_movie)
    elif code == 5 or code == 6:
        for movie in movies_list:
            if movie[code].lower() == value.lower():
                filtered_list.append(movie)
    if not filtered_list:  # if the list is empty
        print("Sorry, no movies fulfil that criteria.")
    return filtered_list


def interception_of_lists(bigger_list, smaller_list):
    if not smaller_list:
        return smaller_list
    return [item for item in bigger_list if item in smaller_list]  # list of common elements


def multivariate_search(data_list):
    filtered_final = data_list
    print("You will now choose the criteria you want and enter the values you want to search for.")
    spaces2()
    name_q = input("Do you want to search by name? (YES/NO)  ")
    if name_q.lower().strip() == "yes":
        name = input("Enter the name you want to search for: ")
        filtered_list = filtered_search(1, name, filtered_final, 0)
        filtered_final = interception_of_lists(filtered_final, filtered_list)
    spaces2()
    genre_q = input("Do you want to search by genre? (YES/NO)  ")
    if genre_q.lower().strip() == "yes":
        genre = input("Enter the genre you want to search for: ")
        filtered_list = filtered_search(2, genre, filtered_final, 0)
        filtered_final = interception_of_lists(filtered_final, filtered_list)
    spaces2()
    duration_q = input("Do you want to search by duration? (YES/NO)  ")
    if duration_q.lower().strip() == "yes":
        filtered_list = duration_options(3, filtered_final)
        filtered_final = interception_of_lists(filtered_final, filtered_list)
    spaces2()
    directors_q = input("Do you want to search by director(s)? (YES/NO)  ")
    if directors_q.lower().strip() == "yes":
        directors = input("Enter the director you want to search for: ")
        filtered_list = filtered_search(4, directors, filtered_final, 0)
        filtered_final = interception_of_lists(filtered_final, filtered_list)
    spaces2()
    actors_q = input("Do you want to search by lead actor(s)? (YES/NO)  ")
    if actors_q.lower().strip() == "yes":
        actors = input("Enter the actor you want to search for: ")
        filtered_list = filtered_search(5, actors, filtered_final, 0)
        filtered_final = interception_of_lists(filtered_final, filtered_list)
    spaces2()
    country_q = input("Do you want to search by country? (YES/NO)  ")
    if country_q.lower().strip() == "yes":
        country = input("Enter the country you want to search for: ")
        filtered_list = filtered_search(6, country, filtered_final, 0)
        filtered_final = interception_of_lists(filtered_final, filtered_list)
    spaces2()
    year_q = input("Do you want to search by year? (YES/NO)  ")
    if year_q.lower().strip() == "yes":
        year = input("Enter the year you want to search for: ")
        filtered_list = filtered_search(7, year, filtered_final, 0)
        filtered_final = interception_of_lists(filtered_final, filtered_list)
    spaces2()

    if not filtered_final:  # checks if the list is empty
        print("No movies fulfil the criteria.\nGoing back to the main menu. ")
    else:
        no_duplicates = []
        [no_duplicates.append(item) for item in filtered_final if item not in no_duplicates]
        if no_duplicates == data_list:
            print("It looks like no filters were applied. Here are all the movies: ")
            all_movies(no_duplicates)
        else:
            all_movies(no_duplicates)


def edit_movie(movies_list):
    while True:
        movie_name = input("Enter the name of the movie you want to edit (or type 'x' to exit).  ")
        if movie_name == "x":
            return
        movie_names = [movie[0] for movie in movies_list]
        if movie_name not in movie_names:
            print("That movie name is not valid. Try again. ")
        print("Choose what you want to edit in a movie:")
        print("  1. Genre\n  2. Duration\n  3. Director(s)\n  4. Lead actors\n  5. Country\n  6. Year")
        code = input("Enter the number of the thing you want to edit or type 'x' to exit.  ")
        if code == "x":
            return
        code = int(code)
        if code == 2:
            print("The duration is important because of all the show times and screenings. You can't change this.")
            print("If you really messed up, you can still delete this movie and create a new one.")
            return
        new_data = input("Enter the new value of the aspect you chose to edit (or 'x' to exit):  ")
        spaces2()
        if new_data.lower().strip() == 'x':
            print("Going back.")
            return
        movies_list[movie_names.index(movie_name)][code] = new_data
        print("Change made successfully, going back now.")
        return movies_list


def read_file_into_list(file_name):
    with open(file_name, "r+") as f:
        list_of_lists = []
        for line in f.readlines():
            list_of_lists.append(line.strip().split("|"))
    return list_of_lists


def write_a_file_from_lists(file_name, data_list):
    with open(file_name, "w") as g:
        for item in data_list:
            item = [str(elem) if not isinstance(elem, list) else ",".join(map(str, elem)) for elem in item]
            # converts every item of list into a string for the .join function and also deals with lists
            g.write("|".join(item) + '\n')
    return file_name


if __name__ == "__main__":
    movies = []
    read_file_into_list('movies.txt')
    movie_list = [movie[0] for movie in movies]
    if movies:
        all_movies(movies)
    else:
        print("No movies to display.")
    new_movie(movies)
    write_a_file_from_lists("movies.txt", movies)   # ovo je bilo za probu
