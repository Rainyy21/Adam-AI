import sqlite3
import discord
import pathlib
from discord.ext import commands

FOLDER = "database"
DB_FILE = "infractions.db"
DB_PATH = pathlib.Path(FOLDER) / DB_FILE

# =====================================================
# make the db base if it doesn't exist
# =====================================================

def initialize_db():
    pathlib.Path(FOLDER).mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS rude_counts (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            count INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()
    return
        
# ===================================================
# this will add people to the db if they curse
# ===================================================

def add_infractions(user_id, username):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute("SELECT count FROM rude_counts WHERE user_id = ?",(user_id,))
    result = c.fetchone()
    
    if result: 
        new_cont = result[0] + 1
        c.execute(
            "UPDATE rude_counts SET count = ?, username = ? WHERE user_id = ?", 
            (new_cont, username, user_id)
        )
    else:
        c.execute(
            "INSERT INTO rude_counts (user_id, username, count) VALUES (?, ?, ?)", 
            (user_id, username, 1)
        )
    conn.commit()
    conn.close()
    return

# ==============================================
# get the top 5 bad people 
# ==============================================
def get_top_infractions(limit=5):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute(f"""
              SELECT user_id , username, count
              FROM rude_counts
              ORDER BY count DECS
              LIMIT ?
              """,(limit,))
    
    top_users = c.fetchall()
    conn.close()
    return top_users