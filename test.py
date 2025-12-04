import sqlite3
import pandas as pd
from main import get_tunes_by_book, get_tunes_by_type, search_tunes

# Load database
conn = sqlite3.connect("tunes.db")
df = pd.read_sql("SELECT * FROM tunes", conn)
conn.close()


