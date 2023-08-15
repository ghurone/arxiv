import sqlite3 as sq
import threading

thread_local = threading.local()

def get_connection():
    if not hasattr(thread_local, "connection"):
        thread_local.connection = sq.connect('dataset/astro.sql')
        
    return thread_local.connection

def get_cursor():
    if not hasattr(thread_local, "cursor"):
        thread_local.cursor = get_connection().cursor()
        
    return thread_local.cursor  

def get_article(index:int):
    cur = get_cursor()
    cur.execute(f'SELECT id, title, abstract FROM astro WHERE "index" = {index}')
    return cur.fetchone()