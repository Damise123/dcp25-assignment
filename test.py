import sqlite3
import pandas as pd
from main import get_tunes_by_book, get_tunes_by_type, search_tunes

# Load database
conn = sqlite3.connect("tunes.db")
df = pd.read_sql("SELECT * FROM tunes", conn)
conn.close()

# Test a few functions
print(get_tunes_by_book(df, 1).head())      # First 5 tunes in book 1
print(get_tunes_by_type(df, "Reel").head()) # First 5 Reels
print(search_tunes(df, "Whiskey").head())   # First 5 tunes with 'Whiskey' in title

