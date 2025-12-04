

import os 
import sqlite3
import pandas as pd
from typing import List, Dict

conn = sqlite3.connect("tunes.db")
df = pd.read_sql("SELECT * FROM tunes", conn)
conn.close()

 

books_dir = "abc_books"


#Parsing Functions
def parse_abc_file(file_path: str, book_number: int) -> List[Dict[str, str]]:

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
all_tunes = []
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
                tunes = parse_abc_file(file_path, int(item))
                for t in tunes:
                    print({
                        "book": t["book"],
                        "X": t["X"],
                        "title": t.get("title", ""),
                        "type": t.get("type", ""),
                        "key": t.get("key", "")
                    })
                




#Data Filtering
def get_tunes_by_book(df: pd.DataFrame, book_number: int)-> pd.DataFrame:
    return df[df["book"] == book_number]

def get_tunes_by_type(df: pd.DataFrame, tune_type:str)-> pd.DataFrame:
   
    return df[df["R"].str.lower() == tune_type.lower()]

def search_tunes(df: pd.DataFrame, search_term:str)-> pd.DataFrame:
    
    return df[df["T"].str.contains(search_term, case=False, na=False)]

#the function containing the interactive menu
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