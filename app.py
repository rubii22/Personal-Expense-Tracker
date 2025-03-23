import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import datetime


st.set_page_config(page_title="Expense Tracker", layout="wide")

st.title("💰 Personal Expense Tracker")

# Sidebar for Inputs
st.sidebar.header("Add New Expense")
category = st.sidebar.selectbox("Category", ["Food", "Travel", "Shopping", "Bills", "Others"])
amount = st.sidebar.number_input("Amount", min_value=0.0, format="%.2f")
date = st.sidebar.date_input("Date", datetime.date.today())
description = st.sidebar.text_area("Description")

# Expense Data (In-memory)
if "expenses" not in st.session_state:
    st.session_state.expenses = pd.DataFrame(columns=["Date", "Category", "Amount", "Description"])

# Add Button
if st.sidebar.button("Add Expense"):
    new_expense = pd.DataFrame([[date, category, amount, description]], columns=["Date", "Category", "Amount", "Description"])
    st.session_state.expenses = pd.concat([st.session_state.expenses, new_expense], ignore_index=True)
    st.success("Expense Added!")

# Show Expenses
st.subheader("📊 Expense History")
st.dataframe(st.session_state.expenses)

# Download CSV
if not st.session_state.expenses.empty:
    csv = st.session_state.expenses.to_csv(index=False).encode("utf-8")
    st.download_button("Download Report", data=csv, file_name="expense_report.csv", mime="text/csv")

# Visualization
st.subheader("📈 Expense Analysis")

if not st.session_state.expenses.empty:
    fig, ax = plt.subplots(figsize=(6, 3))
    st.session_state.expenses.groupby("Category")["Amount"].sum().plot(kind="bar", ax=ax, color=["#ff9999", "#66b3ff", "#99ff99", "#ffcc99"])
    ax.set_ylabel("Total Spent")
    st.pyplot(fig)

    #  Fixed Pie Chart
    fig, ax = plt.subplots(figsize=(5, 5))
    data = st.session_state.expenses.groupby("Category")["Amount"].sum()
    wedges, texts, autotexts = ax.pie(
        data, labels=data.index, autopct='%1.1f%%', startangle=140, colors=["#ff9999", "#66b3ff", "#99ff99", "#ffcc99"]
    )

    # ✅ Fix Overlapping Labels
    for text in texts:
        text.set_size(10)
    for autotext in autotexts:
        autotext.set_size(10)
        autotext.set_color("white") 

    plt.tight_layout()  # ✅ Fix layout issues
    st.pyplot(fig)
