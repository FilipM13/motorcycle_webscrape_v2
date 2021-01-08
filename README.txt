# motorcycle_webscrape_v2
This is a web scraping project. Goal is to search for specific motorcycles on olx website and save offers to database.
Main technology is Python with MySQL database (requires MySQL installed on machine).

Features:
main_automatic (.exe and .py)- script that can be run with task manager with default search entries.
main_manual_cmd (.exe and .py)- script that run in cmd that enables user to input search entries manually.
tools.py - small package of tools programmed by me to complete this project.
test.py - manual tests for tools.py functions.
read (.exe and .py)- script that run in cmd that enables user to fetch data from database

test.py will be uploaded soon.

Upgrade ideas:
-more filters (entries) for searching
-GUI
-integrating read and main_manual_cmd into one script
-running database in cloud for easy access (doesn't require local MySQL)

Some of challanges:
-web scraping
-database architecture and running MySQL queries (basic)
-testing
-creating user-resistant CMD interface (blocking errors as much as possible)

Things to fix:
-CMD malfunctioning
-merging read and main_manual_cmd
-complete restructuring of read and main_manual_cmd (creating version 3.0):
	-more flexible templates (such as 'ask' function in tools.py)
	-general template for both scripts
-exploring possibilities of OOP might be helpful