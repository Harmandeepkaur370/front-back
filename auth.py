from db import conn, cursor
import gradio as gr
import sqlite3

def signup(username, password):
    try:
        cursor.execute("INSERT INTO users(username,password) VALUES (?,?)", (username, password))
        conn.commit()
        return "✅ Signup successful!"
    except sqlite3.IntegrityError:
        return "⚠️ Username exists"

def login(username, password):
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    if cursor.fetchone():
        return gr.update(visible=True), gr.update(visible=False), "✅ Login success", username
    else:
        return gr.update(visible=False), gr.update(visible=True), "❌ Invalid login", None

def logout():
    return gr.update(visible=False), gr.update(visible=True)