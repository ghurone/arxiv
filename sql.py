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
    cur.execute(f'SELECT id, title, abstract, strftime("%Y-%m-%d", date) FROM astro WHERE "index" = {index}')
    return cur.fetchone()


def get_index_articles(i_year, f_year):
    cur = get_cursor()
    cur.execute(f'SELECT "index" FROM astro WHERE date BETWEEN "{i_year}-01-01" AND "{f_year}-12-31";')
    return cur.fetchall()

def year_range():
    cur = get_cursor()
    cur.execute("SELECT strftime('%Y', MIN(date)), strftime('%Y', MAX(date)) FROM astro;") 
    return [int(year) for year in cur.fetchone()]
    
    