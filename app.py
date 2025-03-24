
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import datetime

# Configure Streamlit Page
st.set_page_config(page_title="Expense Tracker", layout="wide")

st.title("💰 Personal Expense Tracker")

# Sidebar for Inputs
st.sidebar.header("➕ Add New Expense")
category = st.sidebar.selectbox("Category", ["Food", "Travel", "Shopping", "Bills", "Others"])
amount = st.sidebar.number_input("Amount", min_value=0.0, format="%.2f")
date = st.sidebar.date_input("Date", datetime.date.today())
description = st.sidebar.text_area("Description")

# Initialize Expense Data
if "expenses" not in st.session_state:
    st.session_state.expenses = pd.DataFrame(columns=["Date", "Category", "Amount", "Description"])

# Add Expense Button
if st.sidebar.button("Add Expense"):
    if amount > 0:  # ✅ Prevent adding empty expenses
        new_expense = pd.DataFrame([[date, category, amount, description]], 
                                   columns=["Date", "Category", "Amount", "Description"])
        st.session_state.expenses = pd.concat([st.session_state.expenses, new_expense], ignore_index=True)
        st.success("✅ Expense Added Successfully!")
    else:
        st.warning("⚠️ Please enter a valid amount before adding an expense.")

# Show Expense History
st.subheader("📊 Expense History")
st.dataframe(st.session_state.expenses)

# Download CSV Report
if not st.session_state.expenses.empty:
    csv = st.session_state.expenses.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download Report", data=csv, file_name="expense_report.csv", mime="text/csv")

# Visualization Section
st.subheader("📈 Expense Analysis")

if not st.session_state.expenses.empty:
    # 🔹 Bar Chart
    fig, ax = plt.subplots(figsize=(6, 3))
    st.session_state.expenses.groupby("Category")["Amount"].sum().plot(
        kind="bar", ax=ax, color=["#ff9999", "#66b3ff", "#99ff99", "#ffcc99"]
    )
    ax.set_ylabel("Total Spent")
    st.pyplot(fig)

    # 🔹 Pie Chart 
    data = st.session_state.expenses.groupby("Category")["Amount"].sum()

    if not data.empty:  
        fig, ax = plt.subplots(figsize=(5, 5))
        wedges, texts, autotexts = ax.pie(
            data, labels=data.index, autopct='%1.1f%%', startangle=140, 
            colors=["#ff9999", "#66b3ff", "#99ff99", "#ffcc99"]
        )

        
        for text in texts:
            text.set_size(10)
        for autotext in autotexts:
            autotext.set_size(10)
            autotext.set_color("white")  

        fig.tight_layout()  
        st.pyplot(fig)
    else:
        st.warning("ℹ️ No expense data available for charts.")
