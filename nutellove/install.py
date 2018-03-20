"""
Script tailored to assists users in easily downloading a file through CLI,
initializing a MySQL db and populating it.

OpenFoodFacts DB Seeker 0.1
"""

# coding: utf8

import os.path

from colorama import init
from termcolor import colored

from csv_cleaner import *
from constants import *
from db_feeding import *


init()  # inits colorama


class InstallMenu():
    """
    InstallMenu object, helps the user to get everything he needs to
    use the OpenFoodFacts csv to db program.
    """

    def __init__(self):
        print()
        print("-" * 56)
        print("*" * 56)
        print(
            """Welcome ! This script is tailored to assist you
through the installation of OpenFoodFacts DB Seeker !""".upper()
        )
        print("*" * 56)
        print("-" * 56)
        self.main_menu()

    def main_menu(self):
        """
        Main menu of the app.
        Asks what the user wants to do.
        """
        print()
        print("*" * 50)
        print("Main menu".upper().center(50))
        print("*" * 50)
        print("1 - Clean CSV File.")
        print("2 - Create MySQL database.")
        print("3 - Populate MySQL database.")
        print("0 - Quit.")
        print()
        print("Input your choice: ")
        try:
            answer = input(" >> ")

            if answer in self.main_menu_actions.keys():
                self.main_menu_actions[answer](self)

            else:
                print()
                print("!" * 31)
                print("Please, input a valid choice.")
                print("!" * 31)
                self.main_menu_actions['main_menu'](self)

        except KeyboardInterrupt as keyinter:
            print("See you, then! :)")
            exit()

    def quit(self):
        """
        Quits the app with a message.
        """
        print("Bye bye!")
        exit()

    def clean_file(self):
        # clean the csv file
        try:
            csv_file = CSVCleaner(CSV_FNAME)
            csv_file.csv_cleaner(
                HEADERS_LIST,
                CATEGORIES_LIST,
                COUNTRIES_LIST,
            )
            print()
            print(colored("File cleaned!", "green"))
            print()
            self.main_menu_actions['main_menu'](self)

        except Exception as e:
            print(e)
            self.main_menu_actions['main_menu'](self)

    def create_db(self):
        """
        Creates the database using the config file
        """
        # manage.py makemigrations
        # manage.py migrate

    def populate_db(self):
        """
        Populates the db from a csv file.
        """
        print()
        print("Filling database... Please wait...")
        try:
            dbf = DBFeed(CLEANED_CSV_FILE, HEADERS_LIST)
            dbf.fill_categories("main_category_fr")
            dbf.fill_stores("stores")
            dbf.fill_brands("brands")
            dbf.fill_products()

            print()
            print(colored(
                "Database filled! You can now use menu.py to use the app.",
                "green")
            )
            print()
            self.main_menu_actions['main_menu'](self)

        except Exception as e:
            print(e)
            self.main_menu_actions['main_menu'](self)

    """
    Main menu actions, used to quickly access some funcs
    """
    main_menu_actions = {
        'main_menu': main_menu,
        '1': clean_file,
        '2': create_db,
        '3': populate_db,
        '0': quit,
    }


if __name__ == "__main__":
    install = InstallMenu()
