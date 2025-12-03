# Starter code for Data Centric Programming Assignment 2025

# os is a module that lets us access the file system

# Bryan Duggan likes Star Trek
# Bryan Duggan is a great flute player

import os 
import sqlite3
import pandas as pd
import mysql.connector
conn = sqlite3.connect("tunes.db")
df = pd.read_sql("SELECT * FROM tunes", conn)
conn.close()
# sqlite for connecting to sqlite databases

# An example of how to create a table, insert data
# and run a select query

def my_sql_database():
    conn = mysql.connector.connect(host="localhost", user="root", database="tunepal")
    
    cursor = conn.cursor()
    cursor.execute("select * from tuneindex")
    
    
    while True:
        row = cursor.fetchone()
        if not row:
            break
        else:
            print(row)
    # results = cursor.fetchall()
    
    

    # Print results
    for row in results:
        print(row)    
    conn.close()
    

books_dir = "abc_books"

def process_file(file):
    with open(file, 'r') as f:
        lines = f.readlines()
    # list comprehension to strip the \n's
    lines = [line.strip() for line in lines]

    # just print the files for now
    for line in lines:
        # print(line)
        pass


# my_sql_database()
# do_databasse_stuff()

# Iterate over directories in abc_books
for item in os.listdir(books_dir):
    # item is the dir name, this makes it into a path
    item_path = os.path.join(books_dir, item)
    
    # Check if it's a directory and has a numeric name
    if os.path.isdir(item_path) and item.isdigit():
        print(f"Found numbered directory: {item}")
        
        # Iterate over files in the numbered directory
        for file in os.listdir(item_path):
            # Check if file has .abc extension
            if file.endswith('.abc'):
                file_path = os.path.join(item_path, file)
                print(f"  Found abc file: {file}")
                process_file(file_path)
def parse_abc_file(file_path, book_number):
    tunes= []
    current_tune = None
    current_tune_notation = ""
    with open(file_path, "r", encoding ='latin-1') as f:
        lines = f.readlines()
    for line in lines:    
        line = line.strip()
        if line.startswith("X:"):
            if current_tune:
                current_tune["notation"] = current_tune_notation
                tunes.append(current_tune)
            current_tune = {"book": book_number, "X": line[2:].strip()}
            current_tune_notation = line + "\n"
        elif current_tune:
            if line.startswith("T:"):
                current_tune["title"] = line[2:].strip()
            elif line.startswith("R:"):
                current_tune["type"] = line[2:].strip()
            elif line.startswith("K:"):
                current_tune["key"] = line[2:].strip()
            current_tune_notation += line + "\n"            
    if current_tune:
        current_tune["notation"] = current_tune_notation
        tunes.append(current_tune)
    
    return tunes

def diction_maker(folder_path):
    all_tunes = []
    for file_name in os.listdir(folder_path):
        if file_name.lower().endswith(".abc"):
            file_path = os.path.join(folder_path, file_name)
            print("Parsing:", file_path)
            tunes = parse_abc_file(file_path)
            all_tunes.extend(tunes)
    return all_tunes
def do_databasse_stuff():

    conn = sqlite3.connect('tunes.db')
    cursor = conn.cursor()

    # Create table
    cursor.execute('CREATE TABLE IF NOT EXISTS users (name TEXT, age INTEGER)')

    # Insert data
    cursor.execute('INSERT INTO users (name, age) VALUES (?, ?)', ('John', 30))

    # Save changes
    conn.commit()

    cursor.execute('SELECT * FROM users')

    
    results = cursor.fetchall()

    
    for row in results:
        print(row)    
        print(row[0])
        print(row[1])
    # Close
    
    df = pd.read_sql("SELECT * FROM users", conn)
    print(df.head())
    conn.close()

def get_tunes_by_book(df, book_number):
    return df[df["book"] == book_number]

def get_tunes_by_type(df, tune_type):
    # case-insensitive match
    return df[df["R"].str.lower() == tune_type.lower()]

def search_tunes(df, search_term):
    # case-insensitive search in titles
    return df[df["T"].str.contains(search_term, case=False, na=False)]


def tunes_menu(df):
    while True:
        print("\n--- Tunes Menu ---")
        print("1 = Get tunes by book")
        print("2 = Get tunes by type")
        print("3 = Search tunes by title")
        print("4 = Quit")

        choice = input("Enter your choice: ")

        if choice == "1":
            book_number = input("Enter book number: ")
            try:
                book_number = int(book_number)
                results = get_tunes_by_book(df, book_number)
                if len(results) == 0:
                    print("No tunes found.")
                else:
                    print(results[["book", "T", "R"]])
            except:
                print("Please enter a number.")

        elif choice == "2":
            tune_type = input("Enter tune type (e.g., Reel, Jig): ")
            results = get_tunes_by_type(df, tune_type)
            if len(results) == 0:
                print("No tunes found.")
            else:
                print(results[["book", "T", "R"]])

        elif choice == "3":
            search_term = input("Enter search term in title: ")
            results = search_tunes(df, search_term)
            if len(results) == 0:
                print("No tunes found.")
            else:
                print(results[["book", "T", "R"]])

        elif choice == "4":
            print("Goodbye!")
            break

        else:
            print("Invalid choice, try again.")


tunes_menu(df)