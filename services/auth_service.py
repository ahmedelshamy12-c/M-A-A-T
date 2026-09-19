import streamlit as st 
import sqlite3






def register(username, email, password, ssn, job, age):

        conn = sqlite3.connect("data/data_base.db")
        cursor = conn.cursor()

        cursor.execute("INSERT INTO users (username, password, email, ssn, job, age) VALUES (?, ?, ?, ?, ?, ?)", (username, password, email, ssn, job, age))
        conn.commit()
        conn.close()



def login(email, password):

        conn = sqlite3.connect("data/data_base.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
        user = cursor.fetchone()
        conn.close()
    
        return user