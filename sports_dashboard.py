import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Connect to database
conn = sqlite3.connect("kits.db")
cur = conn.cursor()

# Ensure tables exist
cur.execute('''CREATE TABLE IF NOT EXISTS kits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    total INT,
    available INT,
    lost INT DEFAULT 0,
    wornout INT DEFAULT 0)''')

cur.execute('''CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user TEXT,
    kit_name TEXT,
    action TEXT,
    fine INT DEFAULT 0,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
conn.commit()

st.title("🏏 Sports Kits Management Dashboard")

menu = ["Add Kit", "Issue Kit", "Return Kit", "Inventory", "Transactions", "Visualization"]
choice = st.sidebar.selectbox("Menu", menu)

# Add kit
if choice == "Add Kit":
    name = st.text_input("Kit Name")
    total = st.number_input("Total Quantity", min_value=1, step=1)
    if st.button("Add"):
        cur.execute("INSERT INTO kits (name, total, available) VALUES (?, ?, ?)", (name, total, total))
        conn.commit()
        st.success(f"{name} added successfully!")

# Issue kit
elif choice == "Issue Kit":
    user = st.text_input("User Name")
    kit_name = st.text_input("Kit Name")
    if st.button("Issue"):
        cur.execute("SELECT available FROM kits WHERE name=?", (kit_name,))
        row = cur.fetchone()
        if row and row[0] > 0:
            cur.execute("UPDATE kits SET available = available - 1 WHERE name=?", (kit_name,))
            cur.execute("INSERT INTO transactions (user, kit_name, action) VALUES (?, ?, ?)",
                        (user, kit_name, "issued"))
            conn.commit()
            st.success(f"{kit_name} issued to {user}")
        else:
            st.error("Kit not available")

# Return kit
elif choice == "Return Kit":
    user = st.text_input("User Name")
    kit_name = st.text_input("Kit Name")
    condition = st.selectbox("Condition", ["good", "wornout", "lost"])
    if st.button("Return"):
        fine = 0
        if condition == "lost":
            fine = 200
            cur.execute("UPDATE kits SET lost = lost + 1 WHERE name=?", (kit_name,))
        elif condition == "wornout":
            fine = 100
            cur.execute("UPDATE kits SET wornout = wornout + 1 WHERE name=?", (kit_name,))
        else:
            cur.execute("UPDATE kits SET available = available + 1 WHERE name=?", (kit_name,))
        cur.execute("INSERT INTO transactions (user, kit_name, action, fine) VALUES (?, ?, ?, ?)",
                    (user, kit_name, "returned", fine))
        conn.commit()
        st.success(f"{kit_name} returned by {user} | Fine ₹{fine}")

# Inventory
elif choice == "Inventory":
    df = pd.read_sql("SELECT * FROM kits", conn)
    st.dataframe(df)

# Transactions
elif choice == "Transactions":
    df = pd.read_sql("SELECT * FROM transactions ORDER BY date DESC", conn)
    st.dataframe(df)

# Visualization
elif choice == "Visualization":
    df = pd.read_sql("SELECT name, available, lost, wornout FROM kits", conn)
    if not df.empty:
        df.set_index("name")[["available", "lost", "wornout"]].plot(kind="bar")
        st.pyplot(plt)
    else:
        st.warning("No data available for visualization")
elif choice == "Raw Database View":
    st.subheader("📌 Kits Table")
    df1 = pd.read_sql("SELECT * FROM kits", conn)
    if not df1.empty:
        st.dataframe(df1)
    else:
        st.warning("No kits added yet!")

    st.subheader("📌 Transactions Table")
    df2 = pd.read_sql("SELECT * FROM transactions", conn)
    if not df2.empty:
        st.dataframe(df2)
    else:
        st.warning("No transactions recorded yet!")

